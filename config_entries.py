import logging
import logging.handlers
from config.load_config import load
# create logger with __name__
logger = logging.getLogger('testscript.config')

config_values = {}
logger.debug('testscript.config -> Loading "config_values"...')
load(config_values)
logger.debug('testscript.config -> Dict "config_values" is loaded')
