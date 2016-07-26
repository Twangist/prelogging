__author__ = 'brianoneill'

import logging
# from pprint import pformat

try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['../..']
from lcd import LoggingConfigDictEx, ConfiguratorABC

##############################################################################
# ConfiguratorABC used by test_configurator()
##############################################################################

class Configurator(ConfiguratorABC):
    @classmethod
    def add_to_lcd(cls, lcdx: LoggingConfigDictEx):
        """(Virtual) Call ``LoggingConfigDictEx`` methods to augment ``lcdx``.

        :param lcdx: a ``LoggingConfigDictEx``
        """
        lcdx.add_stdout_console_handler('con-out',
                                        formatter='logger_level_msg',
                                        attach_to_root=True)

class ConfiguratorSub(Configurator):
    """A Configurator class to organize a group of subclasses,
    perhaps to share data (class attributes).
    This class does **not** implement ``add_to_lcd``,
    which therefore will **not** be called on it
    (as that would call ``Configurator.add_to_lcd`` a second time).
    """
    pass


class ConfiguratorSubA(ConfiguratorSub):
    @classmethod
    def add_to_lcd(cls, lcdx: LoggingConfigDictEx):
        """(Virtual) Call ``LoggingConfigDictEx`` methods to augment ``lcdx``.

        :param lcdx: a ``LoggingConfigDictEx``
        """
        # Set up a logger 'subA' and a file handler it exclusively uses.
        # Assume the code that uses this module is well-debugged and stable,
        # so we an set logger's level = ``ERROR``.
        #
        #   Messages logged by logger 'subA' will be written
        #       to logfile 'subA.log', and
        #       to root logger (propagate=True).
        #   Root logger will NOT log to 'subA.log' (attach_to_root=False)
        lcdx.add_file_handler('subA-fh',
                              filename='subA.log',
                              formatter='logger_level_msg',
                              attach_to_root=False)
        lcdx.add_logger('subA',
                        handlers='subA-fh',
                        level='ERROR',
                        propagate=True)


class ConfiguratorSubB(ConfiguratorSub):
    @classmethod
    def add_to_lcd(cls, lcdx: LoggingConfigDictEx):
        """(Virtual) Call ``LoggingConfigDictEx`` methods to augment ``lcdx``.

        :param lcdx: a ``LoggingConfigDictEx``
        """
        # Configure so that:
        #   Messages logged by logger 'subB'
        #       will be written to logfile 'subB.log', and
        #       will NOT be written to root logger (propagate=False)
        #
        #   Root logger will NOT log to 'subB.log' (attach_to_root=False)
        # Assume the code that uses this logger is in development,
        # so we'll set level to ``DEBUG``.
        lcdx.add_file_handler('subB-fh',
                              filename='subB.log',
                              formatter='logger_level_msg',
                              attach_to_root=False)
        lcdx.add_logger('subB',
                        handlers='subB-fh',
                        level='DEBUG',
                        propagate=False)

##############################################################################
# test(s)
##############################################################################

def test_configurator():
    """
    >>> LOG_PATH = '_testlogs/configurator'

    >>> Configurator.configure_logging(
    ...     root_level='WARNING',
    ...     log_path=LOG_PATH,
    ...     locking=False,
    ...     attach_handlers_to_root=False)

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
