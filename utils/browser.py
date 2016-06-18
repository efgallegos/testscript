"""Create an webdriver browser"""

import platform
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

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


def getWebDriver(browser_name, proxy=False, verbose=False):
    proxy_host = 'localhost:9100'
    os_name = platform.system()

    if verbose:
        print('Broswer:', browser_name,
              ', os_name: ', os_name,
              ', Proxy:', proxy)
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
            elif browser_name == 'IE':
                caps = DesiredCapabilities.INTERNETEXPLORER
                caps['ignoreProtectedModeSettings'] = True
                if os_name != "Darwin":
                    # driver = webdriver.Remote(command_executor='http://10.211.55.4:4444/wd/hub', desired_capabilities=caps)
                    # else:
                    driver = webdriver.Ie(config_browsers[browser_name][os_name], capabilities=caps)
            else:
                profile = FirefoxProfile()
                profile.add_extension(config_browsers[browser_name]['extension_path'][os_name] + 'firebug-2.0.16-fx.xpi')
                driver = webdriver.Firefox(firefox_profile=profile)

        driver.maximize_window()
        driver.implicitly_wait(30)

        if verbose:
            print('Driver was created successfully')
        return driver
    except Exception as e:
        raise BrowserException(str(e))


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
