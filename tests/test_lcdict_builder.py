__author__ = 'brianoneill'

import logging

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['../..']
from prelogging import LCDict, LCDictBuilderABC

##############################################################################

from test_lcdict_builders_top import LCDictBuilder
import test_lcdict_builder_SubA
import test_lcdict_builder_SubB

##############################################################################
# test(s)
##############################################################################

def test_builder():
    """
    >>> LOG_PATH = '_testlogs/builder'
    >>> lcd = LCDictBuilder.build_lcdict(
    ...     root_level='WARNING',
    ...     log_path=LOG_PATH,
    ...     locking=False,
    ...     attach_handlers_to_root=False)
    >>> lcd.config()

Now log some messages

    >>> root = logging.getLogger()
    >>> loggerA = logging.getLogger('subA')
    >>> loggerB = logging.getLogger('subB')

    >>> root.debug(   "0.")
    >>> root.info(    "1.")
    >>> root.warning( "2.")
    root                : WARNING : 2.
    >>> root.error(   "3.")
    root                : ERROR   : 3.
    >>> root.critical("4.")
    root                : CRITICAL: 4.

    >>> loggerA.debug(   "10.")
    >>> loggerA.info(    "11.")
    >>> loggerA.warning( "12.")
    >>> loggerA.error(   "13.")
    subA                : ERROR   : 13.
    >>> loggerA.critical("14.")
    subA                : CRITICAL: 14.

    >>> loggerB.debug(   "20.")
    >>> loggerB.info(    "21.")
    >>> loggerB.warning( "22.")
    >>> loggerB.error(   "23.")
    >>> loggerB.critical("24.")

Check logfile contents

    >>> import os
    >>> with open(os.path.join(LOG_PATH, 'subA.log')) as f:
    ...     text_A = f.read()
    >>> text_A == ("subA                : ERROR   : 13.\\n"
    ...            "subA                : CRITICAL: 14.\\n")
    True

    >>> with open(os.path.join(LOG_PATH, 'subB.log')) as f:
    ...     text_B = f.read()
    >>> text_B == ("subB                : DEBUG   : 20.\\n"
    ...            "subB                : INFO    : 21.\\n"
    ...            "subB                : WARNING : 22.\\n"
    ...            "subB                : ERROR   : 23.\\n"
    ...            "subB                : CRITICAL: 24.\\n")
    True
    """
    pass


##############################################################################

import doctest

# For unittest integration
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests

if __name__ == "__main__":

    doctest.testmod()   # (verbose=True)
