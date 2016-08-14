__author__ = 'brianoneill'

import logging
try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['../..']
from lcd import LCDEx

from .module import do_something, do_something_else
__all__ = ['do_something', 'do_something_else']

# configure logging
lcdx = LCDEx()                  # default: disable_existing_loggers=False
lcdx.add_null_handler('library-nullhandler')    # default: level='NOTSET'
lcdx.add_logger('library', handlers='library-nullhandler', level='INFO')
lcdx.config()
