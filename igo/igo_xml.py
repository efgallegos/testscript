"""This file contains the functions used to creates an iGo XML file."""

import re, os
from config_entries import config_values


def updateXMLElement(line, carrier, product, state, plan, verbose=False):
    regex = re.compile(r'>[,-=a-zA-Z0-9_ ]*<')

    for entry in config_values[carrier][product]['xmls_entry']:
        if re.search(entry, line):
            string = eval(config_values[carrier][product]['xmls_entry'][entry])
            return regex.sub(string, line)
    else:
        return line


def createXML(carrier, product, state, plan, verbose=False):
    try:
        if verbose:
            print('Carrier: ' + carrier)
            print('Product: ' + product)
            print('State: ' + state)
            print('Plan: ' + plan)

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
                            config_values[carrier][product]['product_path']

        file_name = state + '_' + config_values[carrier][product]['plans'][plan]['file_name'] + '.xml'

        output_xml_path = output_xml_folder + \
                          config_values['os_path_separator'] + \
                          file_name


        # output_xml_path = config_values['base_path'] + \
        #     config_values[carrier]['carrier_path'] + \
        #     config_values['os_path_separator'] + \
        #     config_values[carrier][product]['product_path'] + \
        #     config_values['os_path_separator'] + \
        #     config_values[carrier][product]['xml_output_path'] + \
        #     config_values['os_path_separator'] + \
        #     state + '_' + \
        #     config_values[carrier][product]['plans'][plan]['file_name'] + '.xml'

        if verbose:
            print('input file path: ' + input_xml_path)
            print('output file path: ' + output_xml_path)

        if os.getcwd() != output_xml_folder:
            if verbose:
                print('Current directory: ', os.getcwd())
            os.chdir(output_xml_folder)
            if verbose:
                print('Changed currect directory to: ', output_xml_folder)

        if os.path.isfile(file_name):
            if verbose:
                print('XML file exists and it is at: ', output_xml_folder + config_values['os_path_separator'] + file_name)
                print('Skipping CREATE XML process...')
            return output_xml_path

        if verbose:
            print("File was never created for this state. Starting Craete XML process.")

        with open(input_xml_path, 'r') as input_file:
            with open(output_xml_path, 'w') as output_file:
                if verbose:
                    print('files opened successfully.')

                entity_client = False

                for line in input_file:
                    if entity_client:
                        updateLine = updateXMLElement(line, carrier, product, state, plan)
                    else:
                        entity_client = re.search('EntityName="Client"', line)
                        updateLine = line

                    if verbose:
                        print(updateLine)

                    output_file.write(updateLine)

                if verbose:
                    print('Files were closed successfully.')

                return output_xml_path

    except Exception as e:
        if verbose:
            print('Function CreateXML() failed.')
        raise createXMLException(str(e), carrier, product, state, plan)


class createXMLException(Exception):

    def __init__(self, value, carrier, product, state, plan):
        self.value = '"Function CreateXML() failed." - Carrier: ' + carrier + \
                     ', Product:' + product + ', Plan:' + plan + ', Sate:' + state + \
                      '.\nDetails: ' + value

    def __str__(self):
        return repr(self.value)
