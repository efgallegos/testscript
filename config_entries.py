"""Dictionaries Configuration"""

import platform
import json
import logging
import os, fnmatch
from igo.igo_config_entries import igo_config
import pprint

logger = logging.getLogger('testscript.config_values')
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(ch)

def get_base_path():
    if platform.system() == "Darwin":
        return '/Users/efgallegos/Dropbox/Automation/'
    return 'C:\\zz_EFG\\Dropbox\\Automation\\'


def get_path_separator():
    if platform.system() == "Darwin":
        return'/'
    return '\\'

def search_carriers():
    path = get_base_path() + 'Carriers'
    carriers = os.listdir(path)
    carriers = [carrier for carrier in carriers if carrier != '.DS_Store']
    return carriers

print(search_carriers())

def search_products(carrier):
    path = get_base_path() + 'Carriers' + get_path_separator() + carrier + get_path_separator() + 'Products'
    products = os.listdir(path)
    products = [product for product in products if product != '.DS_Store']
    return products

print(search_products('Bankers'))

def find_file(pattern, path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return os.path.join(root, name)
    return None        

def load():
    # output_file_path = get_base_path() + 'config_entries.json'
    # with open(output_file_path,'r') as f:
    #     for line in f:
    #         new_entry = line.split(',')
    #         config_values[new_entry[0]] = new_entry[1]
    pp = pprint.PrettyPrinter(indent=4)

    json_file_path = find_file('*.json',get_base_path())
    logger.debug('testscript.config_values -> JASON path: ' + str(json_file_path))
    with open(json_file_path,'r') as data_file:    
        logger.debug('testscript.config_values -> File opened.')
        config_values = json.load(data_file)
        logger.debug('testscript.config_values -> Loading general config entries')
    logger.debug('testscript.config_values -> File closed.')

    logger.debug('testscript.config_values -> Loading base folder')
    config_values['base_path'] = get_base_path()
    config_values['os_path_separator'] = get_path_separator()

    logger.debug('testscript.config_values -> Loading igo_common dic')
    config_values['igo_common'] = igo_config

    logger.debug('testscript.config_values -> Loading Carriers')
    config_values['carriers'] = [x.lower() for x in search_carriers()]

    for carrier in search_carriers():
        logger.debug('testscript.config_values -> Loading Carrier : "' + carrier.lower() + '"')
        json_file_path = find_file('*.json',get_base_path() + 'Carriers' + get_path_separator() + carrier)
        logger.debug('testscript.config_values -> JASON path: ' + str(json_file_path))
        if json_file_path:
            with open(json_file_path,'r') as data_file:    
                logger.debug('testscript.config_values -> File opened.')
                config_values[carrier.lower()] = json.load(data_file)
                logger.debug('testscript.config_values -> Loading carrier "' + carrier.lower() + '"" config entries')
            logger.debug('testscript.config_values -> File closed.')

            logger.debug('testscript.config_values -> Loading carrier "' +  carrier.lower() + '" folder path')
            config_values[carrier.lower()]['carrier_path'] = carrier

            logger.debug('testscript.config_values -> Loading State-Product Matrix for Carrier: ' + carrier.lower())
            config_values[carrier.lower()]['products'] = [x.lower() for x in search_products(carrier)]

            for product in search_products(carrier):
                logger.debug('testscript.config_values -> Loading config values for product: "' + product + '"')
                config_values[carrier.lower()][product.lower()] = {}

        else:
            logger.debug("testscript.config_values -> Carrier doesn't have config file to be loaded")
            config_values[carrier.lower()] = {}
    
    logger.debug('testscript.config_values -> "Config_values": ' + str(config_values))
    pp.pprint(config_values)

load()
