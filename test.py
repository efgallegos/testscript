"""Test File"""

from igo.igo_common import *
from utilities.browser import getWebDriver

try:
    driver = getWebDriver('IE', verbose=True)
    logIn(driver, 'bankers', 'qd3', 'tombqd5', 'password1', verbose=True)
    viewMyCases(driver, verbose=True)

    states = ['AR','CO','DE','DC','FL','GA','HI','ID','IL','KS','KY','LA','ME','MD','MA','MN','MS','MO','MT','NE','NV','NH','NJ','NM','ND','OK','OR','RI','SC','SD','TN','UT','VT','VA','WV','WI','WY']
    print('start process')
    print('list of states:' + str(states))
    
    for state in states:
        try:
            importCase(driver, 'bankers','annuity', state, 'LA07G_GLIA_Q', verbose=True)
        except Exception as e:
            print('State: ' + state + ', plan: LA07G_GLIA_Q --> FAILED')
        print('State: ' + state + ', plan: LA07G_GLIA_Q --> PASSED')
        try:
            importCase(driver, 'bankers','annuity', state, 'LA07G_GLIA_NQ', verbose=True)
        except Exception as e:
            print('State: ' + state + ', plan: LA07G_GLIA_NQ --> FAILED')
        print('State: ' + state + ', plan: LA07G_GLIA_NQ --> PASSED')
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
