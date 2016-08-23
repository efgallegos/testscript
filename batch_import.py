import sys
import logging
import logging.handlers
from datetime import datetime
from utilities.browser import config_browsers, getWebDriver
from igo.igo_common import logIn, viewMyCases, importCase, logOut
from config_entries import config_values

LOG_FILENAME = 'batch_import_bankers.log'

# create logger with __name__
logger = logging.getLogger('testscript')
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create file handler
fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1018576*5, backupCount=7)
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handler to the logger
logger.addHandler(ch)
logger.addHandler(fh)

def batch_import(arguments):
    ####################################################################################
    #                                 batch_import                                     #
    ####################################################################################
    # This fuctions allows to create Appliction cases in IGO in batch mode, which will #
    # allow the testers to speed up the testing.                                       #
    #                                                                                  #
    # The Carriers/Products must be configured in order to allow the batch fuction to  #
    # craete the Application cases.                                                    #
    #                                                                                  #
    # Paremeters:                                                                      #
    # 1) Browser: Specify the webdriver used to run the selenium script: IE, Firefox   #
    #              or Google Chorme.                                                   #
    # 2) Carrier: Sets the carrier for the application case that would be created,     #
    #             e.g.: Bankers, Lincol, MetLife. The value must match one of the      #
    #             config_values['carriers'] entries.                                   #
    # 3) Environment: Sets one of the QA or UAT environments e.g.: QD3, QD4, TD1, TD3. #
    # 4) Product: Sets the product that would be used to create the applciation case.  #
    #             This value should match one of the                                   #
    #             config_values[carrier]['prodcuts'] entries.                          #
    # 5) State: Sets the state for the application case e.g.: AL, AK, NY, etc. The     #
    #           value must match one of the config_values[carrier]['states'] entries   #
    # 6) Plan:  Sets the plan for the application case. e.g.: LA02P, 19E, 20E, etc.    #
    #           This value must match one of the config_values[carrier]['plans']       #
    #           entries.                                                               #
    ####################################################################################

    # start time counter to track the script duration.
    start_time = datetime.now()

    logger.info("batch_import -> ################################################################################")
    logger.info('batch_import -> Start time:' +  str(start_time))
    logger.info("batch_import -> Parameters list:")
    logger.info("batch_import -> \tAction: Import Case")

    # Validate the number of parameters
    if len(arguments) != 8:
        # logger.debuging exception for LOG
        logger.info("batch_import -> --------------------------------------------------------------------------------")
        logger.error('batch_import -> Error: Expecting 8 argmunets. Found: ' + str(len(arguments)))
        # Exiting batch with status failed.
        sys.exit(1)

    logger.info("batch_import -> \tBrowser: " + arguments[0])
    logger.info("batch_import -> \tCarrier: " + arguments[1])
    logger.info("batch_import -> \tEnvironment: " + arguments[2])
    logger.info("batch_import -> \tUser: " + arguments[3])
    logger.info("batch_import -> \tPass: " + arguments[4])
    logger.info("batch_import -> \tProduct: " + arguments[5])
    logger.info("batch_import -> \tState: " + arguments[6])
    logger.info("batch_import -> \tPlan: " + arguments[7])
    logger.info("batch_import -> --------------------------------------------------------------------------------")

    # Validate the browser parameter to match on of the valid browser: IE, Frifox, Chrome
    if arguments[0] in config_browsers:
        browser = arguments[0]
    else:
        # logger.debuging exception for LOG
        logger.error('batch_import -> Invalid Browser: ' + arguments[0])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the carrier parameter to match on of the valid carriers.
    if arguments[1] in config_values['carriers']:
        carrier = arguments[1]
    else:
        # logger.debuging exception for LOG
        logger.error('batch_import -> Invalid Carrier: ' + arguments[1])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the environment parameter to match on of the valid environments.
    if arguments[2] in config_values[carrier]['environments']:
        environment = arguments[2]
    else:
        # logger.debuging exception for LOG
        logger.error('batch_import -> Invalid Environment: ' + arguments[2])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the user parameter to match on of the valid users for that Carrier and Environment.
    if arguments[3] in config_values[carrier]['users'][environment[0:2] +'-user-list']:
        username = arguments[3]
    else:
        # logger.debuging exception for LOG
        logger.error('batch_import -> Invalid User: ' + arguments[3])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the password parameter to not be null/empty
    if len(arguments[4]) > 0:
        password = arguments[4]
    else:
        # logger.debuging exception for LOG
        logger.error("batch_import -> Passowrd can't be empty.")
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the product parameter to match on of the valid products.
    if arguments[5] in config_values[carrier]['products']:
        product = arguments[5]
    else:
        # logger.debuging exception for LOG
        logger.error('batch_import -> Invalid Product: ' + arguments[5])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the state parameter to match on of the valid states.
    if arguments[6].upper() in config_values[carrier][product]['states']:
        state = arguments[6].upper()
    else:
        # logger.debuging exception for LOG
        logger.error('batch_import -> Invalid State for Product - ' + \
              config_values[carrier][product]['name'] + \
              ': ' + arguments[6].upper())
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the plan parameter to match on of the valid plans.
    if arguments[7] in config_values[carrier][product]['states'][state]['plans']:
        plan = arguments[7]
    else:
        # logger.debuging exception for LOG
        logger.error('batch_import -> Invalid Plan for Product - ' + \
              config_values[carrier][product]['name'] + \
              ': ' + arguments[7])
        # Exiting batch with status failed.
        sys.exit(1)

    # Starts script execution
    try:
        logger.info('batch_import -> Call to "getWebDriver(' + browser + ') procedure')
        driver = getWebDriver(browser)
        logger.info('batch_import -> Call to "logIn(driver, ' + environment + ', ' + username + ', ' + password + ') procedure')
        logIn(driver, carrier, environment, username, password)
        logger.info('batch_import -> Call to "viewMyCases(driver) procedure')
        viewMyCases(driver)
        logger.info('batch_import -> Call to "importCase(driver, ' + carrier + ', ' + product + ', ' + state + ', ' + plan + ') procedure')
        importCase(driver, carrier, product, state, plan)
        logger.info('batch_import -> Call to logOut(driver) procedure')
        logOut(driver)
        logger.info('batch_import -> End time:' + str(datetime.now()))
        logger.info('batch_import -> Execution time:' + str(datetime.now()-start_time))

    except Exception as e:
        # An exception was catch in the script
        # logger.debuging exception for LOG
        logger.error(str(e))
        # Exiting batch with status failed.
        sys.exit(1)
    finally:
        logger.info('batch_import -> driver quit()')
        driver.quit()
        logger.info('batch_import -> ################################################################################')

if __name__ == "__main__":
    batch_import(sys.argv[1:])
