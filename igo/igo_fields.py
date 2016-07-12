import logging
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By

# create logger with __name__
logger = logging.getLogger('igo.igo_xml')
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create file handler
fh = logging.FileHandler('run_bankers.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handler to the logger
logger.addHandler(ch)
logger.addHandler(ch)

class DateIgo():
    """docstring for ClassName"""

    def __init__(self, driver, element_id):
        self.d = driver
        self.id = element_id

    def set_date(self, dob_date):
        parent = self.d.find_element_by_id(self.id)
        elem_month = parent.find_element_by_class_name('jq-dte-month')
        elem_day = parent.find_element_by_class_name('jq-dte-day')
        elem_year = parent.find_element_by_class_name('jq-dte-year')
        elem_month.clear()
        elem_month.send_keys(str(dob_date.month))
        elem_day.clear()
        elem_day.send_keys(str(dob_date.day))
        elem_year.clear()
        elem_year.send_keys(str(dob_date.year))

    def get_date(self):
        self.d.switch_to_frame('CossScreenFrame')
        parent = self.d.find_element_by_id(self.id)
        elem_month = parent.find_element_by_class_name('jq-dte-month') # needs to capture de value????
        elem_day = parent.find_element_by_class_name('jq-dte-day')
        elem_year = parent.find_element_by_class_name('jq-dte-year')
        return date(int(elem_year), int(elem_month), int(elem_day))


class signBox():
    """docstring for ClassName"""

    def __init__(self, driver, element_id):
        self.d = driver
        if not driver.find_elements_by_id(element_id):
            driver.switch_to_frame('CossScreenFrame')
        self.id = element_id

    def is_signed(self):
        parent = self.d.find_element_by_id(self.id)
        return parent.find_element_by_id("fradisplay_30").get_attribute('style').find('display: block;') != -1

    def sign_capture(self):
        parent = self.d.find_element_by_id(self.id)
        sign_button = parent.find_element_by_tag_name('button')
        sign_button.click()

    def sign(self, role):
        roles = { 'pi' : [(-100,0),'click',(30,0),(0,-30),(-40,0),(10,0),(0,-10),(0,85),'release',(60,0), 'click', (0,-60), 'release'],
                  'ai' :  [(-50,-35),'click',(-25,70), (25,-70),(25,70), 'release', (-60,-35), 'click', (60, 0), 'release', (60,35), 'click', (0,-60), 'release'],
                  'ow' :  [(-100,0),'click',(0,35),(30,0),(0,-70),(-40,0),(10,0),(0,35),'release',(60,-40), 'click', (15,80), (7,-35), (7,35), (15,-70), 'release'],
                  'ow2' :  [(-100,0),'click',(0,35),(30,0),(0,-70),(-40,0),(10,0),(0,35),'release',(60,-40), 'click', (15,80), (7,-35), (7,35), (15,-70), 'release', (50,0),
                               'click', (0,70), 'release', (20,0), 'click', (0,-80), 'release', (10,10), 'click', (-50,0), 'release', (5,60), 'click', (50,0), 'release'],
                  'pa' : [(-100,0),'click',(30,0),(0,-30),(-40,0),(10,0),(0,-10),(0,85),'release',(90,-75), 'click',(-25,70), (25,-70),(25,70), 'release', (-60,-35), 'click', (60, 0), 'release'],
                  'lg' : [(-100,-35),'click',(0,75),(0,-5),(-7,0),(37,0),'release',(70,-45), 'click', (-10,-15), (-20,0),(-10,15),(0,30),(10,15),(20,0),(10,-15),(0,20),(0,-35), (5,0),(-25,0), (0,15),'release'],
                  'tp' : [],
                  'py' : [],
                  'ag' : [(-50,-35),'click',(-25,70), (25,-70),(25,70), 'release', (-60,-35), 'click', (60, 0), 'release',
                            (0,35), (70,-45), 'click', (-10,-15), (-20,0),(-10,15),(0,30),(10,15),(20,0),(10,-15),(0,20),(0,-35), (5,0),(-25,0), (0,15),'release'],
                  'ag2' : [(-50,-35),'click',(-25,70), (25,-70),(25,70), 'release', (-60,-35), 'click', (60, 0), 'release',
                            (0,35), (70,-45), 'click', (-10,-15), (-20,0),(-10,15),(0,30),(10,15),(20,0),(10,-15),(0,20),(0,-35), (5,0),(-25,0), (0,15),'release',
                            (50,-50), 'click', (0,70), 'release', (20,0), 'click', (0,-80), 'release', (10,10), 'click', (-50,0), 'release', (5,60), 'click', (50,0), 'release'],
                }

        parent = self.d.find_element_by_id(self.id)
        if parent.find_elements_by_id("fra_30")[0].get_attribute('style').find('display: none;') != -1:
            self.sign_capture()
            print('clicking Sign button')
            #WebDriverWait(driver, 30).until(EC.alert_is_present())
        else:
            print('Sign button already clicked!')
        e = parent.find_element_by_class_name('jSignature')
        actions = ActionChains(self.d)
        actions.move_to_element(e)
        for value in roles[role]:
            if value == 'click':
                actions.click_and_hold(None)
            elif value == 'release':
                actions.release(None)
            else:
                actions.move_by_offset(value[0],value[1])
        actions.perform()
        self.sign_capture()
        print('Click Capture button')
        #WebDriverWait(self.d, 30).until(EC.staleness_of(By.ID, "fra_30"))
