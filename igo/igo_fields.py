from datetime import date

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
        parent = self.d.find_element_by_id(self.id)
        elem_month = parent.find_element_by_class_name('jq-dte-month') # needs to capture de value????
        elem_day = parent.find_element_by_class_name('jq-dte-day')
        elem_year = parent.find_element_by_class_name('jq-dte-year')
        return date(int(elem_year), int(elem_month), int(elem_day))
