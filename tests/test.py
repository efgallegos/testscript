"""Test File"""

from igo.igo_common import *
from utilities.browser import getWebDriver

def main():
    try:
        driver = getWebDriver('IE', verbose=True)
        logIn(driver, 'bankers', 'qd3', verbose=True)
        viewMyCases(driver, verbose=True)
        #importCase(driver, 'bankers','medsupp', 'OK', 'MEDSUPP', verbose=True)
        #lockCase(driver,'MedSupp, OK_MEDSUPP', verbose=True)
        #search(driver, 'MedSupp, OK_MEDSUPP', verbose=True)
        # igo.viewCaseForms(driver, 'SPWL, ME_F2F',verbose=True)
        # importCase(driver, 'bankers','fuwl', 'tn', '19E', verbose=True)
        # igo.exportCase(driver,'spwl', 'SPWL, ME_F2F', verbose=True)
        # igo.deleteCase(driver,'Annuity, CA_LA02P',verbose=True)  # LastName, FirstName
        logOut(driver, verbose=True)
    except Exception as e:
        print('Exception: ' + str(e))
    finally:
        driver.quit()
