"""This file contains the functions used to creates an iGo XML file."""

import re, os
import logging
from config_entries import config_values


# create logger with __name__
logger = logging.getLogger('igo.igo_xml')
# logger.setLevel(logging.DEBUG)
# # create console handler
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# # create file handler
# fh = logging.FileHandler('run_bankers.log')
# fh.setLevel(logging.DEBUG)
# # create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# # add the handler to the logger
# logger.addHandler(ch)
# logger.addHandler(fh)

def updateXMLElement(line, carrier, product, state, plan, verbose=False):
    regex = re.compile(r'>[,-=a-zA-Z0-9_ ]*<')

    for entry in config_values[carrier][product]['xmls_entry']:
        if re.search(entry, line):
            string = eval(config_values[carrier][product]['xmls_entry'][entry])
            return regex.sub(string, line)
    else:
        return line


def createXML(carrier, product, state, plan, verbose=False):
    logger.info('createXML -> "createXML" procedure started...')
    logger.debug('createXML -> Parameters:')
    logger.debug('createXML -> \t"Carrier": ' +  carrier)
    logger.debug('createXML -> \t"Product": ' + product)
    logger.debug('createXML -> \t"State": ' + state)
    logger.debug('createXML -> \t"Plan" : '+ plan)
    try:
        input_xml_path = config_values['base_path'] + \
                         config_values[carrier]['carrier_path'] + \
                         config_values['os_path_separator'] + \
                         config_values[carrier][product]['product_path'] + \
                         config_values['os_path_separator'] + \
                         config_values[carrier][product]['xml_input_path'] + \
                         config_values['os_path_separator'] + \
                         config_values[carrier][product]['plans'][plan]['file_name'] + '.xml'

        output_xml_folder = config_values['base_path'] + \
                            config_values[carrier]['carrier_path'] + \
                            config_values['os_path_separator'] + \
                            config_values[carrier][product]['product_path'] + \
                            config_values['os_path_separator'] + \
                            config_values[carrier][product]['xml_output_path']

        file_name = state + '_' + config_values[carrier][product]['plans'][plan]['file_name'] + '.xml'

        output_xml_path = output_xml_folder + \
                          config_values['os_path_separator'] + \
                          file_name
        logger.debug('createXML -> Files paths:')
        logger.debug('createXML -> \tInput file path: ' + input_xml_path)
        logger.debug('createXML -> \tOutput file path: ' + output_xml_path)

        if os.getcwd() != output_xml_folder:
            logger.debug('createXML -> Current directory: ' + os.getcwd())
            os.chdir(output_xml_folder)
            logger.debug('createXML -> Changed currect directory to: ' + output_xml_folder)

        if os.path.isfile(file_name):
            logger.info('createXML -> XML file exists and it is at: ' + output_xml_folder + config_values['os_path_separator'] + file_name)
            logger.info('createXML -> Skipping CREATE XML process...')
            return output_xml_path

        logger.info("createXML -> A XML file was never created for this state-product-plan.")
        logger.info("createXML -> Starting XML creation process.")

        with open(input_xml_path, 'r') as input_file:
            with open(output_xml_path, 'w') as output_file:
                logger.debug('createXML -> Files opened successfully.')

                entity_client = False

                for line in input_file:
                    if entity_client:
                        updateLine = updateXMLElement(line, carrier, product, state, plan)
                    else:
                        entity_client = re.search('EntityName="Client"', line)
                        updateLine = line
                    logger.debug('createXML -> XML: ' + updateLine)
                    output_file.write(updateLine)

                logger.debug('createXML -> Files were closed successfully.')
        logger.info('createXML -> CREATE XML process finished')
        return output_xml_path

    except Exception as e:
        logger.error('createXML -> Function CreateXML() failed.')
        raise createXMLException(repr(e), carrier, product, state, plan)

class createXMLException(Exception):

    def __init__(self, value, carrier, product, state, plan):
        self.value = '"Function CreateXML() failed." - Carrier: ' + carrier + \
                     ', Product:' + product + ', Plan:' + plan + ', Sate:' + state + \
                      '.\nDetails: ' + value

    def __str__(self):
        return repr(self.value)
