from config_entries import config_values
from collections import deque
from pprint import pprint

master_fields = {
        'field_1':{'values':['value_1','value_2'],
                 'reg_ex':'[azAZ]@[azAZ].com',
                 'lenght':80,
                 'type':'label',
                 'triggers':[('screen','screen_name'),('field','field_name')]
                 },
        'al_field_1':{'values':['value_1','value_2'],
                 'reg_ex':'[azAZ]@[azAZ].com',
                 'lenght':80,
                 'type':'label',
                 'triggers':[('screen','screen_name'),('field','field_name')],
                 'replaces':'field_1',
                 },
    }

master_screens = {'pi': {'actions': ['action_1'],
                         'expected_butons': ['button_1', 'button_2'],
                         'fields': {'al': ['al_field_1'], 
                                    'basic_fields': ['field_1', 'field_2']
                                   },
                         'next_screen': 'screen_2',
                         'prev_screen': None}
           }

master_products = {'FUWE':{
                        '19E':{'basic_screens':['pi','basic_information'],
                               'al':{'screens':['specific_screen_1','specific_screen_2']},
                               'restricted_countries':['pr']
                               }
                        }
                   }


def populate_case(product='fuwl', state='AL', plan='19E'):
    if product in config_values['products'] and plan in config_values[product]['plans'] and state in config_values[product]['states']:
        brd = config_values[product]['brd']
        screens = deque()
        screens.extend(brd['plans'][plan]['screens']['basic_screens'])
        processed_screens = []
        if state in brd['plans'][plan]['screens']:
            screens.extendleft(brd['plans'][plan]['screens']['basic_screens'][state])
        while screens:
            screen = screens.popleft()
            if screen not in master_screens:
                print('Error: screen ', screen, ' not in master_screens')
                continue
            if screen in processed_screens:
                continue
            fields = deque()
            fields.extend(brd['screens'][screen]['fields']['basic_fields'])
            if state in brd['screens'][screen]['fields']:
                fields.extendleft(brd['screens'][screen]['fields'][state])
            while fields:
                field = fields.popleft()
                if field in brd['fields']:
                    print('###########################################')
                    print('screen:', screen)
                    print('field:', field)
                    pprint(brd['fields'][field])
                    if 'replaces' in brd['fields'][field] and brd['fields'][field]['replaces'] in fields:
                        fields.remove(brd['fields'][field]['replaces'])
                        
                else:
                    print('Error: field ', field, ' not in master_fields')
            processed_screens.append(screen)
    else:
        print('Error: Invalid product/state/plan combination. product:', product, ' state: ', state, ' plan:', plan)
