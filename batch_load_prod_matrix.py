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

annuity_xmls_entry = {
        'ADDR_State__[0-9]{1,1}[0-5]{0,1}">': "'>' + state + '<'",
        'ADDR_State__[0-9]_itmval">': "'>' + state + '<'",
        'ADDR_State__[0-9]_itmtxt">': "'>' + config_values[carrier][product]['states'][state]['name'].upper() + '<'",
        'FullAddress">': "'>123 Main St Exton, ' + state + ' 11111-1111<'",
        'PIFullName">|APPCNT_FullName">': "'>' + state + '_' + plan + ' ' + config_values[carrier][product]['name'] + '<'",
        'PIFirstName">': "'>' + state + '_' + plan + '<'",
        'PILastName">': "'>' + config_values[carrier][product]['name'] + '<'",
        '"State">|"State_itmval">': "'>' + state + '<'",
        '"State_itmtxt">': "'>' + config_values[carrier][product]['states'][state]['name'] + '<'",
        '"PIJurisdiction">|"PIJurisdiction_itmval">': "'>' + state + '<'",
        '"PIJurisdiction_itmtxt">':"'>' + config_values[carrier][product]['states'][state]['name'] + '<'",
        'HEY_IT_ALSO_WORKED">': "'>' + state + '<'"
        }

cb_xmls_entry = {
    'ADDR_State">|ADDR_State_itmval|EFT_State">|EFT_State_itmval|PIJurisdiction">|PIJurisdiction_itmval': "'>' + state + '<'",
    'ProducerAddressState">|ProducerAddressStateTC|State">|State_itmval">|TPState">|TPState_itmval': "'>' + state + '<'",
    'ADDR_State_itmtxt|EFT_State_itmtxt|TPState_itmtxt': "'>' + config_values[carrier][product]['states'][state]['name'].upper() + '<'",
    '"PIJurisdiction_itmtxt"|"State_itmtxt"': "'>' + config_values[carrier][product]['states'][state]['name'] + '<'",
    'PIFullAddress': "'>123 Main St Exton, ' + state + ' 11111<'",
    'AGENT_FullAddress': "'>123 Agent St Exton, ' + state + ' 11111<'",
    'AGENT2_FullAddress':"'>123 Second St Exton, ' + state + ' 11111<'",
    'AGENT_pdf_FullAddress':"'>Address Line 1, Address 2, Exton, ' + state + ', 111111111<'",
    'pdfAGENT_FullNameAddress':"'>Agent Name 123 Agent St Exton, ' + state + ' 11111<'",
    'ProducerCityStateZip':"'>Exton, ' + state + ' 11111-1111<'",
    '"PIFirstName">': "'>' + state + '_' + config_values[carrier][product]['plans'][plan]['full_name'] + '<'",
    '"PILastName">': "'>' + config_values[carrier][product]['name'] + '<'",
    'PIFullName': "'>' + state + '_' + config_values[carrier][product]['plans'][plan]['full_name'] + ' X ' + config_values[carrier][product]['name'] + ' Sr' + '<'",
    'pdfReversePIName': "'>' + config_values[carrier][product]['name'] + ', ' + state + '_' + config_values[carrier][product]['plans'][plan]['full_name'] + ' X' + '<'",
    'CaseDescription': "'>State=' + state + '<'"
    }

fuwl_xmls_entry = {
     # 'ADDR_State__[0-9]{1,1}[0-5]{0,1}">': "'>' + state + '<'"
     'CaseDescription">': "'>State = ' + state + '<'",
     'APPCNT_ADDR_State|CB_ADDR_State|CHILD_Birth_StateOrCountry|CHILD_Birthstate|EFT_ADDR_State': "'>' + state + '<'",
     'OWN1_ADDR_State|OWN2_ADDR_State|PAYOR_ADDR_State|PB_ADDR_State|pdfBENE_ADDRState|PIBILL_ADDR_State': "'>' + state + '<'",
     'PIBirth_State2|PIEMP_ADDR_State|CopyPIADDR_State|StateOrCountry2': "'>' + state + '<'",
     '"State"|OI1_myState|PIAppState|PIJurisdiction">|PIJurisdiction_itmval': "'>' + state + '<'",
     'PIJurisdiction_itmtxt|"State_itmtxt">': "'>' + config_values[carrier][product]['states'][state]['name'] + '<'",
     'PICityStateZip': "'>Exton, ' + state + ' 11111-1111<'",
     'APPCNT_FullAddress|OWN1_FullAddress|OWN2_FullAddress|PIADDR_FullAddress|PIFullAddress': "'>123 Main St Exton, ' + state + ' 11111-1111<'",
     'PB_FullAddress|CB_FullAddress': "'>123 Bene St Exton, ' + state + ' 111111111<'",
     '"PIFirstName"|OI1_myPIFirstName|PImyPIFirstName': "'>' + state + '_' + plan + '<'",
     '"PILastName"|PImyPILastName|OI1_myPILastName': "'>' + config_values[carrier][product]['name'] + '<'",
     'PIFullName': "'>' + state + '_' + plan + ' X ' + config_values[carrier][product]['name'] + '<'",
     'REM_MAIN_04_OWN2': "'>Section 4 - Owner 2 Information [LINE_BREAK]     Relationship: Mother[LINE_BREAK]     Name: Mother X Name MBA[LINE_BREAK]     Address: 123 Main St[LINE_BREAK]     City: Exton[LINE_BREAK]     State: ' + state + '[LINE_BREAK]     Zip: 11111-1111[LINE_BREAK]     SSN: 711-11-1111[LINE_BREAK]     DOB: 01/28/1960[LINE_BREAK]     Phone - home: (789)456-4561[LINE_BREAK]     Phone - work/cell: (564)561-5645<'",
     'REM_MAIN_04_PAYOR': "'>Section 4 - Payor Information [LINE_BREAK]     Relationship: Brother[LINE_BREAK]     Name: Payor X Name Sr[LINE_BREAK]     Address: 123 Main St[LINE_BREAK]     City: Exton[LINE_BREAK]     State: ' + state + '[LINE_BREAK]     Zip: 11111-1111[LINE_BREAK]     SSN: 611-11-1111[LINE_BREAK]     DOB: 01/28/1985[LINE_BREAK]     Phone - home: (787)987-4897[LINE_BREAK]     Phone - work/cell: (456)456-4564<'",
     'REM_MAIN_06_BENES': "'>Section 6 - Full Beneficiary Information [LINE_BREAK]     Beneficiary 1[LINE_BREAK]          Name: Son 1 Name Sr[LINE_BREAK]          Type: Primary[LINE_BREAK]          Relationship: Son[LINE_BREAK]          Date of Birth: 01/28/2000[LINE_BREAK]          SSN: 922-22-2222[LINE_BREAK]          Address: 123 Bene St[LINE_BREAK]          City: Exton[LINE_BREAK]          State: ' + state + '[LINE_BREAK]          Zip: 11111-1111[LINE_BREAK]     Beneficiary 2[LINE_BREAK]          Name: Daughter 2 Name CPA[LINE_BREAK]          Type: Primary[LINE_BREAK]          Relationship: Daughter[LINE_BREAK]          Date of Birth: 01/28/2001[LINE_BREAK]          SSN: 822-22-2222[LINE_BREAK]          Address: 123 Bene St[LINE_BREAK]          City: Exton[LINE_BREAK]          State: ' + state + '[LINE_BREAK]          Zip: 11111-1111[LINE_BREAK]     Beneficiary 3[LINE_BREAK]          Name: Son 3 Name DDS[LINE_BREAK]          Type: Primary[LINE_BREAK]          Relationship: Son[LINE_BREAK]          Date of Birth: 01/28/2003[LINE_BREAK]          SSN: 722-22-2222[LINE_BREAK]          Address: 123 Bene St[LINE_BREAK]          City: Exton[LINE_BREAK]          State: ' + state + '[LINE_BREAK]          Zip: 11111-1111[LINE_BREAK]     Beneficiary 4[LINE_BREAK]          Name: Daughter 4 Name EdD[LINE_BREAK]          Type: Primary[LINE_BREAK]          Relationship: Daughter[LINE_BREAK]          Date of Birth: 01/28/2004[LINE_BREAK]          SSN: 622-22-2222[LINE_BREAK]          Address: 123 Bene St[LINE_BREAK]          City: Exton[LINE_BREAK]          State: ' + state + '[LINE_BREAK]          Zip: 11111-1111[LINE_BREAK]     Beneficiary 5[LINE_BREAK]          Name: Sister 5 Name MBA[LINE_BREAK]          Type: Contingent[LINE_BREAK]          Relationship: Sister[LINE_BREAK]          Date of Birth: 01/28/1981[LINE_BREAK]          SSN: 522-22-2222[LINE_BREAK]          Share: 25 %[LINE_BREAK]          Address: 123 Bene St[LINE_BREAK]          City: Exton[LINE_BREAK]          State: ' + state + '[LINE_BREAK]          Zip: 11111-1111[LINE_BREAK]     Beneficiary 6[LINE_BREAK]          Name: Brother 6 Name Sr[LINE_BREAK]          Type: Contingent[LINE_BREAK]          Relationship: Brother[LINE_BREAK]          Date of Birth: 01/28/1985[LINE_BREAK]          SSN: 422-22-2222[LINE_BREAK]          Share: 25 %[LINE_BREAK]          Address: 123 Bene St[LINE_BREAK]          City: Exton[LINE_BREAK]          State: ' + state + '[LINE_BREAK]          Zip: 11111-1111[LINE_BREAK]     Beneficiary 7[LINE_BREAK]          Name: Uncle 7 Name Sr[LINE_BREAK]          Type: Contingent[LINE_BREAK]          Relationship: Uncle[LINE_BREAK]          Date of Birth: 01/28/1965[LINE_BREAK]          SSN: 322-22-2222[LINE_BREAK]          Share: 25 %[LINE_BREAK]          Address: 123 Bene St[LINE_BREAK]          City: Exton[LINE_BREAK]          State: ' + state + '[LINE_BREAK]          Zip: 11111-1111[LINE_BREAK]     Beneficiary 8[LINE_BREAK]          Name: Spouse 8 Name MBA[LINE_BREAK]          Type: Contingent[LINE_BREAK]          Relationship: Spouse[LINE_BREAK]          Date of Birth: 01/28/1994[LINE_BREAK]          SSN: 122-22-2222[LINE_BREAK]          Share: 25 %[LINE_BREAK]          Address: 123 Bene St[LINE_BREAK]          City: Exton[LINE_BREAK]          State: ' + state + '[LINE_BREAK]          Zip: 11111-1111<'"
     }

medsupp_xmls_entry = {
    '"OTHINS_State__[0-9]">': "'>' + state + '<'",
    '"EFT_States"|"EFT_States_itmval"|"PIADDR_State"|"PIADDR_State_itmval"|"PIJurisdiction"|"PIJurisdiction_itmval"|"State"|"State_itmval"': "'>' + state + '<'",
    '"AGENT_ADDR_State"|"AGENT_ADDR_State_itmval"|"pdfBillingState"|"PIBILLING_ADDR_State"|"PIBILLING_ADDR_State_itmval"': "'>' + state + '<'",
    '"EFT_States_itmtxt"|"PIADDR_State_itmtxt"': "'>' + config_values[carrier][product]['states'][state]['name'].upper() + '<'",
    '"PIJurisdiction_itmtxt"|"State_itmtxt"': "'>' + config_values[carrier][product]['states'][state]['name'] + '<'",
    '"PIFullAddress">': "'>123 Main St Exton, ' + state + ' 12345<'",
    '"AGENT_FullAddress">': "'>123 Agent St Exton, ' + state + ' 12345<'",
    '"pdfAGENT_FullNameAddress">': "'>Agent Name 123 Agent St Exton, ' + state + ' 12345<'",
    '"PIFirstName"|"pdfPIAdjFirstName">': "'>' + state + '_' + plan + '<'",
    '"PILastName"|"pdfPIAdjLastName">': "'>' + config_values[carrier][product]['name'] + '<'",
    '"PIFullName">|"APPCNT_FullName">': "'>' + state + '_' + plan + ' ' + config_values[carrier][product]['name'] + '<'",
     }

spwl_xmls_entry = {
    '"OWN_ADDR_State"|"OWN_ADDR_State_itmval"|"ADDR_State"|"ADDR_State_itmval"|ADDR_State__[1-3]{1,1}">|ADDR_State__[1-3]{1,1}_itmval">': "'>' + state + '<'",
    '"pdfBENE_State__[0-9]{1,1}[0-5]{0,1}">|"pdfOwnerState"|"PIJurisdiction"|"PIJurisdiction_itmval"|"State"|"State_itmval"': "'>' + state + '<'",
    '"ADDR_State_itmtxt"|"OWN_ADDR_State_itmtxt"|ADDR_State__[1-3]{1,1}_itmtxt">': "'>' + config_values[carrier][product]['states'][state]['name'].upper() + '<'",
    '"PIJurisdiction_itmtxt"|"State_itmtxt"': "'>' + config_values[carrier][product]['states'][state]['name'] + '<'",
    '"APPCNT_FullAddress"': "'>123 Owner St  Exton, '+ state +', 11111<'",
    '"PIFullAddress">': "'>123 Main St Exton, ' + state + ' 11111<'",
    '"pdfAPPCNT_CityState"': "'>Exton, ' + state + ' 11111<'",
    '"pdfCityStateZip"': "'>Exton, ' + state + ', 11111<'",
    '"CaseDescription">': "'>State=' + state + '<'",
    '"PIFirstName">': "'>' + state + '_' + plan + '<'",
    '"PILastName">': "'>' + config_values[carrier][product]['name'] + '<'",
    '"PIFullName">|"CWPartyName__70">': "'>' + state + '_' + plan + ' X ' + config_values[carrier][product]['name'] + ' Sr'+ '<'",
    '"pdfReversePIName">': "'>' + config_values[carrier][product]['name'] + ', ' + state + '_' + plan + ' X' + '<'"
    }

srlife_xmls_entry = {
    '"OWN_ADDR_State"|"OWN_ADDR_State_itmval"|"ADDR_State"|"ADDR_State_itmval"|ADDR_State__[1-3]{1,1}">|ADDR_State__[1-3]{1,1}_itmval">': "'>' + state + '<'",
    '"pdfBENE_State__[0-9]{1,1}">|"pdfOwnerState"|"PIJurisdiction"|"PIJurisdiction_itmval"|"State"|"State_itmval"': "'>' + state + '<'",
    '"EFT_ADDR_State"|"EFT_ADDR_State_itmval"|"Payor_BILLING_ADDR_State"|"Payor_BILLING_ADDR_State_itmval"|"pdfBillingState"': "'>' + state + '<'",
    '"ADDR_State_itmtxt"|"OWN_ADDR_State_itmtxt"|ADDR_State__[1-3]{1,1}_itmtxt">|"EFT_ADDR_State_itmtxt"|"Payor_BILLING_ADDR_State_itmtxt"': "'>' + config_values[carrier][product]['states'][state]['name'].upper() + '<'",
    '"PIJurisdiction_itmtxt"|"State_itmtxt"': "'>' + config_values[carrier][product]['states'][state]['name'] + '<'",
    '"APPCNT_FullAddress"': "'>123 Owner St  Exton, '+ state +', 11111<'",
    '"PIFullAddress">': "'>123 Main St Exton, ' + state + ' 11111<'",
    '"EFT_BankAddress">': "'>123 Bank St Exton, ' + state + ' 11111<'",
    '"pdfAPPCNT_CityState"': "'>Exton, ' + state + ' 11111<'",
    '"pdfCityStateZip"': "'>Exton, ' + state + ', 11111<'",
    '"PIFirstName">': "'>' + state + '_' + plan + '<'",
    '"PILastName">': "'>' + config_values[product]['name'] + '<'",
    '"PIFullName">': "'>' + state + '_' + plan + ' X ' + config_values[product]['name'] + ' Sr'+ '<'",
    '"pdfReversePIName">': "'>' + config_values[product]['name'] + ', ' + state + '_' + plan + ' X' + '<'",
    '"CaseDescription">': "'>State=' + state + '<'"
    }

stc_xmls_entry = {
    'ADDR_State">|ADDR_State_itmval|EFT_State">|EFT_State_itmval|PIJurisdiction">|PIJurisdiction_itmval': "'>' + state + '<'",
    'ProducerAddressState">|ProducerAddressStateTC|State">|State_itmval">|TPState">|TPState_itmval': "'>' + state + '<'",
    'ADDR_State_itmtxt|EFT_State_itmtxt|TPState_itmtxt': "'>' + config_values[carrier][product]['states'][state]['name'].upper() + '<'",
    '"PIJurisdiction_itmtxt"|"State_itmtxt"': "'>' + config_values[carrier][product]['states'][state]['name'] + '<'",
    'PIFullAddress': "'>123 Main St Exton, ' + state + ' 11111<'",
    'AGENT_FullAddress': "'>123 Agent St Exton, ' + state + ' 11111<'",
    'AGENT2_FullAddress':"'>123 Second St Exton, ' + state + ' 11111<'",
    'AGENT_pdf_FullAddress':"'>Address Line 1, Address 2, Exton, ' + state + ', 111111111<'",
    'pdfAGENT_FullNameAddress':"'>Agent Name 123 Agent St Exton, ' + state + ' 11111<'",
    'ProducerCityStateZip':"'>Exton, ' + state + ' 11111-1111<'",
    '"PIFirstName">': "'>' + state + '_' + plan + '<'",
    '"PILastName">': "'>' + config_values[carrier][product]['name'] + '<'",
    'PIFullName': "'>' + state + '_' + plan + ' X ' + config_values[carrier][product]['name'] + ' Sr' + '<'",
    'pdfReversePIName': "'>' + config_values[carrier][product]['name'] + ', ' + state + '_' + plan + ' X' + '<'",
    'CaseDescription': "'>State=' + state + '<'"
    }

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
        excel_path = config_values[carrier]['carrier_path'] + 'bankers_product_matrix.xlsx'
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

        product_dict['name'] = product.upper()

        product_dict['product_path'] = config_values[carrier]['carrier_path'] +\
                                       'Products' + config_values['os_path_separator'] +\
                                       product + config_values['os_path_separator']
        product_dict['xml_input_path'] = config_values[carrier]['carrier_path'] +\
                                       'Products' + config_values['os_path_separator'] +\
                                       product + config_values['os_path_separator'] +\
                                       'Input' + config_values['os_path_separator']
        product_dict['xml_output_path'] = config_values[carrier]['carrier_path'] +\
                                       'Products' + config_values['os_path_separator'] +\
                                       product + config_values['os_path_separator'] +\
                                       'Output' + config_values['os_path_separator']                                       
        product_dict['xml_export_path'] = config_values[carrier]['carrier_path'] +\
                                       'Products' + config_values['os_path_separator'] +\
                                       product + config_values['os_path_separator'] +\
                                       'Export' + config_values['os_path_separator']
        product_dict['runs_path'] = config_values[carrier]['carrier_path'] +\
                                       'Products' + config_values['os_path_separator'] +\
                                       product + config_values['os_path_separator'] +\
                                       'Runs' + config_values['os_path_separator']

        logger.debug("load_prod_matrix -> General product config values loaded") 

        states = {}

        row = 7
        while True:
            if sheet['B'+str(row)].value == None:
                #print (sheet['C'+str(row)].value)
                break
            else:
                col = 'C'
                while True:
                    if sheet[col + '6'].value == None:
                        #print(sheet[col + '5'].value)
                        break
                    else:
                        if sheet[col + str(row)].value == 'x' or sheet[col + str(row)].value == 'X':
                            if sheet['B' + str(row)].value in states:
                                states[sheet['B' + str(row)].value]['plans'].append(sheet[col + '6'].value)
                            else:
                                states[sheet['B' + str(row)].value] = {'name': sheet['A'+str(row)].value, 
                                                                       'plans': [sheet[col + '6'].value]}
                        col = chr(ord(col) + 1) 
            row += 1

        product_dict['states'] = states
        logger.debug("load_prod_matrix -> State Dict for product loaded")
        
        plans = {}

        col = 'C'
        while True:
            plan = sheet[col + '6'].value
            if plan == None:
                break
            else:
                plans[plan] = {'full_name': sheet[col + '6'].value,
                               'file_name': plan }
            col = chr(ord(col) + 1)

        product_dict['plans'] = plans
        logger.debug("load_prod_matrix -> Plans Dict for product loaded")

        if product.lower() == 'annuity':
            product_dict['xmls_entry'] = annuity_xmls_entry
        elif product.lower() == 'cb':
            product_dict['xmls_entry'] = cb_xmls_entry
        elif product.lower() == 'fuwl':
            product_dict['xmls_entry'] = fuwl_xmls_entry
        elif product.lower() == 'medsupp':
            product_dict['xmls_entry'] = medsupp_xmls_entry
        elif product.lower() == 'spwl':
            product_dict['xmls_entry'] = spwl_xmls_entry
        elif product.lower() == 'srlife':
            product_dict['xmls_entry'] = srlife_xmls_entry
        elif product.lower() == 'stc':
            product_dict['xmls_entry'] = stc_xmls_entry
        else:
            product_dict['xmls_entry'] = {}
        logger.debug("load_prod_matrix -> XMLS_Entry Dict for product loaded")


        logger.debug("load_prod_matrix -> Finished process for product: " + product) 
        logger.debug("load_prod_matrix -> Dict: " + str(product_dict))

        logger.debug("load_prod_matrix -> Saving dict into json file")
        json_path = config_values[carrier]['carrier_path'] +\
                    'Products' + config_values['os_path_separator'] +\
                    product + config_values['os_path_separator'] +\
                    product.lower() + '_data.json'
        logger.debug("load_prod_matrix -> Product json file full path: " + json_path)

        with open(json_path, 'w') as fp:
            json.dump(product_dict, fp, sort_keys=True, indent=4)
        logger.debug("load_prod_matrix -> JSON file saved")

    logger.info('load_prod_matrix -> End time:' + str(datetime.now()))
    logger.info('load_prod_matrix -> Execution time:' + str(datetime.now()-start_time))
    logger.info("load_prod_matrix -> ################################################################################")

if __name__ == "__main__":
    load_prod_matrix(sys.argv[1:])

