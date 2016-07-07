"""This file contains the functions used to creates an iGo XML file."""

import re, os
import logging
from config_entries import config_values


# create logger with __name__
logger = logging.getLogger('igo.igo_xml')
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handler to the logger
logger.addHandler(ch)

def updateXMLElement(line, carrier, product, state, plan, verbose=False):
    regex = re.compile(r'>[,-=a-zA-Z0-9_ ]*<')

    for entry in config_values[carrier][product]['xmls_entry']:
        if re.search(entry, line):
            string = eval(config_values[carrier][product]['xmls_entry'][entry])
            return regex.sub(string, line)
    else:
        return line


def createXML(carrier, product, state, plan, verbose=False):
    logger.info('"createXML" procedure started...')
    logger.debug('Parameters:')
    logger.debug('\t"Carrier": ' +  carrier) 
    logger.debug('\t"Product": ' + product)
    logger.debug('\t"State": ' + state) 
    logger.debug('\t"Plan" : '+ plan)
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
        logger.debug('Files paths:')
        logger.debug('\tInput file path: ' + input_xml_path)
        logger.debug('\tOutput file path: ' + output_xml_path)

        if os.getcwd() != output_xml_folder:
            logger.debug('Current directory: ' + os.getcwd())
            os.chdir(output_xml_folder)
            logger.debug('Changed currect directory to: ' + output_xml_folder)

        if os.path.isfile(file_name):
            logger.info('XML file exists and it is at: ' + output_xml_folder + config_values['os_path_separator'] + file_name)
            logger.info('Skipping CREATE XML process...')
            return output_xml_path

        logger.info("A XML file was never created for this state-product-plan.")
        logger.info("Starting XML creation process.")

        with open(input_xml_path, 'r') as input_file:
            with open(output_xml_path, 'w') as output_file:
                logger.debug('files opened successfully.')

                entity_client = False

                for line in input_file:
                    if entity_client:
                        updateLine = updateXMLElement(line, carrier, product, state, plan)
                    else:
                        entity_client = re.search('EntityName="Client"', line)
                        updateLine = line
                    logger.debug('XML: ' + updateLine)
                    output_file.write(updateLine)

                logger.debug('Files were closed successfully.')
        logger.info('CREATE XML process finished')
        return output_xml_path

    except Exception as e:
        logger.error('Function CreateXML() failed.')
        raise createXMLException(repr(e), carrier, product, state, plan)

class createXMLException(Exception):

    def __init__(self, value, carrier, product, state, plan):
        self.value = '"Function CreateXML() failed." - Carrier: ' + carrier + \
                     ', Product:' + product + ', Plan:' + plan + ', Sate:' + state + \
                      '.\nDetails: ' + value

    def __str__(self):
        return repr(self.value)
