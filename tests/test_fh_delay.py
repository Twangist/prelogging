__author__ = 'brianoneill'

import sys
sys.path[0:0] = ['../..']          # prepend

from prelogging import LCDict

#############################################################################

def logging_config(log_path, logfilename=''):
    """Create a root logger with a stdout console handler with level=DEBUG,
    and, if logfilename is not empty, a file handler with level=INFO *and*
    with delay=True, so that the logfile is created only when written to.
    Root logger level will be DEBUG.
    """
    lcd = LCDict(log_path=log_path,
                 root_level='DEBUG',
                 attach_handlers_to_root=True)
    lcd.add_stdout_handler('con', formatter='msg', level='DEBUG')

    if logfilename:
        # add a file handler, which will write to log_path + '/' + logfilename
        lcd.add_formatter(
            'my_file_formatter',
            format='%(levelname)-8s: %(message)s'
        )
        # Defaults:
        #   level='DEBUG',
        #   attach_to_root=True
        lcd.add_file_handler(
            'app_file',
            filename=logfilename,
            formatter='my_file_formatter',
            level='INFO',
            mode='w',       # default, just as a reminder
            delay=True      # default: False
        )
    # lcd.dump()           # | DEBUG

    lcd.config()

#############################################################################

def test_fh_delay():
    """
    >>> import logging
    >>> import os
    >>> import subprocess

    >>> LOG_PATH = '_testlogs'       # NOTE: directory should already exist
    >>> logfilename = 'logfile_delay.log'

    >>> # make sure logfile doesn't exist!
    >>> fullfn = os.path.join(LOG_PATH, logfilename)
    >>> if os.path.exists(fullfn):
    ...     p = subprocess.Popen(['rm', fullfn])
    ...     # _ = p.wait(5)   # seconds
    ...     _ = p.wait()   # Py 2.7

    >>> logging_config(LOG_PATH, logfilename)

    # Nothing written, so file shouldn't exist:
    >>> not os.path.exists(fullfn)
    True

    # Write something at level DEBUG --
    # we should see it in stdout but file should still not exist (handler level is INFO)
    >>> logger = logging.getLogger()
    >>> logger.debug("1. Message logged to console")          # logger level & console level is DEBUG
    1. Message logged to console

    >>> not os.path.exists(fullfn)
    True

    # Write something at level INFO --
    # we should see it in stdout AND in the file, which will be created:
    >>> logger.info("2. Log to both file and console")
    2. Log to both file and console

    >>> os.path.exists(fullfn)
    True

    # logfile contains one line, flush left:
    >>> with open(fullfn) as fh:
    ...     logfile = fh.read()
    >>> expected = "INFO    : 2. Log to both file and console\\n"
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
