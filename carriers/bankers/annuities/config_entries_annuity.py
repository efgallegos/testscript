"""Annuity Configuration Dictionaries"""

xmls_entry = {
        'ADDR_State__[0-9]{1,1}[0-5]{0,1}">': "'>' + state + '<'",
        'ADDR_State__[0-9]_itmval">': "'>' + state + '<'",
        'ADDR_State__[0-9]_itmtxt">': "'>' + config_values[carrier][product]['states'][state].upper() + '<'",
        'FullAddress">': "'>123 Main St Exton, ' + state + ' 11111-1111<'",
        'PIFullName">|APPCNT_FullName">': "'>' + state + '_' + plan + ' ' + config_values[carrier][product]['name'] + '<'",
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
        'LA02P': {'full_name': 'LA-02P - Flex',
                  'file_name': 'LA02P'},
        'LA03D': {'full_name': 'LA-03D - 5 and 5',
                  'file_name': 'LA03D'},
        'LA06T': {'full_name': 'LA-06T - Bonus',
                  'file_name': 'LA06T'},
        'LA07C_SG': {'full_name': 'LA-07C - Strong Guarantee',
                     'file_name': 'LA07C_SG'},
        'LA07C_SP': {'full_name': 'LA-07C - Strong Participation',
                     'file_name': 'LA07C_SP'},
        'LA07G_PBIA': {'full_name': 'LA-07G - PBIA',
                         'file_name': 'LA07G_PBIA'},
        'LA07G_GLIA_Q': {'full_name': 'LA-07G - GLIA',
                         'file_name': 'LA07G_GLIA_Q'},
        'LA07G_GLIA_NQ': {'full_name': 'LA-07G - GLIA',
                          'file_name': 'LA07G_GLIA_NQ'},
        'LA07G_PTP': {'full_name': 'LA-07G - PTP With Cap',
                      'file_name': 'LA07G_PTP'},
        'LA08N': {'full_name': 'LA-08N - Alternative',
                  'file_name': 'LA08N'},
        'LA69A_JOINT': {'full_name': 'LA-69A - Joint Life Payout',
                        'file_name': 'LA69A_JOINT'},
        'LA69A_SINGLE': {'full_name': 'LA-69A - Single Life Payout',
                         'file_name': 'LA69A_SINGLE'},
        'BLNY-LA-06T': {'full_name': 'BLNY-LA-06T',
                        'file_name': 'BLNY-LA-06T'},
        'LA-07C(10)_SG': {'full_name': 'LA-07C(10)_SG',
                          'file_name': 'LA-07C(10)_SG'},
        'LA-07C(10)_SP': {'full_name': 'LA-07C(10)_SP',
                          'file_name': 'LA-07C(10)_SP'},
        'LA-07C(10)_PBIA': {'full_name': 'LA-07C(10)_PBIA',
                            'file_name': 'LA-07C(10)_PBIA'},
        'LA-07C(10)_PTP': {'full_name': 'LA-07C(10)_PTP',
                           'file_name': 'LA-07C(10)_PTP'},
        }

# Product configuration dictionary

annuity_config = {
        'name': 'Annuity',
        'states': states,
        'plans': plans,
        'xmls_entry': xmls_entry,
        'product_path': 'Annuity',
        'runs': 'Runs',
        'xml_input_path': 'Input',
        'xml_output_path': 'Output',
        'xml_export_path': 'Export'
        }
