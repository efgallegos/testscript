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

# import re
# import time
import logging
# from utils.browser import *
# from utils.utils import *
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (#WebDriverException,
                                        TimeoutException,
                                        NoSuchElementException,
                                        #NoSuchFrameException,
                                        NoAlertPresentException,
                                        NoSuchWindowException)
from .igo_xml import createXML, createXMLException
from config_entries import config_values

# create logger with __name__
logger = logging.getLogger('testscript.igo.igo_common')

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
    # 1) "IgoCommonException" will be raised for the following errors:                 #
    # 1.1) Action not listed in config_values['igo_common']['caseActionDropdown']      #
    # 1.2) case_name not found by iGo Search                                           #
    # 1.3) Selenium NoSuchElementException Exception                                   #
    # 1.4) Unknown Exception                                                           #
    #                                                                                  #
    ####################################################################################
    logger.info('caseAction -> "caseAction" procedure stated...')
    logger.debug('caseAction -> Parameters:')
    logger.debug('caseAction -> \t"case_name": ' + case_name)
    logger.debug('caseAction -> \t"action": ' + action)

    logger.debug('caseAction -> Validating parameters.')
    if action not in config_values['igo_common']['caseActionDropdown']:
        msg = 'Case Action: "' + action + '" is not a valid action. Please check the valid actions in the IGo Common dictionary entry "caseActionDropdown".'
        logger.error('caseAction -> ' + msg)
        raise IgoCommonException('caseAction', [('case_name',case_name),('action',action)], msg)
    logger.debug('caseAction -> Case Action value "' + action + '" is valid')
    try:
        #logger.debug('Calling "viewMyCases" procedure')
        #viewMyCases(driver, verbose=verbose)

        if action != 'Import':
            logger.debug('caseAction -> Calling "search" procedure')
            search(driver, case_name, verbose=verbose)

            logger.debug('caseAction -> Finding element: "' + case_name + '"')
            e = driver.find_element_by_link_text(case_name)
            parent = e.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
            logger.debug('caseAction -> Finding "Case Action" dropdown for element: ' + case_name)
            b = parent.find_element_by_tag_name('button')
            logger.debug('caseAction -> Expanding "Case Action" dropdown options')
            b.click()
            logger.debug('caseAction -> Clicked on the "Case Action" option: ' + action)
            b.find_element_by_xpath('..').find_element_by_link_text(config_values['igo_common']['caseActionDropdown'][action]).click()
        else:
            logger.debug('caseAction -> Selected "Import" in the "Case Action" dropdown')
            driver.find_element_by_id("pnlActions").click()
            driver.find_element_by_id("pnlActions").find_element_by_link_text(config_values['igo_common']['caseActionDropdown'][action]).click()
        logger.debug('caseAction -> "Case Action" option: ' + action + ' selected')

    except IgoCommonException as e:
        msg = 'Search Procedure failed or target was not found.' + repr(e)
        logger.error('caseAction -> ' + msg)
        raise IgoCommonException('caseAction', [('case_name',case_name),('action',action)], msg)
    except NoSuchElementException as e:
        msg = 'NoSuchElementException Selenium Exception: Element not found by the Selenium Driver. More Details: ' + repr(e)
        logger.error('caseAction -> ' + msg)
        raise IgoCommonException('caseAction', [('case_name',case_name),('action',action)], msg)
    except Exception as e:
        msg = 'Exception: An unknown Exception has occurred. More Details: ' + repr(e)
        logger.error('caseAction -> ' + msg)
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
    # 1) "IgoCommonException" will be raised for the following errors:                 #
    # 1.1) If carrier not listed in config_values['carriers']                          #
    # 1.2) environment not listed in config_values[carrier]['environments']            #
    # 1.3) Selenium NoSuchElementException Exception                                   #
    # 1.4) Unknown Exception                                                           #
    #                                                                                  #
    ####################################################################################
    logger.info('logIn -> "LogIn" procedure started...')
    logger.debug('logIn -> Parameters:')
    logger.debug('logIn -> \t"Carrier": ' +  carrier)
    logger.debug('logIn -> \t"Environment": ' + environment)
    logger.debug('logIn -> \t"Username": ' + username)
    logger.debug('logIn -> \t"Password" : ' + password)

    logger.debug('logIn -> Validating parameters.')
    if carrier not in config_values['carriers']:
        msg = 'LogIn Failed. Invalid Carrier. ' + carrier + " is not listed in config_values['carriers']"
        logger.error('logIn -> ' + msg)
        raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)
    logger.debug('logIn -> Carrier value "' + carrier + '" is valid')
    if not environment:
        logger.debug('logIn -> Using Default environment')
        environment = 'default'
    else:
        if environment not in config_values[carrier]['environments']:
            msg = 'LogIn Failed. Environment "' + environment + '"not valid for carrier "' + carrier +". Please check the config_values[carrier]['environments'] dictionary."
            logger.error('logIn -> ' + msg)
            raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)
    logger.debug('logIn -> Environment value "' + environment + '" is valid')

    base_url = config_values[carrier]['environments'][environment]
    logger.debug('logIn -> Base URL: ' + base_url)

    if not username:
        username = config_values[carrier]['users'][environment[0:2] + '-user']
        password = config_values[carrier]['users'][environment[0:2] + '-pass']
        logger.debug('logIn -> Using default environment user and password: ' + username +', ' + password)

    try:
        logger.debug('logIn -> Loading base URL: ' + base_url)
        driver.get(base_url)

        if driver.current_url.find("/CossEnterpriseSuite/") == -1:
            logger.debug('logIn -> Setting User and Password: ' + username +', ' + password)

            elem = driver.find_element_by_name("user")
            elem.clear()
            elem.send_keys(username)

            elem = driver.find_element_by_name("password")
            elem.clear()
            elem.send_keys(password)

            elem = driver.find_element_by_name("Submit")
            elem.click()

            logger.debug('logIn -> Loading "Welcome" page')
            elem = WebDriverWait(driver,30).until(lambda x: x.find_element_by_id("mycases-button"))
            logger.debug('logIn -> "Welcome" page loaded successfully')
            logger.info("logIn -> LogIn finished successfully")
        else:
            msg = 'LogIn Failed. The carrier "' + carrier + '" login screen failed to load.'
            logger.error('logIn -> ' + msg)
            raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)

    except NoSuchElementException as e:
        msg = 'LogIn Failed. NoSuchElementException Selenium Exception: Element not found by the Selenium Driver. More Details: ' + repr(e)
        logger.error('logIn -> ' + msg)
        raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)
    except TimeoutException as e:
        msg = 'LogIn Failed. TimeoutException Selenium Exception: "mycases-button" button not found. More Details: ' + repr(e)
        logger.error('logIn -> ' + msg)
        raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)
    except Exception as e:
        msg = 'LogIn Failed. An unknown Exception has occurred. More Details:' + repr(e)
        logger.error('logIn -> ' + msg)
        raise IgoCommonException('caseAction', [('carrier',carrier),('environment',environment),('username',username),('password',password)], msg)

def logOut(driver, verbose=False):
    ####################################################################################
    #                                    logOut                                        #
    ####################################################################################
    # This fuction allows the script to logout iGo for any carrier                     #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #ls
    #            or Google Chorme.                                                     #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) IgoCommonException when something failed within the webdriver.                #
    #                                                                                  #
    ####################################################################################
    logger.info('logOut -> "logOut" procedure starts...')

    try:
        if driver.find_elements_by_id('CossScreenFrame'):
            logger.debug('logOut -> Switching to windows')
            driver.switch_to_window(driver.current_window_handle)

        try:
            driver.find_element_by_id('ctrlBanner_lnkUserMenu').click()
        except Exception as e:
            driver.find_element_by_id('PageBanner1_lnkUserMenu').click()    
        logger.debug('logOut -> User options displayed')
        
        sign_out = driver.find_element_by_id("lnkSignOut")
        while True:
            if sign_out.is_displayed():
                break
        sign_out.click()
        logger.debug('logOut -> Clicking the "Sing Out" button')

        #elem = driver.find_element_by_xpath("//body[@id='documentBody']/div[9]/div/div/div/h4")
        #elem = driver.find_element_by_class_name("modal-title")

        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,"btn-log-off")));

        logout = driver.find_element_by_class_name('btn-log-off')
        while True:
            if logout.is_displayed():
                break

        # if elem.text == 'Sign Out?':
        logger.debug('logOut -> Inline Pop up was displayed.')
        #logger.debug('logOut -> Inline pop up title: ' + elem.text)
        driver.find_element_by_class_name('btn-log-off').click()
        logger.info('logOut -> Sign Out completed')
        
        #else:
        #    msg = 'Inline Pop up was not displayed'
        #    logger.error('logOut -> ' + msg)
        #    raise IgoCommonException('logOut', None, msg)
    except Exception as e:
        msg = 'LogOut Failed. An unknown exception has occured. More details: ' + repr(e)
        logger.error('logOut -> ' + msg)
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
    # 1) IgoCommonException when the View My Cases screen failed to be loaded.         #
    #                                                                                  #
    ####################################################################################
    logger.info('viewMyCases -> Navigating to "View My Cases" started...')

    try:
        if driver.find_elements_by_id('btnNewCase'):
            logger.info('viewMyCases -> Driver is already in the "View My Cases" screen')
        else:
            if driver.find_elements_by_id('mycases-button'):
                logger.debug('viewMyCases -> Driver is in the "Welcome" screen')
                driver.find_element_by_id('mycases-button').click()
            elif driver.find_elements_by_id('PageBanner1_lnkMyCasesLink'):
                logger.debug('viewMyCases -> Driver is in the "Existing Case" screen')
                driver.find_element_by_id('PageBanner1_lnkMyCasesLink').clik()
            else:
                logger.error('viewMyCases -> Driver is in an unkonwn screen.')
                msg = '"viewMyCases" procedure failed. The driver is at an unknown screen and the "View My Cases" screen can not be loaded'
                logger.error('viewMyCases -> ' + msg)
                raise IgoCommonException('viewMyCases', None, msg)

            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("btnNewCase"))
            logger.info('viewMyCases -> Navigating to "View My Cases" - Completed')

    except TimeoutException as e:
        msg = '"viewMyCases" procedure failed. The "View My Cases" screen was not loaded and a Timeout Exception took place. More datils:' + repr(e)
        logger.error('viewMyCases -> ' + msg)
        raise IgoCommonException('viewMyCases', None, msg)
    except Exception as e:
        msg = 'viewMyCases Failed. An unknown exception has occured. More datils:' + repr(e)
        logger.error('viewMyCases -> ' + msg)
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
    # 1) IgoCommonException when the View My Cases screen failed to be loaded.         #
    #                                                                                  #
    ####################################################################################
    logger.info('search -> "Search" procedure started...')
    logger.debug('search -> Parameters:')
    logger.debug('search -> \ttarget: ' + target)

    try:
        logger.debug('search -> Call to "viewMyCases" procedure')
        viewMyCases(driver, verbose)

        logger.debug('search -> Splitting target in information in First_Name and Last_Name')
        last_name = target.split(',')[0].strip()
        first_name = target.split(',')[1].strip()
        logger.debug('search -> Last_Name: ' + last_name)
        logger.debug('search -> First_Name: ' + first_name)

        logger.debug('search -> Searching by First_Name: ' + first_name)
        driver.find_element_by_id("txtSearch").clear()
        driver.find_element_by_id("txtSearch").send_keys(first_name)
        driver.find_element_by_id("btnSearch").click()

        logger.debug('search -> Checking if target "' + target + '" was found')
        if driver.find_elements_by_link_text(target):
            logger.info('search -> Target "' + target + '" was found searching by First Name.')
        else:
            logger.debug('search -> Searching by Last_Name: ' + last_name)
            driver.find_element_by_id("txtSearch").clear()
            driver.find_element_by_id("txtSearch").send_keys(last_name)
            driver.find_element_by_id("btnSearch").click()

            logger.debug('search -> Checking if target "' + target + '" was found')
            if driver.find_elements_by_link_text(target):
                logger.info('search -> Target "' + target + '" was found searching by Last Name.')
            else:
                msg = 'Search Failed - The search element was not found. More Details:'
                logger.error('search -> ' + msg)
                raise IgoCommonException('search', [('target',target)], msg)
    except NoSuchElementException as e:
        msg = 'Search Failed - Selenium NoSuchElementException error. More Details:' + repr(e)
        logger.error('search -> ' + msg)
        raise IgoCommonException('selenium', [('target',target)], msg)

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
    logger.info('importCase -> "importCase" procedure started...')
    logger.debug('importCase -> Parameters:')
    logger.debug('importCase -> \tcarrier: ' + carrier)
    logger.debug('importCase -> \tproduct: ' + product)
    logger.debug('importCase -> \tstate: ' + state)
    logger.debug('importCase -> \tplan: ' + plan)

    logger.debug('importCase -> Validating parameters.')
    if carrier not in config_values['carriers']:
        msg = 'importCase Failed - Invalid Carrier: ' + carrier
        logger.error('importCase -> ' + msg)
        raise Exception #IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
    logger.debug('Carrier value "' + carrier + '" is valid')
    if product not in config_values[carrier]['products']:
        msg = 'importCase Failed - Invalid product: ' + product
        logger.error('importCase -> ' + msg)
        raise Exception #raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
    logger.debug('Product value "' + product + '" is valid')
    state = state.upper()
    if state not in config_values[carrier][product]['states']:
        msg = 'importCase Failed - Invalid State "' + state + '") for product: "' + product + '".'
        logger.error('importCase -> ' + msg)
        raise Exception #raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
    logger.debug('importCase -> State value "' + state + '" is valid')
    if plan not in config_values[carrier][product]['states'][state]['plans']:
        msg = 'importCase Failed - Invalid plan: ' + plan
        logger.error('importCase -> ' + msg)
        raise Exception #raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
    logger.debug('Plan value "' + plan + '" is valid')
    try:
        logger.debug('importCase -> Calling to createXML(carrier, product, state, plan, verbose)...')
        file_full_path = createXML(carrier, product, state, plan, verbose)
        logger.debug('importCase -> "file_full_path" to be imported: ' + file_full_path)
    except createXMLException as e:
        msg = 'Function createXML() failed. More Details:' + repr(e)
        logger.error('importCase -> ' + msg)
        raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

    current_window = driver.current_window_handle

    logger.debug('importCase -> Current window handler: ' + current_window)

    try:
        logger.debug("importCase -> Call to caseAction('','Import',verbose)")
        caseAction(driver, '', 'Import', verbose)
    except IgoCommonException as e:
        msg = 'Call to caseAction failed. More Details:' + repr(e)
        logger.error('importCase -> ' + msg)
        raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

    try:
        file_imported = False
        for winHandle in driver.window_handles:
            try:
                driver.switch_to.window(winHandle)
                logger.debug('importCase -> Switching to window: ' + winHandle)
                logger.debug('importCase -> Windows title: ' + driver.title)
            except NoSuchWindowException as e:
                msg = 'Failed to switch to import window handle. More Details:' + repr(e)
                logger.error('importCase -> ' + msg)
                raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
            if driver.title =='Import Case':
                try:
                    logger.debug('importCase -> Setting file path in Pop up.')
                    elem = WebDriverWait(driver,30).until(lambda x: x.find_element_by_id("ClientFile"))
                    elem.send_keys(file_full_path)
                    logger.debug('importCase -> Submiting Import Case in Pop up.')
                    driver.find_element_by_id("Submit1").click()
                    file_imported = True
                    break
                except TimeoutException as e:
                    msg = 'Import windows never displayed. More details:' + repr(e)
                    logger.error('importCase -> ' + msg)
                    raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

        driver.switch_to.window(current_window)
        logger.debug('importCase -> Switching back to main window.')

        #time.sleep(10)

        if file_imported:
            logger.debug('importCase -> Current Windows: ' + current_window)
            logger.debug('importCase -> Import pop up closed.')
            logger.debug('importCase -> Checking the case in "My View Cases".')

            # case_name = "LastName, FirstName"
            case_name = config_values[carrier][product]['name'] + ', ' + state + '_' + plan
            logger.debug('importCase -> Searching for imported application case: ' + case_name)
            try:
                WebDriverWait(driver,30).until(lambda  x: x.find_element_by_link_text(case_name))
                logger.info('importCase -> "Import Case" finished successfully')
            except TimeoutException as e:
                msg = 'Import Case - Failed. Imported Case was not found.' + repr(e)
                logger.error('importCase -> ' + msg)
                raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)
        else:
            msg = 'File Impot pop up windows never displayed. Faled to import file.'
            logger.error('importCase -> ' + msg)
            raise IgoCommonException('importCase', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)

    except Exception as e:
        msg = 'Import Case - Unhandle exception.'
        logger.error('importCase -> ' + msg)
        raise IgoCommonException('selenium', [('carrier',carrier),('product',product),('state',state),('plan',plan)], msg)


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

def get_button(driver, elem_id):
    if driver.find_elements_by_id(elem_id):
        return driver.find_element_by_id(elem_id)
    else:
        # searching by alt_id
        buttons = driver.find_elements_by_tag_name('button')
        for btn in buttons:
            if btn.get_attribute('alt_id') == elem_id:
                return btn
        return None


def get_required_fields(driver):
    fields = driver.find_elements_by_class_name('is-required')
    req = []
    if fields:
        for field in fields:
            if field.is_displayed():
                req.append(field)
    return req
    #
    #elements = []
    #for _type in ['label','input','span']:
    #
    #    elements.extend(driver.find_elements_by_xpath("//"+_type+"[contains(@class, 'is-required')]"))
    #    elements.extend(driver.find_elements_by_xpath("//"+_type+"[contains(@class, 'jq-dte-is-required')]"))
    #return elements

def validate_igo_screen(driver, fields_to_process, verbose=False):
    while fields_to_process:
        for field in fields_to_process:
            if field.tag_name.lower() == 'label':
                if field.find_element_by_xpath('..').get_attribute('class').find('radio-group') != -1:
                    if field.text.upper() == 'NO':
                        field.click()
                        break
                if field.get_attribute('class').find('js-check-btn') != -1:
                    field.click()
                    break
            elif field.tag_name.lower() == 'input':
                if field.get_attribute('maxlength') != None:
                    field.send_keys('testing')
                    field.send_keys(Keys.TAB)
                    break
                if field.get_attribute('number') != None:
                    field.send_keys('1234')
                    field.send_keys(Keys.TAB)
                    break
                if field.get_attribute('currency') != None:
                    field.send_keys('12345')
                    field.send_keys(Keys.TAB)
                    break
            elif field.tag_name.lower() == 'select':
                Select(field).select_by_index(1)
                field.send_keys(Keys.TAB)

        fields_to_process = get_required_fields(driver)

def get_screen_name(driver):
    headers = driver.find_elements_by_tag_name('h1')
    while not headers:
        headers = driver.find_elements_by_tag_name('h1')
        # logger.debug('get_screen_name -> headers: ' + str(headers))
    screen_name = headers[0].text.lower().strip()
    while not screen_name:
        screen_name = headers[0].text.lower().strip()
    return screen_name

def check_screen_name(driver, screen_name):
    return get_screen_name(driver) == screen_name.lower().strip()

def lockCase(driver, case_name, verbose=False):
    ####################################################################################
    #                                  lockCase                                        #
    ####################################################################################
    # This fuction allows the script to lock an application case (xml) in iGo for a    #
    # specific carrier like Bankers, JH, Anico, MetLife, etc.                          #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) driver: webdriver used to run the selenium script: IE, Firefox                #
    #            or Google Chorme.                                                     #
    # 2) case_name: It is the full name of the case applicaiton desired to be locked.  #
    #                                                                                  #
    # Raise Exceptions:                                                                #
    # 1) carrier not listed in config_values['carriers']                               #
    # 2) product not listed in config_values[carrier]['products']                      #
    # 3) plan not in config_values[carrier][product]['plans']                          #
    # 4) state not in config_values[carrier][product]['states']                        #
    #                                                                                  #
    ####################################################################################
    logger.info('lockCase -> starting lockCase process...')
    logger.info('lockCase -> Case Name: ' + case_name)

    try:
        #import pdb;pdb.set_trace()
        logger.debug("lockCase -> Calling to procedure 'caseAction'")
        caseAction(driver, case_name, 'OpenCase', verbose)

        wh = driver.current_window_handle
        logger.debug('lockCase -> Current windows handler: ' + str(wh))

        if driver.find_element_by_id('tab0').text.lower() == 'case information' and driver.find_element_by_id('tab0').get_attribute('class').lower() == 'active':
            logger.debug('lockCase -> "Case Information" tab.')
            #Case information screen:
            if driver.find_elements_by_id('CossScreenFrame'):
                logger.debug('lockCase -> Switch to frame.')
                driver.switch_to_frame('CossScreenFrame')
                logger.debug('lockCase -> Click on selected Product-Plan option.')
                elem = driver.find_element_by_id('GridView1_ctl02_btnIgo1')
                elem.click()
                elem = WebDriverWait(driver,30).until(lambda x: x.find_element_by_xpath("//button[starts-with(@alt_id, 'btnNext')]"))
                logger.debug('lockCase -> Switch to windows: ' + str(wh))
                driver.switch_to_window(wh)
        if driver.find_element_by_id('tab1').text.lower().strip() == 'application' and driver.find_element_by_id('tab1').get_attribute('class').lower() == 'active':
            #Application:
            logger.debug('lockCase -> "Applicaiton" Tab.')
            if driver.find_elements_by_id('CossScreenFrame'):
                logger.debug('lockCase -> Switch to frame: "CossScreenFrame".')
                driver.switch_to_frame('CossScreenFrame')
            screen_name = get_screen_name(driver)
            while not screen_name == 'Forms To Be Sent to the Applicant'.lower().strip():
                logger.info('lockCase -> Current screen: ' + screen_name)
                if screen_name == 'Validate and Lock Data'.lower().strip():
                    logger.debug('lockCase -> Locking application...')
                    #btn_lock_application = get_button(driver, 'btnLock')
                    btn_lock_application = driver.find_element_by_xpath("//button[starts-with(@alt_id, 'btnLock')]")
                    btn_lock_application.click()
                    logger.info('lockCase -> Application locked.')
                elif screen_name == '':
                    logger.error('lockCase -> Missing screen name')
                    break
                else:
                    logger.debug('lockCase -> checking if requried fields exist in current screen: ' + screen_name)
                    required = get_required_fields(driver)
                    logger.debug('lockCase -> required: ' + str(required))
                    if required:
                        logger.debug('lockCase -> Missing required fields. Starting "validate_igo_screen" procedure...')
                        validate_igo_screen(driver, required)
                logger.debug('lockCase -> finding "Next" button')
                btn_next = driver.find_element_by_xpath("//button[starts-with(@alt_id, 'btnNext')]")
                logger.debug('lockCase -> clicking "Next" button.')
                btn_next.click()
                logger.info('lockCase -> "Next" button clicked.')
                screen_name = get_screen_name(driver)

            logger.debug('lockCase -> Switch to windows: ' + str(wh))
            driver.switch_to_window(wh)
        else:
            logger.error('lockCase -> "Application" tab is not active')

    except IgoCommonException as e:
        msg = 'Case Name "' + case_name + '" was not found or could not be opened to be locked'
        logger.error('lockCase -> '+ msg)
        raise IgoCommonException('lockCase', [('case_name',case_name)], msg)
    except Exception as e:
        msg = 'Unkown Exception. More Details:' + repr(e)
        logger.error('lockCase -> '+ msg)
        raise IgoCommonException('lockCase', [('case_name',case_name)], msg)


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

    def get_fuctionName(self):
        return self.fuctionName

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
                self.printParameters() +\
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

class IgoCaseExportxception(Exception):

    def __init__(self, value):
        self.value = '"Export Case Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)
