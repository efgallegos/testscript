"""iGo common functionality"""

import re
import time
from utils.utils import *
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (WebDriverException,
                                        TimeoutException,
                                        NoSuchElementException,
                                        NoSuchFrameException,
                                        NoAlertPresentException,
                                        NoSuchWindowException)
from .igo_xml import createXML, createXMLException
from config_entries import config_values
from utils.browser import config_browsers


class IGO:

    """Common functionality for iGo iPipeline
        List of public Function:
            1) LogIn -> DONE
            2) logOut -> DONE
            3) viewMyCases -> DONE
            4) search -> DONE
            5) viewCaseForms -> PENDING
            6) deleteCase -> DONE
            7) importCase -> DONE
            8) exportCase -> PENDING
            9) openCase -> DONE
            10) unlockCase -> PENDING
            11) createNewCase -> PENDING
    """

    def __init__(self, driver):
        self.driver = driver
        self.driverName = getBrowserType(driver)

    def caseAction(self, case_name, action, verbose=False):
        try:
            if self.driver.current_url.find('/webforms/caselist.aspx') == -1:
                if verbose:
                    print('Navigate to "View My Cases"')
                self.viewMyCases(verbose=verbose)

            if action != 'Import':
                first_name = re.split(',', case_name)[1]
                if verbose:
                    print('Searching cases by First Name:' + first_name)
                self.search(first_name, verbose=verbose)

                if action not in config_values['igo_common']['caseActionDropdown']:
                    if verbose:
                        print('Case Action: "' + action + '" is not a valid action. Please check the valied actions in the dictionary entry "caseActionDropdown".')
                    raise IgoCaseActionException('Case Action: "' + action + '" is not a valid action. Please check the valied actions in the dictionary entry "caseActionDropdown".')

                if self.driver.find_elements_by_link_text(case_name):
                    if verbose:
                        print('Case Name: "' + case_name + '" was found.')
                        print("Looking for Case Name:" + case_name + "'s Row_id.")

                    e = self.driver.find_elements_by_link_text(case_name)[0]
                    parent = e.find_element_by_xpath('..')
                    cd = parent.find_elements_by_link_text('Case Details')[0]
                    row_id = cd.get_attribute('id')[3:cd.get_attribute('id').find('_', 3)]

                    if verbose:
                        print('Action to execute:' + action)
                        print('Row_id: ' + row_id)

                    if action != 'ViewForms':
                        case_action_id = 'gc_' + row_id + '_ddlGridActions'
                        if verbose:
                            print('Case Action Id: ' + case_action_id)
                            print('Selecting action" ' + action + '" in the case action dropdown for case name:' + case_name)

                        Select(self.driver.find_element_by_id(case_action_id)).select_by_value(action)

                    else:
                        case_action_id = 'gc$' + row_id + '$ctl05'
                        if verbose:
                            print('Case Action Id: ' + case_action_id)
                            print('Executing action" ' + action + '" for case name:' +case_name)

                        self.driver.find_element_by_name(case_action_id).click()
                else:
                    if verbose:
                        print('Case Name: "' + case_name + '" was not found in the "View My Cases" screen')
                    raise IgoCaseNotFound('Case Name: "' + case_name + '".')
            else:
                if verbose:
                    print('Selection "Import" in the case action dropdown')
                Select(self.driver.find_element_by_id('ddAct')).select_by_value(action)

        except NoSuchElementException as e:
            raise IgoCaseActionException('Case Action Exception: An unknow error took place in the caseAction function. More Details' + str(e))

    def logIn(self, carrier, environment='', username='', password='', verbose=False):
        try:
            if verbose:
                print("LogIn procedure starts")
                print('Carrier: ', carrier)
                print('Environment:', environment) 
                print('Username:', username)
                print('Password:', password)
                print('Base_url:', base_url)

            if carrier not in config_values['carriers']:
                if verbose:
                    print('Invalid Carrier.')
                raise IgoLogInException('Carrier is a mandatory value for Procedure "logIn()".')

            if not environment:
                if verbose:
                    print('Using Default environment: ', environment)
                environment = config_values[carrier]['environments']['default']
            else:
                if environment not in config_values[carrier]['environments']:
                    if verbose:
                        print('Environment not valid for Carrier.')
                    raise IgoLogInException('Environment not valid for Carrier.')

            base_url = config_values[carrier]['environments'][environment]

            if not username:
                username = config_values[carrier]['users'][environment[0:2] + '-user']
                password = config_values[carrier]['users'][environment[0:2] + '-pass']
                if verbose:
                    print('Using default environment user and password: ', username, password)

            if verbose:
                print('Carrier: ', carrier)
                print('Environment:', environment) 
                print('Username:', username)
                print('Password:', password)
                print('Base_url:', base_url)

            self.driver.get(base_url)

            if self.driver.current_url.find("/CossEnterpriseSuite/") == -1:
                if verbose:
                    print('Setting User and Password')

                elem = self.driver.find_element_by_name("user")
                elem.clear()
                elem.send_keys(username)

                elem = self.driver.find_element_by_name("password")
                elem.clear()
                elem.send_keys(password)

                elem = self.driver.find_element_by_name("Submit")
                elem.click()

                if verbose:
                    print('Checking that the start page is Displayed')

                elem = WebDriverWait(self.driver,30).until(lambda x: x.find_element_by_id("mycases-button"))

            if verbose:
                print("LogIn Bankers Method Finished successfully")
        except Exception as e:
            raise IgoLogInException(str(e))


    def logOut(self, verbose=False):
        if verbose:
            print('Log Out Bankers."')
        self.driver.find_element_by_id("lnkSignOut").click()

        current_window = self.driver.current_window_handle

        for winHandle in self.driver.window_handles:
            self.driver.switch_to.window(winHandle)
            if self.driver.title == 'Sign Out?':
                if verbose:
                    print('Pop Up Displayed.')
                    print('Pop Up Title:' + self.driver.title)
                self.driver.find_element_by_css_selector("input.csd_button").click()
                break

        if verbose:
            print('Log out successfully.')
            print('Switching back to main windows.')
        self.driver.switch_to.window(current_window)


    def viewMyCases(self, verbose=False):
        if verbose:
            print('Navigating to "View My Cases"')

        try:
            if self.driver.find_elements_by_id('mycases-button'):
                self.driver.find_element_by_id('mycases-button').click()

                if verbose:
                    print('Navigating to "View My Cases" - Completed 1')

            elif self.driver.find_elements_by_id('spanMyCases'):
                self.driver.find_element_by_id('spanMyCases').click()

                if verbose:
                    print('Navigating to "View My Cases" - Completed')

            try:
                WebDriverWait(self.driver, 30).until(lambda x: x.find_element_by_id("gc_btnNewCase"))
            except TimeoutException as e:
                raise IgoViewMyCasesException('The "View My Cases" screen was not loaded and a Timeout Exception took place. More datils:' + str(e))
        except NoSuchElementException as e:
            raise IgoViewMyCasesException('Unhandle error. More datils:' + str(e))


    def search(self, target, verbose=False):
        if verbose:
            print('iGO Search - target:' + target)

        try:
            if self.driver.current_url.find('/webforms/caselist.aspx') == -1:
                    if verbose:
                        print('Navigate to "View My Cases"')
                    self.viewMyCases()

            if verbose:
                print('Searching target...')
            self.driver.find_element_by_id("txtSearch").clear()
            self.driver.find_element_by_id("txtSearch").send_keys(target)
            self.driver.find_element_by_id("btnSearch").click()

            if verbose:
                print('Searching target completed...')
        except NoSuchElementException as e:
            raise IgoSearchException('iGO Search Failed - More Details:' + str(e))


    def viewCaseForms(self, case_name, verbose=False):
        if verbose:
            print('Stating "View Case Forms" process...')
            print('Case Name: ' + case_name)
        try:
            if verbose:
                print("Call to self.caseAction(case_name,'ViewForms',verbose)")
            self.caseAction(case_name,'ViewForms', verbose)
        except IgoCaseNotFound as e:
            if verbose:
                print('Case Name was not found...')
            raise IgoCaseViewException('Case Name was not found. More Details:' + str(e))
        except IgoCaseActionException as e:
            if verbose:
                print('Call to self.caseAction failed...')
            raise IgoCaseViewException('Call to self.caseAction failed. More Details:' + str(e))

        # Checking the Label "LOADING..."
        try:
            if verbose:
                print('Forms are bieng loading...')
            WebDriverWait(self.driver, 30).until(lambda x: x.find_element_by_class_name("cases_container").find_element_by_id('lblLoading'))
        except TimeoutException as e:
            if verbose:
                print('View Forms process failed, the Froms are not being loaded. More details:' + str(e))
            raise IgoCaseViewException('View Forms process failed, the Froms are not being loaded. More details:' + str(e))

        if verbose:
            print('Checing the View Forms Request status...')

        try:
            WebDriverWait(self.driver, 30).until(lambda x: x.find_element_by_class_name("cases_container").find_element_by_id('lblFormsOK'))
            if verbose:
                print('View Forms process was completed successfully.')
        except TimeoutException as e:
            try:
                WebDriverWait(self.driver, 30).until(lambda x: x.find_element_by_class_name("cases_container").find_element_by_id('lblFormsError'))
                if verbose:
                    print('View Forms process failed - There was an error in the PDF creation.')
                raise IgoCaseViewException('View Forms process failed - There was an error in the PDF creation.')
            except TimeoutException as e:
                if verbose:
                    print('Unknow status of the View Form process. The script was not able to capture the status of the process. More Details: ' + str(e))
                raise IgoCaseViewException('Unknow status of the View Form process. The script was not able to capture the status of the process. More Details: ' + str(e))

        current_window = self.driver.current_window_handle

        if verbose:
            print('Current Windows:' + current_window)

        try:
            if verbose:
                print('Window handles: ', self.driver.window_handles)

            for winHandle in self.driver.window_handles:
                try:
                    self.driver.switch_to.window(winHandle)
                    if verbose:
                        print('winHandle', winHandle)
                        print('Windows title:', self.driver.title)
                except NoSuchWindowException as e:
                    if verbose:
                        print('Failed to switch to the "View Forms" window handle. More Details:' + str(e))
                    raise IgoCaseViewException('Failed to switch to the "View Forms" window handle. More Details:' + str(e))

                if len(self.driver.window_handles) == 2 and winHandle != current_window:
                    try:
                        if verbose:
                            print('Switching to "View Froms" Iframe...')
                        self.driver.switch_to.frame("Iframe1")
                        if verbose:
                            print('Switch to "View Froms" Iframe completed.')
                    except NoSuchFrameException as e:
                        raise IgoCaseViewException('Failed to switch to the "View Forms" Iframe. More Details:' + str(e))

                    elem = WebDriverWait(self.driver, 30).until(lambda x: x.find_element_by_id("pageContainer1"))

                    if elem:
                        if verbose:
                            print('PDF loaded successfully.')
                            print('Starting PDF download...')

                        # TODO: Rutina para descargar el PDF. Usar libreria standar de python para manipular el Windows dialgo.
                        pdf_save_path = config_values[carrier]['carrier_path'] + \
                                        config_values['os_path_separator'] + \
                                        config_values[carrier][product]['product_path'] + \
                                        config_values['os_path_separator'] + \
                                        config_values[carrier][product]['form_path'] + \
                                        case_name + '.pdf'

                        if verbose:
                            print('Download file path: ' + pdf_save_path)

                        win = WindowFinder()
                        win.find_window_wildcard(config_browsers[self.driverName]['saveWindow'])
                        win.set_foreground()
                        ent = "{ENTER}"                  # Enter key stroke.
                        SendKeys(pdf_save_path)          # Use SendKeys to send path string to Save As dialog
                        SendKeys(ent)                    # Use SendKeys to send ENTER key stroke to Save As dialog

                        if verbose:
                            print('PDF downloaded successfully.')
                            print('Closing "View Forms" window.')

                        self.driver.close()
                        break
                    else:
                        raise IgoCaseViewException('PDF failed to be loaded in Iframe container.')

            if verbose:
                print('Switching back to Current Window: ' + current_window)
            self.driver.switch_to.window(current_window)

        except Exception as e:
            if verbose:
                print('View Froms - Unhandle exception.')
            raise IgoCaseViewException('View Form - Unhandle exception.')


    def importCase(self, carrier, product, state, plan, verbose=False):
        if carrier not in config_values['carriers']:
            if verbose:
                print('Skipping "import Case" process - Invalid Carrier: ' + carrier)
            raise InvalidProductPlanState(carrier, product, plan, state)
        if product not in config_values[carrier]['products']:
            if verbose:
                print('Skipping "Import Case" process - Invalid product: ' + product)
            raise InvalidProductPlanState(carrier, product, plan, state)
        elif plan not in config_values[carrier][product]['plans']:
            if verbose:
                print('Skipping "Import Case" process - Invalid plan: ' + plan)
            raise InvalidProductPlanState(carrier, product, plan, state)
        elif state not in config_values[carrier][product]['states']:
            if verbose:
                print('Skipping "Import Case" process - Invalid State (' + state + ') for product: ' + product)
            raise InvalidProductPlanState(carrier, product, plan, state)
        else:
            if verbose:
                print('Stating "Import Case" process...')
            
            if verbose:
                print('product:', product)
                print('plan:', plan)

            if verbose:
                print('Calling to createXML(carrier, product, state, plan, verbose)...')

            try:
                file_full_path = createXML(carrier, product, state, plan, verbose)
                if verbose:
                    print('file_full_path:', file_full_path)
            except createXMLException as e:
                if verbose:
                    print('Function createXML() failed...')
                raise IgoCaseImportExcepﬂtion('Function createXML() failed. More Details:' + str(e))

            current_window = self.driver.current_window_handle

            if verbose:
                print('current_window:', current_window)

            try:
                if verbose:
                    print("Call to self.caseAction('','Import',verbose)")
                self.caseAction('', 'Import', verbose)
            except IgoCaseActionException as e:
                if verbose:
                    print('Call to self.caseAction failed...')
                raise IgoCaseImportException('Call to self.caseAction failed. More Details:' + str(e))

            try:
                file_imported = False
                for winHandle in self.driver.window_handles:
                    try:
                        self.driver.switch_to.window(winHandle)
                        if verbose:
                            print('winHandle', winHandle)
                            print('Windows title:', self.driver.title)
                    except NoSuchWindowException as e:
                        if verbose:
                            print('Failed to switch to import window handle. More Details:' + str(e))
                        raise IgoCaseImportException('Failed to switch to import window handle. More Details:' + str(e))

                    if self.driver.title =='Import Case':                                                
                        try:
                            if verbose:
                                print('Setting file path in Pop up.')
                            elem = WebDriverWait(self.driver,30).until(lambda x: x.find_element_by_id("ClientFile"))
                            elem.send_keys(file_full_path)

                            if verbose:
                                print('Submiting Import Case in Pop up.')
                            self.driver.find_element_by_id("Submit1").click()
                            file_imported = True
                            break
                        except TimeoutException as e:
                            if verbose:
                                print('Import windows never displayed. More details:' + str(e))
                            raise IgoCaseImportException('Import windows never displayed. More details:' + str(e))

                if verbose:
                    print('Switching back to main window.')
                self.driver.switch_to.window(current_window)

                time.sleep(10)

                if file_imported:
                    if verbose:
                        print(current_window)
                        print('Import pop up closed.')
                        print('Checking the case in "My View Cases".')

                    # case_name = "LastName, FirstName"
                    case_name = config_values[carrier][product]['name'] + ', ' + state + '_' + plan        
                    

                    if verbose:
                        print('Searching for: ' + case_name)

                    try:
                        if self.driver.find_elements_by_link_text(case_name):
                            if verbose:
                                print('Case Name: '+case_name+ ' found in "View My Cases"- Import Case Finished successfully.')
                                print('Importing case - Finished successfully.')
                        else:
                            if verbose:
                                print('Import case - Failed. The case is not listed in the "View My Cases" screen.')
                            raise IgoCaseImportException('Unkonw error. Case was not imported. The case is not listed in '
                                                         'the "View My Cases" screen.')
                    except (WebDriverException, NoSuchElementException) as e:
                        if verbose:
                            print('Impot Case - Failed. find_elements_by_link_text failed for case name:' + case_name)
                        raise IgoCaseImportException('Impot Case - Failed. find_elements_by_link_text failed for case name:' + case_name)

                else:
                    if verbose:
                        print('File Impot pop up windows never displayed. Faled to import file.')
                    raise IgoCaseImportException('File Impot pop up windows never displayed. Faled to import file.')

            except Exception as e:
                if verbose:
                    print('Import Case - Unhandle exception.')
                raise IgoCaseImportException('Import Case - Unhandle exception.')


    def deleteCase(self, case_name, verbose):
        try:
            if verbose:
                print("Call to self.caseAction(case_name,'Delete',verbose)")
            self.caseAction(case_name, 'Delete', verbose)
        except IgoCaseNotFound as e:
            if verbose:
                print('Case Name "' + case_name +'" was not found...')
            raise IgoCaseDeleteException('Case Name "' + case_name + '" was not found. More Details:' + str(e))
        except IgoCaseActionException as e:
            if verbose:
                print('Call to self.caseAction failed...')
            raise IgoCaseDeleteException('Call to self.caseAction failed. More Details:' + str(e))

        try:
            if verbose:
                print('Waiting for the Alert to pop up...')
            WebDriverWait(self.driver, 30).until(EC.alert_is_present())
        except TimeoutException as e:
            if verbose:
                print('Alert never pop up...')
            raise IgoCaseDeleteException('Alert never pop up. More Details:' + str(e))

        try:
            if verbose:
                print('Delete alert was found')
                print('Switching focus to Alert.')

            alert = self.driver.switch_to.alert

            if alert.text == 'Are you sure?':
                if verbose:
                    print('Alert text: ' + alert.text)
                    print('Accept Alert.')
                alert.accept()
            else:
                if verbose:
                    print('Invalid message in the Delete alert pop up. More Details:' + alert.text)
                raise IgoCaseDeleteException('Invalid message in the Delete alert pop up. More Details:' + alert.text)
        except NoAlertPresentException as e:
            if verbose:
                print('Failed to switch to Alert pop up...')
            raise IgoCaseDeleteException('Failed to switch to Alert pop up. More Details:' + str(e))

        try:
            if verbose:
                print('Waiting for delete confirmation pop up...')
            WebDriverWait(self.driver, 30).until(EC.alert_is_present())
        except TimeoutException as e:
            if verbose:
                print('Alert never pop up...')
            raise IgoCaseDeleteException('Confirmation Delete alert never pop up. More Details:' + str(e))

        try:
            if verbose:
                print('Confirmation Delete alert was found')
                print('Switching focus to Confirmation Delete alert pop up.')

            alert = self.driver.switch_to.alert

            if alert.text == 'The cases were deleted successfully.':
                if verbose:
                    print('Alert text: ' + alert.text)
                    print('Accept Alert.')
                alert.accept()
            else:
                if verbose:
                    print('Invalid message in the Confirmation Delete alert pop up. More Details:' + alert.text)
                raise IgoCaseDeleteException('Invalid message in the Confirmation Delete alert pop up. More Details:' + alert.text)
        except NoAlertPresentException as e:
            if verbose:
                print('Failed to switch to Confirmation Delete alert pop up...')
            raise IgoCaseDeleteException('Failed to switch to Confirmation Delete alert pop up. More Details:' + str(e))  


    def exportCase(self, product, case_name, verbose=False):
        # TODO: This has to be implemented

        if verbose:
            print('starting exportCase process...')
            print('Case Name: ' + case_name)

        try:
            if verbose:
                print("Call to self.caseAction(case_name,'Export',verbose)")
            self.caseAction(case_name, 'Export', verbose)
        except IgoCaseNotFound as e:
            if verbose:
                print('Case Name "' + case_name + '" was not found...')
            raise IgoCaseExportxception('Case Name "' + case_name + '" was not found. More Details:' + str(e))
        except IgoCaseActionException as e:
            if verbose:
                print('Call to self.caseAction failed...')
            raise IgoCaseExportxception('Call to self.caseAction failed. More Details:' + str(e))

        current_window = self.driver.current_window_handle

        if verbose:
            print('Current windows: ' + current_window)

        file_full_path = config_values[carrier]['base_path'] + \
                         config_values[carrier][product]['product_path'] + \
                         config_values[carrier][product]['xml_export_path'] + \
                         case_name + '.xml'

        if verbose:
            print('file_full_path: ' + file_full_path)

        try:
            for winHandle in self.driver.window_handles:
                try:
                    self.driver.switch_to.window(winHandle)
                    if verbose:
                        print('winHandle', winHandle)
                        print('Windows title:', self.driver.title)
                except NoSuchWindowException as e:
                    if verbose:
                        print('Failed to switch to import window handle. More Details:' + str(e))
                    raise IgoCaseExportxception('Failed to switch to import window handle. More Details:' + str(e))

                if self.driver.title == 'Export Case':
                    if verbose:
                        print('Switched to Export pop up correctly.')
                        print('Downloading the case XML to the following path: ' + file_full_path)

                    # TODO: Save File
                    e = self.driver.find_element_by_tag_name('a')

                    if verbose:
                        print('Element ID:' + e.id)
                        print('Element Text:' + e.text)
                        print('Element Attribute "href":' + e.get_attribute('href'))

                    try:
                        rightClickSaveLinkAs(self.driver, e, verbose)
                        if verbose:
                            print('Window "Save As..." opened successfully.')

                    except Exception as e:
                        raise IgoCaseExportxception('Failed to open windows "Save As..." window. More Details:' + str(e))

                    try:
                        time.sleep(3)
                        win = WindowFinder()
                        win.find_window_wildcard(config_browsers[self.driverName]['saveWindow'])
                        win.set_foreground()
                        ent = "{ENTER}"                   # Enter key stroke.
                        SendKeys(file_full_path)          # Use SendKeys to send path string to Save As dialog
                        SendKeys(ent)                     # Use SendKeys to send ENTER key stroke to Save As dialog
                    except Exception as e:
                        raise IgoCaseExportxception('Failed to interact to windows "Save As..." window. More Details:' + str(e))

                    if verbose:
                        print('File downloaded successfully.')
                    break

            if verbose:
                print('Switching back to main window...')
            self.driver.switch_to.window(current_window)

        except Exception as e:
            if verbose:
                print('Import Case - Unhandle exception.')
            raise IgoCaseExportxception('Import Case - Unhandle exception.')


    def openCase(self, case_name, verbose=False):
        if verbose:
            print('starting openCase process...')
            print('Case Name: ' + case_name)

        try:
            if verbose:
                print("Call to self.caseAction(case_name,'OpenCase',verbose)")
            self.caseAction(case_name, 'OpenCase', verbose)
        except IgoCaseNotFound as e:
            if verbose:
                print('Case Name "' + case_name + '" was not found...')
            raise IgoCaseOpenException('Case Name "' + case_name + '" was not found. More Details:' + str(e))
        except IgoCaseActionException as e:
            if verbose:
                print('Call to self.caseAction failed...')
            raise IgoCaseOpenException('Call to self.caseAction failed. More Details:' + str(e))

        try:
            if verbose:
                print('Waiting for case "Case Information" screen to be loaded...')
            WebDriverWait(self.driver, 30).until(lambda x: x.find_element_by_id("header_client_name"))
            if verbose:
                print('finished openCase process...')
        except TimeoutException as e:
            if verbose:
                print('Failed to load "Case Information" screen for case name: ' + case_name + '. More Details: ' + str(e))
            raise IgoCaseOpenException('Failed to load "Case Information" screen for case name: ' + case_name + '. More Details: ' + str(e))


class IgoLogInException(Exception):

    def __init__(self, value):
        self.value = '"Log In Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)


class IgoCaseImportException(Exception):

    def __init__(self, value):
        self.value = '"Case Import Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)


class InvalidProductPlanState(Exception):

    def __init__(self, carrier, product, plan, state):
        self.value = ('"Case Import Exception" - Details: Invalid Carrier/Product/Plan/state combination. '
                     'Carrier:' + carrier + ', Product:' + product + ', Plan:' + plan + ', State:' + state + 
                     '. Please check the dictionary to see the valid Product/Plan/State combinations.')

    def __str__(self):
        return repr(self.value)


class IgoCaseDeleteException(Exception):

    def __init__(self, value):
        self.value = '"Delete Case Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)


class IgoCaseActionException(Exception):

    def __init__(self, value):
        self.value = '"Delete Case Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)


class IgoCaseNotFound(Exception):

    def __init__(self, value):
        self.value = '"Case Not Found" - Details:' + value

    def __str__(self):
        return repr(self.value)


class IgoViewMyCasesException(Exception):

    def __init__(self, value):
        self.value = 'Navigate to "View My Case" Failed - Details:' + value

    def __str__(self):
        return repr(self.value)


class IgoSearchException(Exception):

    def __init__(self, value):
        self.value = 'Case Search Failed - Details:' + value

    def __str__(self):
        return repr(self.value)


class IgoCaseViewException(Exception):

    def __init__(self, value):
        self.value = '"View Forms Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)


class IgoCaseOpenException(Exception):

    def __init__(self, value):
        self.value = '"Open Case Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)


class IgoCaseExportxception(Exception):

    def __init__(self, value):
        self.value = '"Export Case Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)
