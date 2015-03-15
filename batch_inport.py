import sys
from utils.browser import Browser, config_browsers, BrowserException
from igo.igo_common import (IGO,
                            IgoLogInException,
                            IgoCaseImportException,
                            InvalidProductPlanState)
from config_entries import config_values


def batch_inport(arguments):
    print("################################################################################")
    print("Parameters:")
    print("Browser: ", arguments[0])
    print("Environment: ", arguments[1])
    print("Product: ", arguments[2])
    print("State: ", arguments[3])
    print("Plan: ", arguments[4])
    print("################################################################################")
    
    if len(arguments) != 5:
        print('error, no hay 5 argumentos')
        sys.exit(1)

    if arguments[0] in config_browsers:
        b = arguments[0]
    else:
        print('Invalid Browser: ' + arguments[0])
        sys.exit(1)

    if arguments[1] in config_values:
        environment = arguments[1]
    else:
        print('Invalid Environment: ' + arguments[1])
        sys.exit(1)

    if arguments[2] in config_values['products']:
        product = arguments[2]
    else:
        print('Invalid Product: ' + arguments[2])
        sys.exit(1)

    if arguments[3] in config_values[product]['states']:
        state = arguments[3]
    else:
        print('Invalid State for Product - ' + \
              config_values[product]['name'] + \
              ': ' + arguments[3])
        sys.exit(1)

    if arguments[4] in config_values[product]['plans']:
        plan = arguments[4]
    else:
        print('Invalid Plan for Product - ' + \
              config_values[product]['name'] + \
              ': ' + arguments[4])
        sys.exit(1)

    try:        
        driver = Browser.getWebDriver(b)
        print('driver ' + b + ' created successfully.')
        iGo = IGO(driver)
        print('IGO class instanced correctly.')
        iGo.logIn(environment)
        print('logIn to ' + environment + ' successfully.')
        iGo.viewMyCases()
        print('"View My Cases" screen displayed successfully.')
        print('Import Case -> PROCESS STARTED...')
        print('PRODUCT: ' + product)
        print('STATE: ' + state)
        print('PLAN: ' + plan)
        iGo.importCase(product, state, plan, verbose=True)
        print('Import Case -> PROCESS COMPLETED...')
        iGo.logOut()
        print('logOut from ' + environment + ' successfully')
        print('################################################################################')
    except (BrowserException,
            IgoCaseImportException,
            IgoLogInException,
            InvalidProductPlanState,
            Exception) as e:
        print(str(e))
        sys.exit(1)
    finally:            
        driver.quit()
        print('driver quit()')

if __name__ == "__main__":
    batch_inport(sys.argv[1:])
