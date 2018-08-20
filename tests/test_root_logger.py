__author__ = 'brianoneill'

import sys
sys.path[0:0] = ['../..']

from prelogging import LCDict

#############################################################################

def logging_config(log_path, logfilename=''):
    """Create a root logger with a stdout console handler with level=INFO,
    and, if logfilename is not empty, a file handler with level=DEBUG.
    Root logger level will be INFO.
    """
    # . Just for coverage:
    # .     root_level='CRITICAL')
    # . Temporary, cuz of lcd.set_logger_level(...) below.
    lcd = LCDict(log_path=log_path,
                 attach_handlers_to_root=True,
                 root_level='CRITICAL')
    lcd.add_stdout_handler('con', level='WARNING', formatter="msg")

    lcd.set_logger_level(None, 'INFO')    # . coverage ho'

    if logfilename:
        # add a file handler, which will write to log_path + '/' + logfilename
        # Of course, we don't have to add a formatter, we could just
        # use formatter='level_msg' in add_file_handler(...)
        lcd.add_formatter(
            'my_file_formatter',
            format='%(levelname)-8s: %(message)s'
        )
        # Defaults:
        #   level='DEBUG',
        lcd.add_file_handler(
            'app_file',
            filename=logfilename,
            mode='w',
            locking=True,                   # for kicks 'n' coverage
            formatter='my_file_formatter',
        )
    # lcd.dump()           # | DEBUG

    lcd.config()

#############################################################################

def test_root_logger():
    """
    >>> import logging

    >>> LOG_PATH = '_testlogs'       # NOTE: directory should already exist
    >>> logfilename = 'logfile.log'

    >>> logging_config(LOG_PATH, logfilename)

    >>> logger = logging.getLogger()
    >>> logger.debug("1. Message not logged")          # logger level is INFO
    >>> logger.warning("2. Log to both file and console")
    2. Log to both file and console

    >>> logger.setLevel(logging.DEBUG)
    >>> logger.debug("3. Log to file only")
    >>> logger.warning("4. Log to both file and console")
    4. Log to both file and console

    # _testlogs/logfile.log contains these lines, flush left:
    #   WARNING : 2. Log to both file and console
    #   DEBUG   : 3. Log to file only
    #   WARNING : 4. Log to both file and console
    >>> import os
    >>> with open(os.path.join(LOG_PATH, logfilename)) as fh:
    ...     logfile = fh.read()
    >>> expected = ("WARNING : 2. Log to both file and console\\n"
    ...             "DEBUG   : 3. Log to file only\\n"
    ...             "WARNING : 4. Log to both file and console\\n")
    >>> logfile == expected
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
