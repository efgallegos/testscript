"""Util file"""

# import win32gui,win32com.client
# import re
from .browser import config_browsers, webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


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

"""
class WindowFinder:
    """"Class to find and make focus on a particular Native OS dialog/Window """"

    def __init__ (self):
        self._handle = None

    def print_win(self):
        print('win_handle:' + str(self._handle))

    def find_window(self, class_name, window_name = None):
        """"""Pass a window class name & window name directly if known to get the window """""""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Call back func which checks each open window and matches the name of window using reg ex'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """"""" This function takes a string as input and calls EnumWindows to enumerate through all open windows """"""

        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """"Get the focus on the desired open window""""
        self.print_win()
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self._handle)


def SendKeys(input,verbose=False):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys(input, 0) # 1 für Pause = true 0 für nein

"""
