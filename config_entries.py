"""Dictionaries Configuration"""

import platform
from igo.igo_config_entries import igo_config
from bankers.annuities.config_entries_annuity import annuity_config
from bankers.spwl.config_entries_spwl import spwl_config
from bankers.fuwl.config_entries_fuwl import fuwl_config
from bankers.cb.config_entries_cb import cb_config
from bankers.stc.config_entries_stc import stc_config
from bankers.medsupp.config_entries_medsupp import medsupp_config
from bankers.srlife.config_entries_srlife import srlife_config


def get_base_path():
    if platform.system() == "Darwin":
        return '/Users/efgallegos/Dropbox/Automation/Bankers/'
    return 'C:\\zz_EFG\\Dropbox\\Automation\\Bankers\\'


def get_path_separator():
    if platform.system() == "Darwin":
        return'/'
    return '\\'


config_values = {
    'qd3': 'http://pipepasstoigo-qd3.ipipeline.com/default.aspx?gaid=5752',
    'qd4': 'http://pipepasstoigo-qd4.ipipeline.com/default.aspx?gaid=5752',
    'qd5': 'http://pipepasstoigo-qd5.ipipeline.com/default.aspx?gaid=5752',
    'td1': 'https://pipepasstoigo-test.ipipeline.com/default.aspx?gaid=5752',
    'td2': 'https://pipepasstoigo-td2.ipipeline.com/default.aspx?gaid=5752',
    'td3': 'https://pipepasstoigo-td3.ipipeline.com/default.aspx?gaid=5752',
    'qd-user': 'test5752',
    'qd-pass': 'test5752',
    'td-user': 'bankers02',
    'td-pass': 'bankers02',
    # 'base_mac': '/Users/efgallegos/Dropbox/Automation/Bankers/',
    # 'base_win': 'C:\\zz_EFG\\Dropbox\\Automation\\Bankers\\',
    'base_path': get_base_path(),
    'os_path_separator': get_path_separator(),
    'igo_common': igo_config,
    'products': ['annuity',
                 'spwl',
                 'fuwl',
                 'cb',
                 'stc',
                 'medsupp',
                 'srlife'],
    'annuity': annuity_config,
    'spwl': spwl_config,
    'fuwl': fuwl_config,
    'cb': cb_config,
    'stc': stc_config,
    'medsupp': medsupp_config,
    'srlife': srlife_config,
    }
