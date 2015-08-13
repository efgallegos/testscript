"""Universal Life Configuration Dictionaries"""

xmls_entry = {
        'ADDR_State__[0-9]{1,1}[0-5]{0,1}">': "'>' + state + '<'",
        'ADDR_State__[0-9]_itmval">': "'>' + state + '<'",
        'ADDR_State__[0-9]_itmtxt">': "'>' + config_values[carrier][product]['states'][state].upper() + '<'",
        'FullAddress">': "'>123 Main St Exton, ' + state + ' 11111-1111<'",
        'PIFullName">|APPCNT_FullName">': "'>' + state + '_' + plan + ' X ' + config_values[carrier][product]['name'] + '<'",
        'PIFirstName">': "'>' + state + '_' + plan + '<'",
        'PILastName">': "'>' + config_values[carrier][product]['name'] + '<'",
        '"State">|"State_itmval">': "'>' + state + '<'",
        '"State_itmtxt">': "'>' + config_values[carrier][product]['states'][state] + '<'",
        '"PIJurisdiction">|"PIJurisdiction_itmval">': "'>' + state + '<'",
        '"PIJurisdiction_itmtxt">':"'>' + config_values[carrier][product]['states'][state] + '<'",
        'HEY_IT_ALSO_WORKED">': "'>' + state + '<'"
        }

# Product's valid states

states = {
        'AK':'Alaska',
        'AL':'Alabama',
        'AR':'Arkansas',
        'AZ':'Arizona',
        'CA':'California',
        'CO':'Colorado',
        'CT':'Connecticut',
        'DC':'District of Columbia',
        'DE':'Delaware',
        'FL':'Florida',
        'GA':'Georgia',
        'GU':'Guam',
        'HI':'Hawaii',
        'IA':'Iowa',
        'ID':'Idaho',
        'IL':'Illinois',
        'IN':'Indiana',
        'KS':'Kansas',
        'KY':'Kentucky',
        'LA':'Louisianna',
        'MA':'Massachussetts',
        'MD':'Maryland',
        'ME':'Maine',
        'MI':'Michigan',
        'MN':'Minnesota',
        'MO':'Missouri',
        'MP':'Northern Mariana Islands',
        'MS':'Mississippi',
        'MT':'Montana',
        'NC':'North Carolina',
        'ND':'North Dakota',
        'NE':'Nebraska',
        'NH':'New Hampshire',
        'NJ':'New Jersey',
        'NM':'New Mexico',
        'NV':'Nevada',
        #'NY':'New York',
        'OH':'Ohio',
        'OK':'Oklahoma',
        'OR':'Oregon',
        'PA':'Pennsylvania',
        #'PR':'Puerto Rico',
        'RI':'Rhode Island',
        'SC':'South Carolina',
        'SD':'South Dakota',
        'TN':'Tennesse',
        'TX ':'Texas',
        'UT':'Utah',
        'VA':'Virginia',
        'VI':'Virgin Islands (US)',
        'VT':'Vermont',
        'WA':'Washington',
        'WV':'West Virginia',
        'WI':'Wisconsin',
        'WY':'Wyoming',
        }

# Product's valid plans

plans = {
        'UL_LifeCurrent': {'full_name': 'Lincoln LifeCurrent UL',
                           'file_name': 'UL_LifeCurrent'},
        'UL_LIfeGuarantee': {'full_name': 'Lincoln Life LIfeGuarantee UL',
                             'file_name': 'UL_LIfeGuarantee'},
        'UL_LifeReserve': {'full_name': 'Lincoln LifeReserve UL',
                           'file_name': 'UL_LifeReserve'},
        }

# Product configuration dictionary

ul_config = {
        'name': 'Universal Life',
        'states': states,
        'plans': plans,
        'xmls_entry': xmls_entry,
        'product_path': 'UL',
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
