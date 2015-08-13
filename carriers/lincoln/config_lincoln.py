from carriers.lincoln.sul.config_entries_sul import sul_config
from carriers.lincoln.ul.config_entries_ul import ul_config
from carriers.lincoln.term.config_entries_term import term_config


lincoln_config = {
    'carrier_path': 'Lincoln',
    'environments': {
            'qd3': 'https://pipepasstoigo-qd3.ipipeline.com/default.aspx?gaid=3080',
            'qd4': 'https://pipepasstoigo-qd4.ipipeline.com/default.aspx?gaid=3080',
            'td1':'',
            'td3':'',
            'default': 'https://pipepasstoigo-qd4.ipipeline.com/default.aspx?gaid=3080'
          },
    'users': {
            'qd-user': 'test3080',
            'qd-pass': 'test3080',
            'td-user': '',
            'td-pass': ''
           },
    'products': ['sul','ul','term'],
    'sul': sul_config,
    'ul': ul_config,
    'term': term_config
}