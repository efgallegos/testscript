"""Critical Benefits Configuration Dictionaries"""

xmls_entry = {
    'ADDR_State">|ADDR_State_itmval|EFT_State">|EFT_State_itmval|PIJurisdiction">|PIJurisdiction_itmval': "'>' + state + '<'",
    'ProducerAddressState">|ProducerAddressStateTC|State">|State_itmval">|TPState">|TPState_itmval': "'>' + state + '<'",
    'ADDR_State_itmtxt|EFT_State_itmtxt|TPState_itmtxt': "'>' + config_values[carrier][product]['states'][state].upper() + '<'",
    '"PIJurisdiction_itmtxt"|"State_itmtxt"': "'>' + config_values[carrier][product]['states'][state] + '<'",
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
    'GR-G220': {'full_name': 'GR-G220',
                'file_name': 'GR-G220'},
    'GR-G222': {'full_name': 'GR-G222',
                'file_name': 'GR-G222'},
    'GR-G224': {'full_name': 'GR-G224',
                'file_name': 'GR-G224'},
    'BLNY-GR-G224': {'full_name': 'BLNY-GR-G224',
                     'file_name': 'BLNY-GR-G224'}
    }


# Product configuration dictionary

cb_config = {
    'name': 'CB',
    'states': states,
    'plans': plans,
    'xmls_entry': xmls_entry,
    'product_path': 'CB',
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
