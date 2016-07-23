__author__ = 'brianoneill'

import sys
sys.path[0:0] = ['../..']

from lcd import LoggingConfigDictEx

#############################################################################

def configure_logging(log_path, logfilename=''):
    """Create a root logger with a stdout console handler with level=INFO,
    and, if logfilename is not empty, a file handler with level=DEBUG.
    Root logger level will be INFO.
    """
    lcd_ex = LoggingConfigDictEx(log_path=log_path,
                                 add_handlers_to_root=True,
                                 root_level='CRITICAL')     # . temporary; cuz of lcd_ex.set_logger_level(...) below
                                 # root_level='INFO')
    lcd_ex.add_stdout_console_handler('con', formatter="minimal")

    lcd_ex.set_logger_level(None, 'INFO')    # . coverage ho'

    if logfilename:
        # add a file handler, which will write to log_path + '/' + logfilename
        lcd_ex.add_formatter(
            'my_file_formatter',
            format='%(levelname)-8s: %(message)s'
        )
        # Defaults:
        #   level='DEBUG',
        lcd_ex.add_file_handler(
            'app_file',
            filename=logfilename,
            formatter='my_file_formatter',
        )
    # lcd_ex.dump()           # | DEBUG

    lcd_ex.config()

#############################################################################

def test_root_logger():
    """
    >>> import logging

    >>> LOG_PATH = '_testlogs'       # NOTE: directory should already exist
    >>> logfilename = 'logfile.log'

    >>> configure_logging(LOG_PATH, logfilename)

    >>> logger = logging.getLogger()
    >>> logger.debug("1. Message not logged")          # logger level is WARNING
    >>> logger.warning("2. Log to both file and console")
    2. Log to both file and console

    >>> logger.setLevel(logging.DEBUG)
    >>> logger.debug("3. Log to file only")
    >>> logger.warning("4. Log to both file and console")
    4. Log to both file and console

    # _log/root_loggelogfile.log contains these lines, flush left:
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