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
    #'CO','DE','DC','FL','GA','HI','ID','IL','KS','KY','LA','ME','MD','MA','MN','MS','MO','MT','NE','NM','RI','SC','SD','TN','UT','VT','VA','WV','WI','WY']
    # 'NV','NH','NJ','ND', 'AR'
    logger.debug('testscript -> start process')
    logger.debug('testscript -> list of states:' + str(states))
    
    for state in states:

        # try:
        #     viewMyCases(driver)
        #     case_name = 'Annuity, ' + state + '_LA07G_GLIA_Q'
        #     logger.debug('testscript -> case name: ' + case_name)
        #     search(driver, case_name)
        #     lockCase(driver, case_name)
        #     #importCase(driver, 'bankers','annuity', state, 'LA07G_GLIA_NQ', verbose=True)
        #     logger.debug("testscript -> 'State: " + state + ", plan: LA07G_GLIA_Q --> PASSED")
        # except Exception as e:
        #     logger.error("testscript -> 'State: " + state + ", plan: LA07G_GLIA_Q --> FAILED")
        
        # try:
        #     viewMyCases(driver)
        #     case_name = 'Annuity, ' + state + '_LA07G_GLIA_NQ'
        #     logger.debug('testscript -> case name: ' + case_name)
        #     search(driver, case_name)
        #     lockCase(driver, case_name)
        #     #importCase(driver, 'bankers','annuity', state, 'LA07G_GLIA_NQ', verbose=True)
        #     logger.error("testscript -> 'State: " + state + ", plan: LA07G_GLIA_NQ --> PASSED")
        # except Exception as e:
        #     logger.error("testscript -> 'State: " + state + ", plan: LA07G_GLIA_NQ --> FAILED")
        viewMyCases(driver)
        importCase(driver, 'bankers','annuity', state, 'LA07G_GLIA_NQ', verbose=True)
        #lockCase(driver,'MedSupp, OK_MEDSUPP', verbose=True)
        #search(driver, 'MedSupp, OK_MEDSUPP', verbose=True)
    logOut(driver, verbose=True)
except Exception as e:
    print('Exception: ' + str(e))
finally:
    driver.quit()
