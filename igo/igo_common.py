"""
    Common functionality for iGo iPipeline
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

import re
import time
from utils.browser import *
#from utils.utils import *
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (WebDriverException,
                                        TimeoutException,
                                        NoSuchElementException,
                                        #NoSuchFrameException,
                                        NoAlertPresentException,
                                        NoSuchWindowException)
from .igo_xml import createXML, createXMLException
from config_entries import config_values


def caseAction(driver, case_name, action, verbose=False):
    ####################################################################################
    #                                 caseAction                                       #
    ####################################################################################
    # This fuction allows the script to identify an application case in the "View My   #
    # Cases" screen in order to select a valid action from the dropdownlist on         #
    # config_values['igo_common']['caseActionDropdown'] dictionary.                    #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #
    #              or Google Chorme.                                                   #
    # 2) case_name: It is the aplication name e.g.: "LastName, FirstName".             #
    #                                                                                  #
    # 3) action: Sets the action to be selected on the dropdown                        #
    # 4) verbose: Determines the log level for this procedure.                         #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) action not listed in config_values['igo_common']['caseActionDropdown']        #
    # 2) case_name not found by iGo Search                                             #
    # 3) Selenium NoSuchElementException Exception                                     #
    # 4) Unknown Exception                                                             #
    #                                                                                  #
    ####################################################################################

    if action not in config_values['igo_common']['caseActionDropdown']:
        msg = 'Case Action: "' + action + '" is not a valid action. Please check the valid actions in the IGo Common dictionary entry "caseActionDropdown".'
        if verbose:
            print(msg)
        raise IgoCommonException('caseAction', [('case_name',case_name),('action',action)], msg)
    try:
        if driver.current_url.find('/webforms/caselist.aspx') == -1:
            if verbose:
                print('Navigate to "View My Cases"')
            viewMyCases(driver, verbose=verbose)

        if action != 'Import':
            first_name = re.split(',', case_name)[1]
            if verbose:
                print('Searching cases by First Name:' + first_name)
            search(driver, first_name, verbose=verbose)

            if driver.find_elements_by_link_text(case_name):
                if verbose:
                    print('Case Name: "' + case_name + '" was found.')
                    print("Looking for Case Name:" + case_name + "'s Row_id.")

                e = driver.find_elements_by_link_text(case_name)[0]
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

                    Select(driver.find_element_by_id(case_action_id)).select_by_value(action)
                else:
                    case_action_id = 'gc$' + row_id + '$ctl05'
                    if verbose:
                        print('Case Action Id: ' + case_action_id)
                        print('Executing action" ' + action + '" for case name:' +case_name)
                    driver.find_element_by_name(case_action_id).click()
            else:
                msg = 'Case Name: "' + case_name + '" was not found in the "View My Cases" screen'
                if verbose:
                    print(msg)
                IgoCommonException('caseAction', [['case_name',case_name],['action',action]], msg)
        else:
            if verbose:
                print('Selection "Import" in the case action dropdown')
            Select(driver.find_element_by_id('ddAct')).select_by_value(action)

    except NoSuchElementException as e:
        msg = 'NoSuchElementException Selenium Exception: Element not found by the Selenium Driver. More Details: ' + repr(e)
        if verbose:
            print(msg)
        raise IgoCommonException('caseAction', [('case_name',case_name),('action',action)], msg)
    except Exception as e:
        msg = 'Exception: An unknown Exception has occurred. More Details: ' + repr(e)
        if verbose:
            print(msg)
        raise IgoCommonException('caseAction', [('case_name',case_name),('action',action)], msg)

def logIn(driver, carrier, environment='', username='', password='', verbose=False):
    ####################################################################################
    #                                    logIn                                         #
    ####################################################################################
    # This fuction allows the script to login iGo for a specific carrier like Bankers  #
    # JH, Anico, MetLife, etc.                                                         #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #
    #            or Google Chorme.                                                     #
    # 2) Carrier: Sets the carrier for the application case that would be created,     #
    #             e.g.: Bankers, Lincol, MetLife. The value must match one of the      #
    #             config_values['carriers'] entries.                                   #
    # 3) Environment (optional): Sets one of the QA or UAT environments e.g.: QD3,     #
    #                            QD4, TD1, TD3. If not value is defined QD3 is used as #
    #                            the default value.                                    #
    # 4) username (optional): Specify the username value to be used in the             #
    #                         authentication process. If not value is defined QD3 user #
    #                         will be used as default.                                 #
    # 5) password (optional): Specify the password value to be used in the             #
    #                         authentication process. If not value is defined QD3 pass #
    #                         will be used as default.                                 #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) carrier not listed in config_values['carriers']                               #
    # 2) environment not listed in config_values[carrier]['environments']              #
    # 3) Selenium NoSuchElementException Exception                                     #
    # 4) Unknown Exception                                                             #
    #                                                                                  #
    ####################################################################################
    if verbose:
        print("LogIn procedure parameters:")
        print('Carrier: ', carrier)
        print('Environment:', environment)
        print('Username:', username)
        print('Password:', password)

    if carrier not in config_values['carriers']:
        msg = 'LogIn Failed. Invalid Carrier. ' + carrier + " is not listed in config_values['carriers']"
        if verbose:
            print(msg)
        raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)

    if not environment:
        if verbose:
            print('Using Default environment: ', environment)
        environment = config_values[carrier]['environments']['default']
    else:
        if environment not in config_values[carrier]['environments']:
            msg = 'LogIn Failed. Environment "' + environment + '"not valid for carrier "' + carrier +". Please check the config_values[carrier]['environments'] dictionary."
            if verbose:
                print(msg)
            raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)

    base_url = config_values[carrier]['environments'][environment]

    if not username:
        username = config_values[carrier]['users'][environment[0:2] + '-user']
        password = config_values[carrier]['users'][environment[0:2] + '-pass']
        if verbose:
            print('Using default environment user and password: ', username, password)

    try:
        if verbose:
            print("LogIn procedure final parameters:")
            print('Carrier: ', carrier)
            print('Environment:', environment)
            print('Username:', username)
            print('Password:', password)
            print('Base_url:', base_url)

        driver.get(base_url)

        if driver.current_url.find("/CossEnterpriseSuite/") == -1:
            if verbose:
                print('Setting User and Password')

            elem = driver.find_element_by_name("user")
            elem.clear()
            elem.send_keys(username)

            elem = driver.find_element_by_name("password")
            elem.clear()
            elem.send_keys(password)

            elem = driver.find_element_by_name("Submit")
            elem.click()

            if verbose:
                print('Checking that the start page is Displayed')

            try:
                elem = WebDriverWait(driver,30).until(lambda x: x.find_element_by_id("mycases-button"))
            except TimeoutException as e:
                msg = 'LogIn Failed. TimeoutException Selenium Exception: "mycases-button" button not found. More Details: ' + repr(e)
                if verbose:
                    print(msg)
                raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)
            if verbose:
                print("LogIn finished successfully")
        else:
            msg = 'LogIn Failed. The carrier "' + carrier + '" login screen failed to load.'
            if verbose:
                print(msg)
            raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)

    except NoSuchElementException as e:
        msg = 'LogIn Failed. NoSuchElementException Selenium Exception: Element not found by the Selenium Driver. More Details: ' + repr(e)
        if verbose:
            print(msg)
        raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)
    except Exception as e:
        msg = 'LogIn Failed. An unknown Exception has occurred. More Details:' + repr(e)
        if verbose:
            print(msg)
        # carrier, environment='', username='', password=''
        raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)

def logOut(driver, verbose=False):
    ####################################################################################
    #                                    logOut                                        #
    ####################################################################################
    # This fuction allows the script to logout iGo for any carrier                     #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #
    #            or Google Chorme.                                                     #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) WebDriverException when something failed within the webdriver.                #
    #                                                                                  #
    ####################################################################################
    if verbose:
        print('Log Out procedure starts."')
    try:
        driver.find_element_by_id("lnkSignOut").click()

        current_window = driver.current_window_handle

        for winHandle in driver.window_handles:
            driver.switch_to.window(winHandle)
            if driver.title == 'Sign Out?':
                if verbose:
                    print('Pop Up Displayed.')
                    print('Pop Up Title:' + driver.title)
                driver.find_element_by_css_selector("input.csd_button").click()
                break

        if verbose:
            print('Log out successfully.')
            print('Switching back to main windows.')
        driver.switch_to.window(current_window)

    except Exception as e:
        msg = 'LogOut Failed. An unknown exception has occured. More details: ' + repr(e)
        if verbose:
            print(msg)
        raise IgoCommonException('logOut', None, msg)

def viewMyCases(driver, verbose=False):
    ####################################################################################
    #                                  viewMyCases                                     #
    ####################################################################################
    # This fuction allows the script to navigate to the "View My Cases" screen for any #
    # carrier                                                                          #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #
    #            or Google Chorme.                                                     #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) TimeoutException when the View My Cases screen failed to be loaded.           #
    # 2) Exception: Unknow exception.                                                  #
    #                                                                                  #
    ####################################################################################
    if verbose:
        print('Navigating to "View My Cases" started...')

    try:
        if driver.find_elements_by_id('mycases-button'):
            driver.find_element_by_id('mycases-button').click()
            if verbose:
                print('Navigating to "View My Cases" - Completed 1')

        elif driver.find_elements_by_id('spanMyCases'):
            driver.find_element_by_id('spanMyCases').click()

            if verbose:
                print('Navigating to "View My Cases" - Completed')
        try:
            WebDriverWait(driver, 30).until(lambda x: x.find_element_by_id("gc_btnNewCase"))
        except TimeoutException as e:
            msg = 'viewMyCases Failed. The "View My Cases" screen was not loaded and a Timeout Exception took place. More datils:' + repr(e)
            if verbose:
                print(msg)
            raise IgoCommonException('viewMyCases', None, msg)
    except Exception as e:
        msg = 'viewMyCases Failed. An unknown exception has occured. More datils:' + repr(e)
        if verbose:
            print(msg)
        raise IgoCommonException('viewMyCases', None, msg)

def search(driver, target, verbose=False):
    ####################################################################################
    #                                    search                                        #
    ####################################################################################
    # This fuction allows the script to search an application case in the "View My     #
    # Cases" screen                                                                    #
    # carrier                                                                          #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #
    #            or Google Chorme.                                                     #
    # 2) target: Is the value to be used in the iGo search function.                   #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) TimeoutException when the View My Cases screen failed to be loaded.           #
    # 2) Exception: Unknow exception.                                                  #
    #                                                                                  #
    ####################################################################################
    if verbose:
        print('iGO Search process started')
        print('Target:' + target)

    try:
        if driver.current_url.find('/webforms/caselist.aspx') == -1:
            if verbose:
                print('Navigate to "View My Cases"')
            viewMyCases(driver, verbose)

        if verbose:
            print('Searching target...')
        driver.find_element_by_id("txtSearch").clear()
        driver.find_element_by_id("txtSearch").send_keys(target)
        driver.find_element_by_id("btnSearch").click()

        if verbose:
            print('Searching target completed...')
    except NoSuchElementException as e:
        msg = 'Search Failed - The search element was not found. More Details:' + repr(e)
        if verbose:
            print(msg)
        raise IgoCommonException('search', [('target',target)], msg)

# def viewCaseForms(driver, case_name, verbose=False):
#     if verbose:
#         print('Stating "View Case Forms" process...')
#         print('Case Name: ' + case_name)
#     try:
#         if verbose:
#             print("Call to caseAction(case_name,'ViewForms',verbose)")
#         caseAction(driver, case_name,'ViewForms', verbose)
#     except IgoCaseNotFound as e:
#         if verbose:
#             print('Case Name was not found...')
#         raise IgoCaseViewException('Case Name was not found. More Details:' + str(e))
#     except IgoCaseActionException as e:
#         if verbose:
#             print('Call to caseAction failed...')
#         raise IgoCaseViewException('Call to caseAction failed. More Details:' + str(e))

#     # Checking the Label "LOADING..."
#     try:
#         if verbose:
#             print('Forms are bieng loading...')
#         WebDriverWait(driver, 30).until(lambda x: x.find_element_by_class_name("cases_container").find_element_by_id('lblLoading'))
#     except TimeoutException as e:
#         if verbose:
#             print('View Forms process failed, the Froms are not being loaded. More details:' + str(e))
#         raise IgoCaseViewException('View Forms process failed, the Froms are not being loaded. More details:' + str(e))

#     if verbose:
#         print('Checing the View Forms Request status...')

#     try:
#         WebDriverWait(driver, 30).until(lambda x: x.find_element_by_class_name("cases_container").find_element_by_id('lblFormsOK'))
#         if verbose:
#             print('View Forms process was completed successfully.')
#     except TimeoutException as e:
#         try:
#             WebDriverWait(driver, 30).until(lambda x: x.find_element_by_class_name("cases_container").find_element_by_id('lblFormsError'))
#             if verbose:
#                 print('View Forms process failed - There was an error in the PDF creation.')
#             raise IgoCaseViewException('View Forms process failed - There was an error in the PDF creation.')
#         except TimeoutException as e:
#             if verbose:
#                 print('Unknow status of the View Form process. The script was not able to capture the status of the process. More Details: ' + str(e))
#             raise IgoCaseViewException('Unknow status of the View Form process. The script was not able to capture the status of the process. More Details: ' + str(e))

#     current_window = driver.current_window_handle

#     if verbose:
#         print('Current Windows:' + current_window)

#     try:
#         if verbose:
#             print('Window handles: ', driver.window_handles)

#         for winHandle in driver.window_handles:
#             try:
#                 driver.switch_to.window(winHandle)
#                 if verbose:
#                     print('winHandle', winHandle)
#                     print('Windows title:', driver.title)
#             except NoSuchWindowException as e:
#                 if verbose:
#                     print('Failed to switch to the "View Forms" window handle. More Details:' + str(e))
#                 raise IgoCaseViewException('Failed to switch to the "View Forms" window handle. More Details:' + str(e))

#             if len(driver.window_handles) == 2 and winHandle != current_window:
#                 try:
#                     if verbose:
#                         print('Switching to "View Froms" Iframe...')
#                     driver.switch_to.frame("Iframe1")
#                     if verbose:
#                         print('Switch to "View Froms" Iframe completed.')
#                 except NoSuchFrameException as e:
#                     raise IgoCaseViewException('Failed to switch to the "View Forms" Iframe. More Details:' + str(e))

#                 elem = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_id("pageContainer1"))

#                 if elem:
#                     if verbose:
#                         print('PDF loaded successfully.')
#                         print('Starting PDF download...')

#                     # TODO: Rutina para descargar el PDF. Usar libreria standar de python para manipular el Windows dialgo.
#                     # pdf_save_path = config_values[carrier]['carrier_path'] + \
#                     #                 config_values['os_path_separator'] + \
#                     #                 config_values[carrier][product]['product_path'] + \
#                     #                 config_values['os_path_separator'] + \
#                     #                 config_values[carrier][product]['form_path'] + \
#                     #                 case_name + '.pdf'

#                     if verbose:
#                         print('Download file path: ' + pdf_save_path)

#                     # win = WindowFinder()
#                     # win.find_window_wildcard(config_browsers[getBrowserType(driver)]['saveWindow'])
#                     # win.set_foreground()
#                     # ent = "{ENTER}"                  # Enter key stroke.
#                     # SendKeys(pdf_save_path)          # Use SendKeys to send path string to Save As dialog
#                     # SendKeys(ent)                    # Use SendKeys to send ENTER key stroke to Save As dialog

#                     if verbose:
#                         print('PDF downloaded successfully.')
#                         print('Closing "View Forms" window.')

#                     driver.close()
#                     break
#                 else:
#                     raise IgoCaseViewException('PDF failed to be loaded in Iframe container.')

#         if verbose:
#             print('Switching back to Current Window: ' + current_window)
#         driver.switch_to.window(current_window)

#     except Exception as e:
#         if verbose:
#             print('View Froms - Unhandle exception.')
#         raise IgoCaseViewException('View Form - Unhandle exception.')

def importCase(driver, carrier, product, state, plan, verbose=False):
    ####################################################################################
    #                                  importCase                                      #
    ####################################################################################
    # This fuction allows the script to import an application case (xml) in iGo for a  #
    # specific carrier like Bankers, JH, Anico, MetLife, etc.                          #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #
    #            or Google Chorme.                                                     #
    # 2) Carrier: Sets the carrier for the application case that would be created,     #
    #             e.g.: Bankers, Lincol, MetLife. The value must match one of the      #
    #             config_values['carriers'] entries.                                   #
    # 3) Product: Sets the product that would be used to create the applciation case.  #
    #             This value should match one of the                                   #
    #             config_values[carrier]['prodcuts'] entries.                          #
    # 4) State: Sets the state for the application case e.g.: AL, AK, NY, etc. The     #
    #           value must match one of the config_values[carrier]['states'] entries   #
    # 5) Plan:  Sets the plan for the application case. e.g.: LA02P, 19E, 20E, etc.    #
    #           This value must match one of the config_values[carrier]['plans']       #
    #           entries.                                                               #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) carrier not listed in config_values['carriers']                               #
    # 2) product not listed in config_values[carrier]['products']                      #
    # 3) plan not in config_values[carrier][product]['plans']                          #
    # 4) state not in config_values[carrier][product]['states']                        #
    #                                                                                  #
    ####################################################################################
    if verbose:
        print('Stating "Import Case" process...')
        print('carrier: ', carrier)
        print('product:', product)
        print('state: ', state)
        print('plan:', plan)

    if carrier not in config_values['carriers']:
        msg = 'importCase Failed - Invalid Carrier: ' + carrier
        if verbose:
            print(msg)
        raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
    if product not in config_values[carrier]['products']:
        msg = 'importCase Failed - Invalid product: ' + product
        if verbose:
            print(msg)
        raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
    elif plan not in config_values[carrier][product]['plans']:
        msg = 'importCase Failed - Invalid plan: ' + plan
        if verbose:
            print(msg)
        raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
    elif state not in config_values[carrier][product]['states']:
        msg = 'importCase Failed - Invalid State "' + state + '") for product: "' + product + '".'
        if verbose:
            print(msg)
        raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
    else:
        if verbose:
            print('Calling to createXML(carrier, product, state, plan, verbose)...')

        try:
            file_full_path = createXML(carrier, product, state, plan, verbose)
            if verbose:
                print('file_full_path:', file_full_path)
        except createXMLException as e:
            if verbose:
                print('Function createXML() failed...')
            msg = 'Function createXML() failed. More Details:' + repr(e)
            if verbose:
                print(msg)
            raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

        current_window = driver.current_window_handle

        if verbose:
            print('current_window:', current_window)

        try:
            if verbose:
                print("Call to caseAction('','Import',verbose)")
            caseAction(driver, '', 'Import', verbose)
        except IgoCommonException as e:
            if verbose:
                print('Call to caseAction failed...')
            msg = 'Call to caseAction failed. More Details:' + repr(e)
            if verbose:
                print(msg)
            raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

        try:
            file_imported = False
            for winHandle in driver.window_handles:
                try:
                    driver.switch_to.window(winHandle)
                    if verbose:
                        print('winHandle', winHandle)
                        print('Windows title:', driver.title)
                except NoSuchWindowException as e:
                    if verbose:
                        print('Failed to switch to import window handle. More Details:' + repr(e))
                    msg = 'Failed to switch to import window handle. More Details:' + repr(e)
                    if verbose:
                        print(msg)
                    raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

                if driver.title =='Import Case':
                    try:
                        if verbose:
                            print('Setting file path in Pop up.')
                        elem = WebDriverWait(driver,30).until(lambda x: x.find_element_by_id("ClientFile"))
                        elem.send_keys(file_full_path)

                        if verbose:
                            print('Submiting Import Case in Pop up.')
                        driver.find_element_by_id("Submit1").click()
                        file_imported = True
                        break
                    except TimeoutException as e:
                        if verbose:
                            print('Import windows never displayed. More details:' + repr(e))
                        msg = 'Import windows never displayed. More details:' + repr(e)
                        if verbose:
                            print(msg)
                        raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

            if verbose:
                print('Switching back to main window.')
            driver.switch_to.window(current_window)

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
                    if driver.find_elements_by_link_text(case_name):
                        if verbose:
                            print('Case Name: '+case_name+ ' found in "View My Cases"- Import Case Finished successfully.')
                            print('Importing case - Finished successfully.')
                    else:
                        if verbose:
                            print('Import case - Failed. The case is not listed in the "View My Cases" screen.')
                        msg = 'Unkonw error. Case was not imported. The case is not listed in ' +\
                              'the "View My Cases" screen.'
                        if verbose:
                            print(msg)
                        raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

                except (WebDriverException, NoSuchElementException) as e:
                    if verbose:
                        print('Impot Case - Failed. find_elements_by_link_text failed for case name:' + case_name)
                    msg = 'Impot Case - Failed. find_elements_by_link_text failed for case name:' + case_name
                    if verbose:
                        print(msg)
                    raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
            else:
                if verbose:
                    print('File Impot pop up windows never displayed. Faled to import file.')
                msg = 'File Impot pop up windows never displayed. Faled to import file.'
                if verbose:
                    print(msg)
                raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

        except Exception as e:
            if verbose:
                print('Import Case - Unhandle exception.')
            msg = 'Import Case - Unhandle exception.'
            if verbose:
                print(msg)
            raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)


def deleteCase(driver, case_name, verbose):
    ####################################################################################
    #                                  deleteCase                                      #
    ####################################################################################
    # This fuction allows the script to delete an application case in iGo for a        #
    # specific carrier like Bankers, JH, Anico, MetLife, etc.                          #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #
    #            or Google Chorme.                                                     #
    # 2) case_name: It is the aplication name e.g.: "LastName, FirstName".             #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) carrier not listed in config_values['carriers']                               #
    # 2) environment not listed in config_values[carrier]['environments']              #
    # 3) Selenium NoSuchElementException Exception                                     #
    # 4) Unknown Exception                                                             #
    #                                                                                  #
    ####################################################################################
    try:
        if verbose:
            print("Call to caseAction(case_name,'Delete',verbose)")
        caseAction(driver, case_name, 'Delete', verbose)
    except IgoCaseNotFound as e:
        if verbose:
            print('Case Name "' + case_name +'" was not found...')
        raise IgoCaseDeleteException('Case Name "' + case_name + '" was not found. More Details:' + str(e))
    except IgoCaseActionException as e:
        if verbose:
            print('Call to caseAction failed...')
        raise IgoCaseDeleteException('Call to caseAction failed. More Details:' + str(e))

    try:
        if verbose:
            print('Waiting for the Alert to pop up...')
        WebDriverWait(driver, 30).until(EC.alert_is_present())
    except TimeoutException as e:
        if verbose:
            print('Alert never pop up...')
        raise IgoCaseDeleteException('Alert never pop up. More Details:' + str(e))

    try:
        if verbose:
            print('Delete alert was found')
            print('Switching focus to Alert.')

        alert = driver.switch_to.alert

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
        WebDriverWait(driver, 30).until(EC.alert_is_present())
    except TimeoutException as e:
        if verbose:
            print('Alert never pop up...')
        raise IgoCaseDeleteException('Confirmation Delete alert never pop up. More Details:' + str(e))

    try:
        if verbose:
            print('Confirmation Delete alert was found')
            print('Switching focus to Confirmation Delete alert pop up.')

        alert = driver.switch_to.alert

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

# def exportCase(driver, product, case_name, verbose=False):

#     if verbose:
#         print('starting exportCase process...')
#         print('Case Name: ' + case_name)

#     try:
#         if verbose:
#             print("Call to caseAction(case_name,'Export',verbose)")
#         caseAction(driver, case_name, 'Export', verbose)
#     except IgoCaseNotFound as e:
#         if verbose:
#             print('Case Name "' + case_name + '" was not found...')
#         raise IgoCaseExportxception('Case Name "' + case_name + '" was not found. More Details:' + str(e))
#     except IgoCaseActionException as e:
#         if verbose:
#             print('Call to caseAction failed...')
#         raise IgoCaseExportxception('Call to caseAction failed. More Details:' + str(e))

#     current_window = driver.current_window_handle

#     if verbose:
#         print('Current windows: ' + current_window)

#     file_full_path = config_values[carrier]['base_path'] + \
#                      config_values[carrier][product]['product_path'] + \
#                      config_values[carrier][product]['xml_export_path'] + \
#                      case_name + '.xml'

#     if verbose:
#         print('file_full_path: ' + file_full_path)

#     try:
#         for winHandle in driver.window_handles:
#             try:
#                 driver.switch_to.window(winHandle)
#                 if verbose:
#                     print('winHandle', winHandle)
#                     print('Windows title:', driver.title)
#             except NoSuchWindowException as e:
#                 if verbose:
#                     print('Failed to switch to import window handle. More Details:' + str(e))
#                 raise IgoCaseExportxception('Failed to switch to import window handle. More Details:' + str(e))

#             if driver.title == 'Export Case':
#                 if verbose:
#                     print('Switched to Export pop up correctly.')
#                     print('Downloading the case XML to the following path: ' + file_full_path)

#                 # TODO: Save File
#                 e = driver.find_element_by_tag_name('a')

#                 if verbose:
#                     print('Element ID:' + e.id)
#                     print('Element Text:' + e.text)
#                     print('Element Attribute "href":' + e.get_attribute('href'))

#                 try:
#                     rightClickSaveLinkAs(driver, e, verbose)
#                     if verbose:
#                         print('Window "Save As..." opened successfully.')

#                 except Exception as e:
#                     raise IgoCaseExportxception('Failed to open windows "Save As..." window. More Details:' + str(e))

#                 try:
#                     # time.sleep(3)
#                     # win = WindowFinder()
#                     # win.find_window_wildcard(config_browsers[getBrowserType(driver)]['saveWindow'])
#                     # win.set_foreground()
#                     # ent = "{ENTER}"                   # Enter key stroke.
#                     # SendKeys(file_full_path)          # Use SendKeys to send path string to Save As dialog
#                     # SendKeys(ent)                     # Use SendKeys to send ENTER key stroke to Save As dialog
#                     pass
#                 except Exception as e:
#                     raise IgoCaseExportxception('Failed to interact to windows "Save As..." window. More Details:' + str(e))

#                 if verbose:
#                     print('File downloaded successfully.')
#                 break

#         if verbose:
#             print('Switching back to main window...')
#         driver.switch_to.window(current_window)

#     except Exception as e:
#         if verbose:
#             print('Import Case - Unhandle exception.')
#         raise IgoCaseExportxception('Import Case - Unhandle exception.')

def openCase(driver, case_name, verbose=False):
    ####################################################################################
    #                                  importCase                                      #
    ####################################################################################
    # This fuction allows the script to import an application case (xml) in iGo for a  #
    # specific carrier like Bankers, JH, Anico, MetLife, etc.                          #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #
    #            or Google Chorme.                                                     #
    # 2) Carrier: Sets the carrier for the application case that would be created,     #
    #             e.g.: Bankers, Lincol, MetLife. The value must match one of the      #
    #             config_values['carriers'] entries.                                   #
    # 3) Product: Sets the product that would be used to create the applciation case.  #
    #             This value should match one of the                                   #
    #             config_values[carrier]['prodcuts'] entries.                          #
    # 4) State: Sets the state for the application case e.g.: AL, AK, NY, etc. The     #
    #           value must match one of the config_values[carrier]['states'] entries   #
    # 5) Plan:  Sets the plan for the application case. e.g.: LA02P, 19E, 20E, etc.    #
    #           This value must match one of the config_values[carrier]['plans']       #
    #           entries.                                                               #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) carrier not listed in config_values['carriers']                               #
    # 2) environment not listed in config_values[carrier]['environments']              #
    # 3) Selenium NoSuchElementException Exception                                     #
    # 4) Unknown Exception                                                             #
    #                                                                                  #
    ####################################################################################
    if verbose:
        print('starting openCase process...')
        print('Case Name: ' + case_name)

    try:
        if verbose:
            print("Call to caseAction(case_name,'OpenCase',verbose)")
        caseAction(driver, case_name, 'OpenCase', verbose)
    except IgoCaseNotFound as e:
        if verbose:
            print('Case Name "' + case_name + '" was not found...')
        raise IgoCaseOpenException('Case Name "' + case_name + '" was not found. More Details:' + str(e))
    except IgoCaseActionException as e:
        if verbose:
            print('Call to caseAction failed...')
        raise IgoCaseOpenException('Call to caseAction failed. More Details:' + str(e))

    try:
        if verbose:
            print('Waiting for case "Case Information" screen to be loaded...')
        WebDriverWait(driver, 30).until(lambda x: x.find_element_by_id("header_client_name"))
        if verbose:
            print('finished openCase process...')
    except TimeoutException as e:
        if verbose:
            print('Failed to load "Case Information" screen for case name: ' + case_name + '. More Details: ' + str(e))
        raise IgoCaseOpenException('Failed to load "Case Information" screen for case name: ' + case_name + '. More Details: ' + str(e))


class IgoCommonException(Exception):
    """IgoCommonException raised for errors in the iGo Common prodecures.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, fuctionName, parameters, messageDetails):
        self.fuctionName = fuctionName
        self.parameters = parameters
        self.messageDetails = messageDetails

    def printParameters(self):
        output = ''
        if self.parameters:
            for entry in self.parameters:
                output += '\t' + str(entry[0]) + ': ' + str(entry[1]) + ',' + '\n'
            return output
        return '\t' + 'None.' + '\n'

    def __str__(self):
        return 'EXCEPTION PROCEDURE => ' + self.fuctionName + '\n' +\
               'Input Parameters: ' + '\n' +\
                printParameters() +\
               'Message Detail: ' + self.messageDetails


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
