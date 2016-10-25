__author__ = 'brianoneill'

import logging
try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['../..']
from prelogging import LCDict


from .module import *
from . import module
__all__ = module.__all__


# configure logging
lcd = LCDict()                  # default: disable_existing_loggers=False
lcd.add_null_handler('library-nullhandler')    # default: level='NOTSET'
lcd.add_logger('library', handlers='library-nullhandler', level='INFO')
lcd.config()
