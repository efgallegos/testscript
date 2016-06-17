from datetime import date

fields = {'field_1': {'type': 'label',
                      'valid_options': ['value_1', 'value_2'],
                      'reg_ex': '[azAZ]@[azAZ].com',
                      'lenght': None,
                      'type': 'label',
                      'triggers': [('screen', 'screen_name'), ('field', 'field_name')]
                      },
          'field_1': {
                      'valid_values': ['value_1', 'value_2'],
                      'reg_ex': '[azAZ]@[azAZ].com',
                      'lenght': 80,
                      'type': 'label',
                      'triggers': [('screen', 'screen_name'), ('field', 'field_name')],
                      'replaces': 'field_1',
                      },
          'case_info_lblStatus': {
                      'screen': 'CASE_INFORMATION',
                      'type': 'label',
                      'id': 'lblStatus',
                      'name': None,
                      'text': 'Started',
                      'valid_values': ['Started',],
                      },
          'case_info_lblDateModified': {
                      'screen': 'CASE_INFORMATION',
                      'type': 'label',
                      'id': 'lblDateModified',
                      'name': None,
                      'text': date.today().strftime("%m/%d/%y"),
                      },

           'case_info_btnContinue':{
                      'screen': 'CASE_INFORMATION',
                      'type': 'button',
                      'id': 'btnContinue',
                      'name': 'btnContinue',
                      'text': 'Save Changes'
                      },
           'case_info_btnFindAvailableProducts':{
                      'screen': 'CASE_INFORMATION',
                      'type': 'button',
                      'id': 'btnFindAvailableProducts',
                      'name': 'btnFindAvailableProducts',
                      'text': 'Find Available Products'
                      },
          }

tabs = {
    'CASE_INFORMATION': {'actions': ['action_1'],
                         'expected_butons': ['button_1', 'button_2'],
                         'fields': {'basic': ['field_1', 'field_2'],
                                    'state_specific': {'al': ['al_field_1'],
                                                       }
                                    },
                        },
}

screens = {
    'CASE_INFORMATION': {'actions': ['action_1'],
                         'expected_butons': ['button_1', 'button_2'],
                         'fields': {'basic': ['field_1', 'field_2'],
                                    'state_specific': {'al': ['al_field_1'],
                                                       }
                                    },
                         'next_screen': 'DEFINITION_OF_REPLACEMENT',
                         'prev_screen': None},
    'PRELIMINARY_INFORMATION_SHEET': {'actions': ['action_1'],
                                      'expected_butons': ['button_1', 'button_2'],
                                      'fields': {'al': ['al_field_1'],
                                                 'basic': ['field_1', 'field_2']
                                                 },
                                      'next_screen': 'DEFINITION_OF_REPLACEMENT',
                                      'prev_screen': None},
    'DEFINITION_OF_REPLACEMENT': {'actions': ['action_1'],
                                  'expected_butons': ['button_1', 'button_2'],
                                  'fields': {'al': ['al_field_1'],
                                             'basic': ['field_1', 'field_2']
                                             },
                                  'next_screen': 'NEW_YORK_VERIFICATION',
                                  'prev_screen': 'PRELIMINARY_INFORMATION_SHEET'},
    'NEW_YORK_VERIFICATION': {'actions': ['action_1'],
                              'expected_butons': ['button_1', 'button_2'],
                              'fields': {'al': ['al_field_1'],
                                         'basic': ['field_1', 'field_2']
                                         },
                              'next_screen': 'PROPOSED_INSURED',
                              'prev_screen': 'DEFINITION_OF_REPLACEMENT'},
    'PROPOSED_INSURED': {'actions': ['action_1'],
                         'expected_butons': ['button_1', 'button_2'],
                         'fields': {'al': ['al_field_1'],
                                    'basic': ['field_1', 'field_2']
                                    },
                         'next_screen': 'PROPOSED_INSURED_CONT',
                         'prev_screen': 'NEW_YORK_VERIFICATION'},
}

plans = {
    '19E': {'full_name': 'ClearVantage UL (19E)',
            'file_name': '19E',
            'screens': {'basic_screens': ['pi', 'basic_information'],
                        'al': ['specific_screen_1', 'specific_screen_2']
                        },
            'restricted_states': ['NY', 'PR']
            },
    '20E': {'full_name': 'TurningPoint UL (20E)',
            'file_name': '20E',
            'screens': {'basic_screens': ['pi', 'basic_information'],
                        'NY': ['PRELIMINARY_INFORMATION_SHEET', 'DEFINITION_OF_REPLACEMENT']
                        },
            'restricted_states': ['PR']
            },
    '14X': {'full_name': 'Innovative Life (14X)',
            'file_name': '20E',
            'screens': {'basic_screens': ['pi', 'basic_information'],
                        'al': ['specific_screen_1', 'specific_screen_2']
                        },
            'restricted_states': ['IA', 'NH', 'NY', 'PR'],
            },
    'L-5Z1': {'full_name': 'ReliaTerm (L-5Z1)',
              'file_name': '20E',
              'screens': {'basic_screens': ['pi', 'basic_information'],
                           'al': ['specific_screen_1', 'specific_screen_2']
                          },
              'restricted_states': ['NY', 'PR'],
              },
    '10S': {'full_name': 'SecureView (10 Series)',
            'file_name': '20E',
            'screens': {'basic_screens': ['pi', 'basic_information'],
                        'al': ['specific_screen_1', 'specific_screen_2']
                        },
            'restricted_states': ['PR'],
            },
    '14V': {'full_name': 'Innovative Life (14V)',
            'file_name': '20E',
            'screens': {'basic_screens': ['pi', 'basic_information'],
                        'al': ['specific_screen_1', 'specific_screen_2']
                        },
            'restricted_states': ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT',
                                  'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL',
                                  'IN', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
                                  'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
                                  'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
                                  'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN',
                                  'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI',
                                  'WY'],
            }
}

brd = [fields, screens, plans]
