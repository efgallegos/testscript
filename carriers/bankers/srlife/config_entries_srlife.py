"""SrLife Configuration Dictionaries"""

xmls_entry = {
    '"OWN_ADDR_State"|"OWN_ADDR_State_itmval"|"ADDR_State"|"ADDR_State_itmval"|ADDR_State__[1-3]{1,1}">|ADDR_State__[1-3]{1,1}_itmval">': "'>' + state + '<'",
    '"pdfBENE_State__[0-9]{1,1}">|"pdfOwnerState"|"PIJurisdiction"|"PIJurisdiction_itmval"|"State"|"State_itmval"': "'>' + state + '<'",
    '"EFT_ADDR_State"|"EFT_ADDR_State_itmval"|"Payor_BILLING_ADDR_State"|"Payor_BILLING_ADDR_State_itmval"|"pdfBillingState"': "'>' + state + '<'",
    '"ADDR_State_itmtxt"|"OWN_ADDR_State_itmtxt"|ADDR_State__[1-3]{1,1}_itmtxt">|"EFT_ADDR_State_itmtxt"|"Payor_BILLING_ADDR_State_itmtxt"': "'>' + config_values[product]['states'][state].upper() + '<'",
    '"PIJurisdiction_itmtxt"|"State_itmtxt"': "'>' + config_values[product]['states'][state] + '<'",
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
    '13X': {'full_name': 'Senior Life-Basic Life',
            'file_name': '13X'},
    '29J': {'full_name': 'Senior Life-Basic Life Graded Benefit',
            'file_name': '29J'},
    '13Y': {'full_name': 'Senior Life-Basic Life',
            'file_name': '13Y'},
    '29H': {'full_name': 'Senior Life-Basic Life Graded Benefit',
            'file_name': '29H'},
    }

# Product configuration dictionary

srlife_config = {
    'name': 'SrLife',
    'states': states,
    'plans': plans,
    'xmls_entry': xmls_entry,
    'product_path': 'SrLife',
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
