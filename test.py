"""Test File"""

from utils.browser import getWebDriver, BrowserException
# from igo_xml import createXML ,createXMLException
from igo.igo_common import *

try:
    driver = getWebDriver('Firefox', verbose=True)
    logIn(driver, 'bankers', 'qd5', verbose=True)
    viewMyCases(driver, verbose=True)
    # search(driver, 'CB', verbose=True)
    # igo.viewCaseForms(driver, 'SPWL, ME_F2F',verbose=True)
    # importCase(driver, 'bankers','fuwl', 'tn', '19E', verbose=True)
    # igo.exportCase(driver,'spwl', 'SPWL, ME_F2F', verbose=True)
    # igo.deleteCase(driver,'Annuity, CA_LA02P',verbose=True)  # LastName, FirstName
    logOut(driver, verbose=True)
except (BrowserException, IgoCaseImportException,
        IgoLogInException, InvalidProductPlanState,
        IgoCaseDeleteException) as e:
    print('Exception: ' + str(e))
finally:
    driver.quit()
