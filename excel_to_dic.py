"""mapping fuctions: excel to dic"""

from pandas import *
from config_entries import config_values

def map_brd(product):

    input_file_path = config_values['base_path'] + 'brd.xlsm'

    print (input_file_path)

    df = read_excel(input_file_path, 1, index_col=None, na_values=['NA'])

    print (df.to_dict())

map_brd('fuwl')