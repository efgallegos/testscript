"""Dictionaries Configuration"""

import platform
import json
import logging
import os, fnmatch
from igo.igo_config_entries import igo_config
import pprint

logger = logging.getLogger('testscript.config')
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

def search_products(carrier):
    path = get_base_path() + 'Carriers' + get_path_separator() + carrier + get_path_separator() + 'Products'
    products = os.listdir(path)
    products = [product for product in products if product != '.DS_Store']
    return products

def get_file_path(pattern, path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return os.path.join(root, name)
    return None        

config_values = {}

def load(config):
    json_file_path = get_file_path('*.json',get_base_path())
    logger.debug('testscript.config -> JASON path: ' + str(json_file_path))
    with open(json_file_path,'r') as data_file:    
        logger.debug('testscript.config -> File opened.')
        config.update(json.load(data_file))
        logger.debug('testscript.config -> Loading general config entries')
    logger.debug('testscript.config -> File closed.')

    logger.debug('testscript.config -> Loading base folder')
    config['base_path'] = get_base_path()
    config['os_path_separator'] = get_path_separator()

    logger.debug('testscript.config -> Loading igo_common dic')
    config['igo_common'] = igo_config

    logger.debug('testscript.config -> Loading Carriers')
    config['carriers'] = [x.lower() for x in search_carriers()]

    for carrier in search_carriers():
        logger.debug('testscript.config -> Loading Carrier : "' + carrier.lower() + '"')
        json_file_path = get_file_path('*.json',get_base_path() + 'Carriers' + get_path_separator() + carrier)
        logger.debug('testscript.config -> JASON path: ' + str(json_file_path))
        if json_file_path:
            with open(json_file_path,'r') as data_file:    
                logger.debug('testscript.config -> File opened.')
                config[carrier.lower()] = json.load(data_file)
                logger.debug('testscript.config -> Loading carrier "' + carrier.lower() + '"" config entries')
            logger.debug('testscript.config -> File closed.')

            logger.debug('testscript.config -> Loading carrier "' +  carrier.lower() + '" folder path')
            config[carrier.lower()]['carrier_path'] = get_base_path() + 'Carriers' + get_path_separator() + carrier + get_path_separator()

            logger.debug('testscript.config -> Loading State-Product Matrix for Carrier: ' + carrier.lower())
            config[carrier.lower()]['products'] = [x.lower() for x in search_products(carrier)]

            for product in search_products(carrier):
                logger.debug('testscript.config -> Loading config values for product: "' + product + '"')
                json_file_path = get_file_path('*.json', get_base_path() + 'Carriers' + get_path_separator() + carrier + get_path_separator() + 'Products' + get_path_separator() + product)
                logger.debug('testscript.config -> JASON path: ' + str(json_file_path))
                if json_file_path:
                    with open(json_file_path,'r') as data_file:    
                        logger.debug('testscript.config -> File opened.')
                        config[carrier.lower()][product.lower()] = json.load(data_file)
                        logger.debug('testscript.config -> Loading product "' + product.lower() + '"" config entries')
                    logger.debug('testscript.config -> File closed.')

                else:
                    config[carrier.lower()][product.lower()] = {
                                                                   'product_path' : config[carrier.lower()]['carrier_path'] + get_path_separator() + 'Products' + get_path_separator() + product + get_path_separator()
                                                               }

        else:
            logger.debug("testscript.config -> Carrier doesn't have config file to be loaded.")
            config[carrier.lower()] = {}
    
    #logger.debug('testscript.config -> "config": ' + str(config))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(config)

load(config_values)
