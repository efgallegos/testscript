"""Test File"""

from igo.igo_common import importCase, viewMyCases, logIn, logOut
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

    driver = getWebDriver('Firefox', verbose=True)
    logIn(driver, 'bankers', 'qd4', 'Eduardo', 'Eduardo1', verbose=True)
    
    states = ['AK']
    logger.debug('testscript -> start process')
    logger.debug('testscript -> list of states:' + str(states))
    
    for state in states:
        viewMyCases(driver)
        if state == 'NY':
            importCase(driver, 'bankers','annuity', state, 'BLNY-LA-06T', verbose=True)
        else:
            importCase(driver, 'bankers','cb', state, 'GR-G220', verbose=True)
        
        # try:
        #     logger.info('batch_lock_case -> Starting work for state: ' + state)
        #     viewMyCases(driver)
        #     case_name = config_values['bankers']['annuity']['name'] + ', ' + state + '_' + 'LA07G_PBIA'
        #     logger.info('batch_lock_case -> Call to "search(driver, ' + case_name+ ') procedure')
        #     search(driver, case_name)
        #     logger.info('batch_lock_case -> Call to "lockCase(driver, ' + case_name+ ') procedure')
        #     lockCase(driver, case_name)
        # except Exception as e:
        #     print('Case "' + case_name + '" failed. Exception: ' + str(e))        
    
    logOut(driver, verbose=True)
except Exception as e:
    print('Exception: ' + str(e))
finally:
    driver.quit()
