"""STC Configuration Dictionaries"""

xmls_entry = {
    'ADDR_State">|ADDR_State_itmval|EFT_State">|EFT_State_itmval|PIJurisdiction">|PIJurisdiction_itmval': "'>' + state + '<'",
    'ProducerAddressState">|ProducerAddressStateTC|State">|State_itmval">|TPState">|TPState_itmval': "'>' + state + '<'",
    'ADDR_State_itmtxt|EFT_State_itmtxt|TPState_itmtxt': "'>' + config_values[product]['states'][state].upper() + '<'",
    '"PIJurisdiction_itmtxt"|"State_itmtxt"': "'>' + config_values[product]['states'][state] + '<'",
    'PIFullAddress': "'>123 Main St Exton, ' + state + ' 11111<'",
    'AGENT_FullAddress': "'>123 Agent St Exton, ' + state + ' 11111<'",
    'AGENT2_FullAddress':"'>123 Second St Exton, ' + state + ' 11111<'",
    'AGENT_pdf_FullAddress':"'>Address Line 1, Address 2, Exton, ' + state + ', 111111111<'",
    'pdfAGENT_FullNameAddress':"'>Agent Name 123 Agent St Exton, ' + state + ' 11111<'",
    'ProducerCityStateZip':"'>Exton, ' + state + ' 11111-1111<'",
    '"PIFirstName">': "'>' + state + '_' + plan + '<'",
    '"PILastName">': "'>' + config_values[product]['name'] + '<'",
    'PIFullName': "'>' + state + '_' + plan + ' X ' + config_values[product]['name'] + ' Sr'+ '<'",
    'pdfReversePIName': "'>' + config_values[product]['name'] + ', ' + state + '_' + plan + ' X' + '<'",
    'CaseDescription': "'>State=' + state + '<'"
    }


# Product's valid states

states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    # 'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District of Columbia',
    # 'FL': 'Florida',
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
    # 'MA': 'Massachusetts',
    'MI': 'Michigan',
    # 'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    # 'NJ': 'New Jersey',
    'NM': 'New Mexico',
    # 'NY': 'New York',
    'NC': 'North Carolina',
    # 'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    # 'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    # 'SD': 'South Dakota',
    'TN': 'Tennessee',
    # 'TX': 'Texas',
    'UT': 'Utah',
    # 'VT': 'Vermont',
    'VA': 'Virginia',
    # 'WA': 'Washington',
    'WV': 'West Virginia',
    # 'WI': 'Wisconsin',
    'WY': 'Wyoming'
    }

# Product's valid plans

plans = {
    'GR-N560': {'full_name': 'GR-N560',
                'file_name': 'GR-N560'},
    'GR-N565': {'full_name': 'GR-N565',
                'file_name': 'GR-N565'},
    'GR-N320': {'full_name': 'GR-N320',
                'file_name': 'GR-N320'},
    'GR-N325': {'full_name': 'GR-N325',
                'file_name': 'GR-N325'}
    }

# Product configuration dictionary

stc_config = {
    'name': 'STC',
    'states': states,
    'plans': plans,
    'xmls_entry': xmls_entry,
    'product_path': 'STC',
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
