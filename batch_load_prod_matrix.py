import sys
import logging
import logging.handlers
import json
from datetime import datetime
from config_entries import config_values
from openpyxl import load_workbook

LOG_FILENAME = 'load_product_matrix_bankers.log'

# create logger with __name__
logger = logging.getLogger('testscript')
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create file handler
fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1018576*5, backupCount=7)
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handler to the logger
logger.addHandler(ch)
logger.addHandler(fh)

def load_prod_matrix(arguments):
    ####################################################################################
    #                               load_prod_matrix                                   #
    ####################################################################################
    #                                                                                  #
    #                                                                                  #
    #                                                                                  #
    #                                                                                  #
    #                                                                                  #
    #                                                                                  #
    #                                                                                  #
    #                                                                                  #
    #                                                                                  #
    ####################################################################################

    # start time counter to track the script duration.
    start_time = datetime.now()

    logger.info("load_prod_matrix -> ################################################################################")
    logger.info('load_prod_matrix -> Start time:' +  str(start_time))
    logger.info("load_prod_matrix -> Parameters list:")
    if len(arguments) == 2:
        carrier = arguments[1]
        logger.info("load_prod_matrix -> \tCarrier: " + arguments[1])
        excel_path = arguments[2]
        logger.info("load_prod_matrix -> \tExcel full path: " + arguments[2])
    else:
        carrier='bankers'
        logger.info("load_prod_matrix -> \tCarrier: " + carrier + " (Default value)")
        excel_path = config_values['base_path'] +\
                     config_values[carrier]['carrier_path'] + config_values['os_path_separator'] +\
                     'bankers_product_matrix.xlsx'
        logger.info("load_prod_matrix -> \tExcel full path: " + excel_path + " (Default value)")
    logger.info("load_prod_matrix -> --------------------------------------------------------------------------------")

    logger.debug("load_prod_matrix -> Loading excel workbook...")
    wb = load_workbook(filename = excel_path)
    logger.debug("load_prod_matrix -> Excel workbook loaded successfully.")
    
    products = wb.get_sheet_names()
    logger.debug("load_prod_matrix -> List of products to load: " + str(products))

    for product in products:
        logger.debug("load_prod_matrix -> Starting process for product: " + product) 
        sheet = wb.get_sheet_by_name(product)
        logger.debug("load_prod_matrix -> Sheet '" + product + "' loaded") 

        product_dict = {}
        row = 6
        while True:
            if sheet['C'+str(row)].value == None:
                #print (sheet['C'+str(row)].value)
                break
            else:
                col = 'D'
                while True:
                    if sheet[col + '5'].value == None:
                        #print(sheet[col + '5'].value)
                        break
                    else:
                        if sheet[col + str(row)].value == 'x' or sheet[col + str(row)].value == 'X':
                            if sheet['C' + str(row)].value in product_dict:
                                product_dict[sheet['C' + str(row)].value].append(sheet[col + '5'].value)
                            else:
                                product_dict[sheet['C' + str(row)].value] = [sheet[col + '5'].value]
                        col = chr(ord(col) + 1) 
            row += 1
        
        logger.debug("load_prod_matrix -> Finished process for product: " + product) 
        logger.debug("load_prod_matrix -> Dict: " + str(product_dict))

        logger.debug("load_prod_matrix -> Saving dict into json file")
        json_path = config_values['base_path'] +\
                    config_values[carrier]['carrier_path'] + config_values['os_path_separator'] +\
                    config_values[carrier][product]['product_path'] + config_values['os_path_separator'] +\
                    product + '_data.json'
        logger.debug("load_prod_matrix -> Product json file full paht: " + json_path)

        with open(json_path, 'w') as fp:
            json.dump(product_dict, fp, sort_keys=True, indent=4)
        logger.debug("load_prod_matrix -> JSON file saved")

if __name__ == "__main__":
    load_prod_matrix(sys.argv[1:])

