"""This file contains the functions used to creates an iGo XML file."""

import re
from config_entries import config_values


def updateXMLElement(line, product, state, plan):
    regex = re.compile(r'>[,-=a-zA-Z0-9_ ]*<')

    for entry in config_values[product]['xmls_entry']:
        if re.search(entry, line):
            string = eval(config_values[product]['xmls_entry'][entry])
            return regex.sub(string, line)
    else:
        return line


def createXML(product, state, plan, verbose=False):
    try:
        if verbose:
            print('Product: ' + product)
            print('State: ' + state)
            print('Plan: ' + plan)

        input_xml_path = config_values['base_path'] + \
            config_values[product]['product_path'] + \
            config_values['os_path_separator'] + \
            config_values[product]['xml_input_path'] + \
            config_values['os_path_separator'] + \
            config_values[product]['plans'][plan]['file_name'] + '.xml'

        output_xml_path = config_values['base_path'] + \
            config_values[product]['product_path'] + \
            config_values['os_path_separator'] + \
            config_values[product]['xml_output_path'] + \
            config_values['os_path_separator'] + \
            state + '_' + \
            config_values[product]['plans'][plan]['file_name'] + '.xml'

        if verbose:
            print('input file path: ' + input_xml_path)
            print('output file path: ' + output_xml_path)

        input_file = open(input_xml_path, 'r')
        output_file = open(output_xml_path, 'w')

        if verbose:
            print('files opened successfully.')

        entity_client = False

        for line in input_file:
            if entity_client:
                updateLine = updateXMLElement(line, product, state, plan)
            else:
                entity_client = re.search('EntityName="Client"', line)
                updateLine = line

            if verbose:
                print(updateLine)

            output_file.write(updateLine)

        input_file.close()
        output_file.close()

        if verbose:
            print('Files were closed successfully.')

        return output_xml_path
    except Exception as e:
        if verbose:
            print('Function CreateXML() failed.')
        raise createXMLException(str(e), product, state, plan)


class createXMLException(Exception):

    def __init__(self, value, product, state, plan):
        self.value = '"Function CreateXML() failed." - Product:' + \
                      product + ', Plan:' + plan + ', Sate:' + state + \
                      '.\nDetails: ' + value

    def __str__(self):
        return repr(self.value)
