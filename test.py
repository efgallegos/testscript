
"""Test File"""

from utils.browser import Browser, BrowserException
# from igo_xml import createXML ,createXMLException
from igo.igo_common import (IGO, IgoLogInException, IgoCaseImportException,
                        InvalidProductPlanState, IgoCaseDeleteException)

try:
    driver = Browser.getWebDriver('Firefox', verbose=True)
    igo = IGO(driver)
    igo.logIn('qd4')
    igo.viewMyCases()
    igo.search('CA_LA02P', verbose=True)
    # igo.viewCaseForms('SPWL, ME_F2F',verbose=True)
    # igo.importCase('annuity','CA','LA02P',verbose=True)
    # igo.exportCase('spwl', 'SPWL, ME_F2F', verbose=True)
    # igo.deleteCase('Annuity, CA_LA02P',verbose=True)  # LastName, FirstName
    igo.logOut()
    # createXML('spwl','AK','14W',True)
# except createXMLException as e:
except (BrowserException, IgoCaseImportException,
        IgoLogInException, InvalidProductPlanState,
        IgoCaseDeleteException) as e:
    print('Exception: ' + str(e))
finally:
    driver.quit()
