"""Create an webdriver browser"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import platform

# List of available browser to be use by the scripts.

config_browsers = {
    'Firefox':
        {'name': 'Firefox',
         'rightClickSaveLinkAs': 5,
         'saveWindow': '.*save to.*',
         'openWindow': '.*Open File.*'},
    'Chrome':
        {'name': 'Chrome',
         'rightClickSaveLinkAs': 4,
         'saveWindow': '.*Save As.*',
         'openWindow': '.*Open.*',
         'Darwin': '/Users/efgallegos/Dropbox/GitHub/testscript/executables/chromedriver',
         'Windows': 'C:/zz_EFG/Dropbox/GitHub/testscript/executables/chromedriver.exe'},
    'IE':
        {'name': 'Internet Explorer',
         'rightClickSaveLinkAs': 4,
         'saveWindow': '.*Save As.*',
         'openWindow': '.*Open.*',
         'Windows': 'C:/zz_EFG/Dropbox/GitHub/testscript/executables/IEDriverServer.exe'},
    }


class Browser():

    """ DocString for Browser"""

    # Default Proxy setttings to be use by the SHH Tunel

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
                    driver = webdriver.Firefox()
            driver.maximize_window()
            driver.implicitly_wait(30)

            if verbose:
                print('Driver was created successfully')
            return driver
        except Exception as e:
            raise BrowserException(str(e))


class BrowserException(Exception):

    def __init__(self, value):
        self.value = '"Get Browser Exception" - Details:' + value

    def __str__(self):
        return repr(self.value)
