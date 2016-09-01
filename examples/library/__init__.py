__author__ = 'brianoneill'

import logging
try:
    import logging_config
except ImportError:
    import sys
    sys.path[0:0] = ['../..']
from logging_config import LCDict

from .module import do_something, do_something_else
__all__ = ['do_something', 'do_something_else']

# configure logging
lcd = LCDict()                  # default: disable_existing_loggers=False
lcd.add_null_handler('library-nullhandler')    # default: level='NOTSET'
lcd.add_logger('library', handlers='library-nullhandler', level='INFO')
lcd.config()
