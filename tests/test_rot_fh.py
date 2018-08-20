#!/usr/bin/env python
"""
NON-multiprocessing rotating file handler.
"""

__author__ = 'brianoneill'

import logging
# from pprint import pformat

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['../..']
from prelogging import LCDict


LOG_PATH = '_testlogs/rot_fh/'      # NOTE: directory must exist
LOGFILENAME = 'test_rot_fh.log'

#############################################################################

def config_logging():
    """Create a root logger with a stdout console handler with level=WARNING,
    and a file handler with level=DEBUG.
    Root logger level will be DEBUG.
    """
    # Defaults:
    #   attach_handlers_to_root=False,
    lcd = LCDict(log_path=LOG_PATH,
                 attach_handlers_to_root=True,
                 locking=True,
                 root_level='DEBUG')

    lcd.add_stdout_handler('console', level='WARNING', formatter='msg')

    # add a file handler, which will write to log_path + '/' + logfilename
    lcd.add_formatter(
        'my_file_formatter',
        format='%(levelname)-8s: %(message)s',
    )
    lcd.add_rotating_file_handler(
        'rot_fh',
        filename=LOGFILENAME,
        formatter='my_file_formatter',
        max_bytes = 200,
        backup_count=10,
        mode='w',
    )
    # lcd.dump()           # | DEBUG

    lcd.config()

#############################################################################

def test_rot_fh():
    """
    Use rotating logfiles, check on them

    >>> config_logging()
    >>> logger = logging.getLogger()

    >>> for i in range(4):
    ...     logger.debug("<<<< %d >>>> AAAAAaaaaaBBBBBbbbbbCCCCCcccccDDDDDdddddEEEEEeeeeeFFFFFfffffGGGGGggggg"
    ...                  % i)
    ...     logger.warning("<<<< %d >>>> 0....x....1....x....2....x....3....x....4....x....5....x....6....x...."
    ...                   % i)
    <<<< 0 >>>> 0....x....1....x....2....x....3....x....4....x....5....x....6....x....
    <<<< 1 >>>> 0....x....1....x....2....x....3....x....4....x....5....x....6....x....
    <<<< 2 >>>> 0....x....1....x....2....x....3....x....4....x....5....x....6....x....
    <<<< 3 >>>> 0....x....1....x....2....x....3....x....4....x....5....x....6....x....

Now check file contents
    E.g. test_rot_fh.log contains:
    DEBUG   : <<<< 3 >>>> AAAAAaaaaaBBBBBbbbbbCCCCCcccccDDDDDdddddEEEEEeeeeeFFFFFfffffGGGGGggggg
    WARNING : <<<< 3 >>>> 0....x....1....x....2....x....3....x....4....x....5....x....6....x....
    and test_rot_fh.log.1 contains:
    DEBUG   : <<<< 2 >>>> AAAAAaaaaaBBBBBbbbbbCCCCCcccccDDDDDdddddEEEEEeeeeeFFFFFfffffGGGGGggggg
    WARNING : <<<< 2 >>>> 0....x....1....x....2....x....3....x....4....x....5....x....6....x....
    etc.

    >>> params = [
    ...     # i, fn suffix
    ...     (3, ''),
    ...     (2, '.1'),
    ...     (1, '.2'),
    ...     (0, '.3')
    ... ]
    >>> import os
    >>> for i, fn_suffix in params:
    ...     basic_name = os.path.join(LOG_PATH, LOGFILENAME)
    ...     with open(basic_name + fn_suffix, 'r') as fh:
    ...         file_text = fh.read()
    ...         expected_text = (
    ...             'DEBUG   : <<<< %(num)d >>>> AAAAAaaaaaBBBBBbbbbbCCCCCcccccDDDDDdddddEEEEEeeeeeFFFFFfffffGGGGGggggg\\n'
    ...             'WARNING : <<<< %(num)d >>>> 0....x....1....x....2....x....3....x....4....x....5....x....6....x....\\n'
    ...         ) % dict(num=i)
    ...         print(file_text == expected_text)
    True
    True
    True
    True
    """
    pass

import doctest

# For unittest integration
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests

if __name__ == '__main__':
    doctest.testmod()
