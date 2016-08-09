"""MedSupp Configuration Dictionaries"""

xmls_entry = {
    '"OTHINS_State__[0-9]">': "'>' + state + '<'",
    '"EFT_States"|"EFT_States_itmval"|"PIADDR_State"|"PIADDR_State_itmval"|"PIJurisdiction"|"PIJurisdiction_itmval"|"State"|"State_itmval"': "'>' + state + '<'",
    '"AGENT_ADDR_State"|"AGENT_ADDR_State_itmval"|"pdfBillingState"|"PIBILLING_ADDR_State"|"PIBILLING_ADDR_State_itmval"': "'>' + state + '<'",
    '"EFT_States_itmtxt"|"PIADDR_State_itmtxt"': "'>' + config_values[carrier][product]['states'][state].upper() + '<'",
    '"PIJurisdiction_itmtxt"|"State_itmtxt"': "'>' + config_values[carrier][product]['states'][state] + '<'",
    '"PIFullAddress">': "'>123 Main St Exton, ' + state + ' 12345<'",
    '"AGENT_FullAddress">': "'>123 Agent St Exton, ' + state + ' 12345<'",
    '"pdfAGENT_FullNameAddress">': "'>Agent Name 123 Agent St Exton, ' + state + ' 12345<'",
    '"PIFirstName"|"pdfPIAdjFirstName">': "'>' + state + '_' + plan + '<'",
    '"PILastName"|"pdfPIAdjLastName">': "'>' + config_values[carrier][product]['name'] + '<'",
    '"PIFullName">|"APPCNT_FullName">': "'>' + state + '_' + plan + ' ' + config_values[carrier][product]['name'] + '<'",
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
    # 'MA': 'Massachusetts',
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
    'MEDSUPP': {'full_name': 'Medicare Supplement',
                'file_name': 'MEDSUPP'},
    'CPL-GR-A830': {'full_name': 'Medicare Supplement',
                'file_name': 'CPL-GR-A830'},
    'CPL-GR-A820': {'full_name': 'Medicare Supplement',
                'file_name': 'CPL-GR-A820'}
    }

# Product configuration dictionary

medsupp_config = {
    'name': 'MedSupp',
    'states': states,
    'plans': plans,
    'xmls_entry': xmls_entry,
    'product_path': 'MedSupp',
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
