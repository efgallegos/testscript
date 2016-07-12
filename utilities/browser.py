"""Create an webdriver browser"""

import platform
import logging
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


# create logger with __name__
logger = logging.getLogger('igo.utilities.browser')
# logger.setLevel(logging.DEBUG)
# # create console handler
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# # create file handler
# fh = logging.FileHandler('run_bankers.log')
# fh.setLevel(logging.DEBUG)
# # create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# # add the handler to the logger
# logger.addHandler(ch)
# logger.addHandler(fh)

# List of available browser to be use by the scripts.
config_browsers = {
    'Firefox':
        {'name': 'Firefox',
         'rightClickSaveLinkAs': 5,
         'saveWindow': '.*save to.*',
         'openWindow': '.*Open File.*',
         'extension_path': {
                            'Darwin': '/Users/efgallegos/GitHub/testscript/executables/',
                            'Windows': 'C:/zz_EFG/GitHub/testscript/executables/'
                    }
         },
    'Chrome':
        {'name': 'Chrome',
         'rightClickSaveLinkAs': 4,
         'saveWindow': '.*Save As.*',
         'openWindow': '.*Open.*',
         'Darwin': '/Users/efgallegos/Dropbox/GitHub/testscript/executables/chromedriver',
         'Windows': 'C:/zz_EFG/GitHub/testscript/executables/chromedriver.exe'},
    'IE':
        {'name': 'Internet Explorer',
         'rightClickSaveLinkAs': 4,
         'saveWindow': '.*Save As.*',
         'openWindow': '.*Open.*',
         'Windows': 'C:/zz_EFG/GitHub/testscript/executables/IEDriverServer.exe'},
    }


def getWebDriver(browser_name, proxy=False, implicit_wait_seconds=0, verbose=False):
    logger.info('getWebDriver -> "getWebDriver" procedure started...')
    logger.debug('getWebDriver -> Parameters: ')
    logger.debug('getWebDriver -> \t"browser_name": ' + browser_name)
    logger.debug('getWebDriver -> \t"proxy": ' + str(proxy))
    logger.debug('getWebDriver -> \t"inplicit_wait_second": ' + str(implicit_wait_seconds))

    proxy_host = 'localhost:9100'
    if proxy:
        logger.debug('getWebDriver -> \t"proxy_host": ' + proxy_host)
    os_name = platform.system()
    logger.debug('getWebDriver -> \t"Platform": ' + os_name)

    try:
        if proxy:
            if browser_name == "Chrome":
                caps = DesiredCapabilities.CHROME
            elif browser_name == "IE":
                caps = DesiredCapabilities.INTERNETEXPLORER
                caps['ignoreProtectedModeSettings'] = True
            else:
                caps = DesiredCapabilities.FIREFOX

            caps['proxy'] = {"httpProxy": proxy_host,
                             "ftpProxy": proxy_host,
                             "sslProxy": proxy_host,
                             "noProxy": None,
                             "proxyType": "MANUAL",
                             "class": "org.openqa.selenium.Proxy",
                             "autodetect": False}

            if browser_name == 'Chrome':
                driver = webdriver.Chrome(config_browsers[browser_name][os_name], capabilities=caps)
            elif browser_name == 'IE':
                if os_name != "Darwin":
                    # driver = webdriver.Remote(command_executor='http://10.211.55.4:4444/wd/hub', desired_capabilities=caps)
                    # else:
                    driver = webdriver.Ie(config_browsers[browser_name][os_name], capabilities=caps)

            else:
                driver = webdriver.Firefox(capabilities=caps)
        else:
            if browser_name == 'Chrome':
                print(os_name)
                driver = webdriver.Chrome(config_browsers[browser_name][os_name])
            elif browser_name == 'IE' and os_name != "Darwin":
                caps = DesiredCapabilities.INTERNETEXPLORER
                caps['ignoreProtectedModeSettings'] = True
                #if os_name != "Darwin":
                    # driver = webdriver.Remote(command_executor='http://10.211.55.4:4444/wd/hub', desired_capabilities=caps)
                    # else:
                driver = webdriver.Ie(config_browsers[browser_name][os_name], capabilities=caps)
            else:
                browser_name = 'Firefox'
                profile = FirefoxProfile()
                profile.add_extension(config_browsers[browser_name]['extension_path'][os_name] + 'firebug-2.0.16-fx.xpi')
                driver = webdriver.Firefox(firefox_profile=profile)

        #driver.maximize_window()
        driver.implicitly_wait(implicit_wait_seconds)
        logger.info('getWebDriver -> Driver was created successfully')
        return driver

    except Exception as e:
        logger.error('getWebDriver -> Unknown exception. More details: ' + repr(e))
        raise BrowserException(repr(e))


def getBrowserType(driver, verbose=False):
    """returs the name of the active webdriver browser"""

    if isinstance(driver, webdriver.Firefox):
        if verbose:
            print('Browser: Firefox')
        return config_browsers['Firefox']['name']
    elif isinstance(driver, webdriver.Chrome):
        if verbose:
            print('Browser: Chrome')
        return config_browsers['Chrome']['name']
    elif isinstance(driver, webdriver.Ie):
        if verbose:
            print('Browser: IE')
        return config_browsers['IE']['name']
    else:
        return 'Invalid'


def rightClickSaveLinkAs(driver, e, verbose=False):
    """Right Click - Save Link function"""

    if verbose:
        print('Starting rightClickSaveLinkAs proces...')
    browser = getBrowserType(driver, verbose)
    if browser != 'Invalid':
        actions = ActionChains(driver)
        actions.move_to_element(e)
        if verbose:
            print('move to move_to_element...')
        actions.context_click(e)
        if verbose:
            print('right click on element...')
        for i in range(0, config_browsers[browser]['rightClickSaveLinkAs']):
            actions.send_keys(Keys.ARROW_DOWN)
            if verbose:
                print('moving down on the context menu')
        if verbose:
            print('doing clic in "Save Link As..." option...')
        actions.send_keys(Keys.RETURN)
        actions.perform()
    else:
        raise Exception("Invalid Webdriver Browser.")
###
# WebElement elementOpen = driver.findElement(By.linkText("Open")); /*This will select menu after right click */
#
# elementOpen.click();
###



class BrowserException(Exception):

    def __init__(self, value):
        self.value = '"Get Browser Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)
