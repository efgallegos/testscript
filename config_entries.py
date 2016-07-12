"""Dictionaries Configuration"""

import platform
from igo.igo_config_entries import igo_config
from carriers.bankers.config_bankers import bankers_config
#from carriers.lincoln.config_lincoln import lincoln_config


def get_base_path():
    if platform.system() == "Darwin":
        return '/Users/efgallegos/Dropbox/Automation/'
    return 'C:\\zz_EFG\\Dropbox\\Automation\\'


def get_path_separator():
    if platform.system() == "Darwin":
        return'/'
    return '\\'


config_values = {
    'base_path': get_base_path(),
    'os_path_separator': get_path_separator(),
    'igo_common': igo_config,
    'submitted_xmls': 'SUBMITTED_XMLS',
    'carriers': ['bankers'], #,'lincoln'],
    'bankers': bankers_config
    #'lincoln': lincoln_config
    }


def load():
    output_file_path = get_base_path() + 'config_entries.txt'
    with open(output_file_path,'r') as f:
        for line in f:
            new_entry = line.split(',')
            config_values[new_entry[0]] = new_entry[1]

load()
