import sys
import argparse
import logging
import logging.handlers

LOG_FILENAME = 'testscript.log'

# create logger with __name__
logger = logging.getLogger('testscript')
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create file handler
fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1018576*5, backupCount=7)
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handler to the logger
logger.addHandler(ch)
logger.addHandler(fh)


def ts(args):
    parser = argparse.ArgumentParser(description='This is the "TestScript" framework for iGo testing')

    subparsers = parser.add_subparsers(help='commands')

    # A config command
    config_parser = subparsers.add_parser('config', help='Upload/Rebuild configuration parameters')

    group = config_parser.add_mutually_exclusive_group()
    group.add_argument('-b', '--build', action="store_true", default=False, help='Build configuration dictionary')
    group.add_argument('-u', '--upload', action="store_true", default=False, help='Upload Carrier product/plan/state matrix')

    config_parser.add_argument('-f', '--file', action="store", default=False, help='Carrier product/plan/state matrix file path')
    config_parser.add_argument('-c', '--carrier', action="store", default='bankers', help='Carrier name')

    # A igo command
    igo_parser = subparsers.add_parser('igo', help='iGo Common functionality')
    igo_parser.add_argument('-i', '--import', action="store_true", default=False, help='Import Case into iGo')
    igo_parser.add_argument('-l', '--lock', action="store_true", default=False, help='Lock Existing Case in iGo')

    group_variables = igo_parser.add_argument_group('iGo parameters')
    group_variables.add_argument('carrier', action="store", help='Carrier name')
    group_variables.add_argument('-e', '--environmet', action="store", default='qd3', help='Environment name')
    group_variables.add_argument('-u', '--username', action="store", default='Eduardo', help='Username')
    group_variables.add_argument('-p', '--password', action="store", default='Eduardo1', help='Password')
    group_variables.add_argument('product', action="store", help='Product name')
    group_variables.add_argument('state', action="store", help='State (XX) name')
    group_variables.add_argument('plan', action="store", help='Plan name')

    args = parser.parse_args()

    print(args)

if __name__ == "__main__":
    ts(sys.argv[1:])