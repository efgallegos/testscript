"""Test File"""
import pprint
from config_entries import config_values

try:
    pp = pprint.PrettyPrinter(indent=4)
    mydict = config_values['bankers']
    pp.pprint(mydict)  
except Exception as e:
    print('Exception: ' + str(e))

