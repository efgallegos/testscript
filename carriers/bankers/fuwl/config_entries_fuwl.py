"""FUWL Configuration Dictionaries"""

xmls_entry = {
     # 'ADDR_State__[0-9]{1,1}[0-5]{0,1}">': "'>' + state + '<'"
     'CaseDescription">': "'>State = ' + state + '<'",
     'APPCNT_ADDR_State|CB_ADDR_State|CHILD_Birth_StateOrCountry|CHILD_Birthstate|EFT_ADDR_State': "'>' + state + '<'",
     'OWN1_ADDR_State|OWN2_ADDR_State|PAYOR_ADDR_State|PB_ADDR_State|pdfBENE_ADDRState|PIBILL_ADDR_State': "'>' + state + '<'",
     'PIBirth_State2|PIEMP_ADDR_State|CopyPIADDR_State|StateOrCountry2': "'>' + state + '<'",
     '"State"|OI1_myState|PIAppState|PIJurisdiction">|PIJurisdiction_itmval': "'>' + state + '<'",
     'PIJurisdiction_itmtxt|"State_itmtxt">': "'>' + config_values[carrier][product]['states'][state] + '<'",
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


# Product's valid states

states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District of Columbia',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    # 'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
    }

# Product's valid plans

plans = {
    '19E': {'full_name': 'ClearVantage UL (19E)',
            'file_name': '19E'},
    '20E': {'full_name': 'TurningPoint UL (20E)',
            'file_name': '20E'},
    '14X': {'full_name': 'Innovative Life (14X)',
            'file_name': '14X'},
    'L-5Z1': {'full_name': 'ReliaTerm (L-5Z1)',
              'file_name': 'L-5Z1'},
    '10S': {'full_name': 'SecureView (10 Series)',
            'file_name': '10S'},
    '14V': {'full_name': 'Innovative Life (14V)',
            'file_name': '14V'}
    }

# Product configuration dictionary

fuwl_config = {
    'name': 'FUWL',
    'states': states,
    'plans': plans,
    'xmls_entry': xmls_entry,
    'product_path': 'FUWL',
    'runs': 'Runs',
    'xml_input_path': 'Input',
    'xml_output_path': 'Output',
    'xml_export_path': 'Export',
    # Forms created for each Run:
    'form_path': 'Forms',
    'images_path': 'Images',
    'xml_run_import_path': 'XML_Import',
    'xml_run_export_path': 'XML_Export'
    }
