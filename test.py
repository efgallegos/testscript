"""Test File"""

from igo.igo_common import *
from utilities.browser import getWebDriver
import logging

# create logger with __name__
logger = logging.getLogger('testscript')
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create file handler
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(ch)

try:
    driver = getWebDriver('IE', verbose=True)
    logIn(driver, 'bankers', 'qd3', 'Eduardo', 'Eduardo1', verbose=True)
    
    states = ['AR']
    logger.debug('testscript -> start process')
    logger.debug('testscript -> list of states:' + str(states))
    
    for state in states:
        viewMyCases(driver)
        importCase(driver, 'bankers','annuity', state, 'LA07G_GLIA_NQ', verbose=True)
    logOut(driver, verbose=True)
except Exception as e:
    print('Exception: ' + str(e))
finally:
    driver.quit()
