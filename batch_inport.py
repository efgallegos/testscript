import sys
from datetime import datetime
from utils.browser import *
from igo.igo_common import *
from config_entries import config_values


def batch_inport(arguments):
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

    # Validate the number of parameters
    if len(arguments) != 8:
        # Printing exception for LOG
        print('Error: Expecting 8 argmunets.')
        # Exiting batch with status failed.
        sys.exit(1)

    print("################################################################################")
    print('Start time:', str(start_time))
    print("Parameters list:")
    print("Browser: ", arguments[0])
    print("Carrier: ", arguments[1])
    print("Environment: ", arguments[2])
    print("User: ", arguments[3])
    print("Pass: ", arguments[4])
    print("Product: ", arguments[5])
    print("State: ", arguments[6])
    print("Plan: ", arguments[7])
    print("################################################################################")

    # Validate the browser parameter to match on of the valid browser: IE, Frifox, Chrome
    if arguments[0] in config_browsers:
        browser = arguments[0]
    else:
        # Printing exception for LOG
        print('Invalid Browser: ' + arguments[0])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the carrier parameter to match on of the valid carriers.
    if arguments[1] in config_values['carriers']:
        carrier = arguments[1]
    else:
        # Printing exception for LOG
        print('Invalid Carrier: ' + arguments[1])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the environment parameter to match on of the valid environments.
    if arguments[2] in config_values[carrier]['environments']:
        environment = arguments[2]
    else:
        # Printing exception for LOG
        print('Invalid Environment: ' + arguments[2])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the user parameter to match on of the valid users for that Carrier and Environment.
    if arguments[3] in config_values[carrier]['users'][environment[0:2] +'-user-list']:
        username = arguments[3]
    else:
        # Printing exception for LOG
        print('Invalid User: ' + arguments[3])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the password parameter to not be null/empty
    if len(arguments[4]) > 0:
        password = arguments[4]
    else:
        # Printing exception for LOG
        print("Passowrd can't be empty.")
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the product parameter to match on of the valid products.
    if arguments[5] in config_values[carrier]['products']:
        product = arguments[5]
    else:
        # Printing exception for LOG
        print('Invalid Product: ' + arguments[5])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the state parameter to match on of the valid states.
    if arguments[6] in config_values[carrier][product]['states']:
        state = arguments[6]
    else:
        # Printing exception for LOG
        print('Invalid State for Product - ' + \
              config_values[carrier][product]['name'] + \
              ': ' + arguments[6])
        # Exiting batch with status failed.
        sys.exit(1)

    # Validate the plan parameter to match on of the valid plans.
    if arguments[7] in config_values[carrier][product]['plans']:
        plan = arguments[7]
    else:
        # Printing exception for LOG
        print('Invalid Plan for Product - ' + \
              config_values[carrier][product]['name'] + \
              ': ' + arguments[7])
        # Exiting batch with status failed.
        sys.exit(1)

    # Starts script execution
    try:
        driver = getWebDriver(browser)
        print('driver ' + browser + ' created successfully.')
        logIn(driver, carrier, environment, username, password)
        print('logIn to ' + environment + ' with user ' + username + ' successfully.')
        viewMyCases(driver)
        print('"View My Cases" screen displayed successfully.')
        print('Import Case -> PROCESS STARTED...')
        print('CARRIER: ' + carrier)
        print('PRODUCT: ' + product)
        print('STATE: ' + state)
        print('PLAN: ' + plan)
        importCase(driver, carrier, product, state, plan, verbose=True)
        print('Import Case -> PROCESS COMPLETED...')
        logOut(driver, verbose=True)
        print('logOut from ' + environment + ' successfully')
        print('End time:', str(datetime.now()))
        print('Execution time:', str(datetime.now()-start_time))
        print('################################################################################')
    except (BrowserException,
            IgoCaseImportException,
            IgoLogInException,
            InvalidProductPlanState,
            Exception) as e:
        # An exception was catch in the script
        # Printing exception for LOG
        print(str(e))
        # Exiting batch with status failed.
        sys.exit(1)
    finally:
        driver.quit()
        print('driver quit()')

if __name__ == "__main__":
    batch_inport(sys.argv[1:])
