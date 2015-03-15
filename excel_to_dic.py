"""mapping fuctions: excel to dic"""

from pandas import *
import pprint
from config_entries import config_values

def map_brd(product):

    input_file_path = config_values['base_path'] + 'brd.xlsm'

    print (input_file_path)

    df = read_excel(input_file_path, 1, index_col=0, na_values=['NA'])

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint (df.to_dict())

map_brd('fuwl')