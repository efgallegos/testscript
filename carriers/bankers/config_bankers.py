from carriers.bankers.annuities.config_entries_annuity import annuity_config
from carriers.bankers.spwl.config_entries_spwl import spwl_config
from carriers.bankers.fuwl.config_entries_fuwl import fuwl_config
from carriers.bankers.cb.config_entries_cb import cb_config
from carriers.bankers.stc.config_entries_stc import stc_config
from carriers.bankers.medsupp.config_entries_medsupp import medsupp_config
from carriers.bankers.srlife.config_entries_srlife import srlife_config



bankers_config = {
    'carrier_path': 'Bankers',
    'environments': {
            'qd3': 'http://pipepasstoigo-qd3.ipipeline.com/default.aspx?gaid=5752',
            'qd4': 'http://pipepasstoigo-qd4.ipipeline.com/default.aspx?gaid=5752',
            'qd5': 'http://pipepasstoigo-qd5.ipipeline.com/default.aspx?gaid=5752',
            'td1': 'https://pipepasstoigo-test.ipipeline.com/default.aspx?gaid=5752',
            'td2': 'https://pipepasstoigo-td2.ipipeline.com/default.aspx?gaid=5752',
            'td3': 'https://pipepasstoigo-td3.ipipeline.com/default.aspx?gaid=5752',
            'default': 'http://pipepasstoigo-qd5.ipipeline.com/default.aspx?gaid=5752'
          },
    'users': {
            'qd-user': 'tombqd5',
            'qd-pass': 'password1',
            'td-user': 'bankers05',
            'td-pass': 'bankers05',
            'qd-user-list': ['test5752', 'bankers01', 'bankers02', 'bankers03', 'bankers04', 'bankers05', 'tombqd5'],
            'td-user-list': ['bankers01', 'bankers02', 'bankers03', 'bankers04', 'bankers05'],
           },
    'products': ['annuity', 'spwl', 'fuwl', 'cb', 'stc', 'medsupp', 'srlife'],
    'annuity': annuity_config,
    'spwl': spwl_config,
    'fuwl': fuwl_config,
    'cb': cb_config,
    'stc': stc_config,
    'medsupp': medsupp_config,
    'srlife': srlife_config,
    'log_file': 'run_bankers.log'
}