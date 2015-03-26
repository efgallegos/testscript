"""STC Configuration Dictionaries"""

xmls_entry = {
     '': '',
     }


"""
<Data Name="ADDR_State">AL</Data>
<Data Name="ADDR_State_itmtxt">ALABAMA</Data>
<Data Name="ADDR_State_itmval">AL</Data>
<Data Name="AGENT_ADDR_State">PA</Data>
<Data Name="AGENT_ADDR_State_itmtxt">PENNSYLVANIA</Data>
<Data Name="AGENT_FullAddress">123 Agent St Exton, AK 11111</Data>
<Data Name="AGENT_pdf_FullAddress">Address Line 1, Address 2, Exton, PA, 111111111</Data>
<Data Name="AGENT2_ADDR_State">AK</Data>
<Data Name="AGENT2_ADDR_State_itmtxt">ALASKA</Data>
<Data Name="AGENT2_ADDR_State_itmval">AK</Data>
<Data Name="AGENT2_FullAddress">123 Second St Exton, AK 11111</Data>
<Data Name="BILLING_ADDR_State">AK</Data>
<Data Name="BILLING_ADDR_State_itmtxt">ALASKA</Data>
<Data Name="BILLING_ADDR_State_itmval">AK</Data>
<Data Name="EFT_State">AL</Data>
<Data Name="EFT_State_itmtxt">ALABAMA</Data>
<Data Name="EFT_State_itmval">AL</Data>
<Data Name="pdfAGENT_FullNameAddress">Agent Name 123 Agent St Exton, AK 11111</Data>
<Data Name="PIADDR_State">AL</Data>
<Data Name="PIFullAddress">123 Main St Exton, AL 11111</Data>

<Data Name="PIFullName">STC X GR-N560 Sr</Data>
<Data Name="pdfReversePIName">GR-N560, STC X</Data>
<Data Name="PILastName">GR-N560</Data>  
<Data Name="PIFirstName">STC</Data>

<Data Name="PIJurisdiction">AL</Data>
<Data Name="PIJurisdiction_itmtxt">Alabama</Data>
<Data Name="PIJurisdiction_itmval">AL</Data>
<Data Name="ProducerAddressState">PA</Data>
<Data Name="ProducerAddressStateTC">PA</Data>
<Data Name="ProducerCityStateZip">Exton, PA 11111-1111</Data>
<Data Name="State">AL</Data>
<Data Name="State_itmtxt">Alabama</Data>
<Data Name="State_itmval">AL</Data>

<Data Name="TPState">AL</Data>
<Data Name="TPState_itmtxt">ALABAMA</Data>
<Data Name="TPState_itmval">AL</Data>

<Data Name="CaseDescription">State=AL</Data>
"""

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
