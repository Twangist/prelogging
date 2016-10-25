__author__ = 'brianoneill'

import logging
import sys

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['../..']
from prelogging import LCDict


info_count = 0
debug_count = 0

# Classic filters are subclasses of logging.Filter:

class CountInfoSquelchOdd(logging.Filter):
    def filter(self, record):
        """Suppress odd-numbered messages (records) whose level == INFO,
        where the "first" message is the 0-th hence is even-numbered.

        :param self: (unused)
        :param record: logging.LogRecord
        :return: bool -- True ==> let record through, False ==> squelch
        """
        global info_count
        if record.levelno == logging.INFO:
            info_count += 1
            return info_count % 2
        else:
            return True

# A filter can also be a function:

def count_debug_allow_2(record):
    """Allow only the first two DEBUG-level messages to "get through".

    :param record: ``logging.LogRecord``
    :return: ``bool`` -- True ==> let record through, False ==> squelch
    """
    global debug_count
    if record.levelno == logging.DEBUG:
        debug_count += 1
        return debug_count <= 2
    else:
        return True


def test_xxx_filter():
    """
    >>> global info_count
    >>> global debug_count
    >>> info_count = 0
    >>> debug_count = 0

    >>> lcd = LCDict(
    ...     attach_handlers_to_root=True,
    ...     root_level='DEBUG')

    >>> _ = lcd.add_stdout_handler(
    ...     'console',
    ...     level='DEBUG',
    ...     formatter='level_msg')

Configure the root logger to use both filters shown above:

    >>> _ = lcd.add_class_filter('count_i', CountInfoSquelchOdd)
    >>> _ = lcd.add_callable_filter('count_d', count_debug_allow_2)
    >>> _ = lcd.attach_root_filters('count_i', 'count_d')

    # lcd.dump()      # | DEBUG comment out

    >>> lcd.config()

Now use the root logger:

    >>> root = logging.getLogger()
    >>> for i in range(5):
    ...     root.debug(str(i))
    ...     root.info(str(i))
    DEBUG   : 0
    INFO    : 0
    DEBUG   : 1
    INFO    : 2
    INFO    : 4

*** NOTE Filters on the root will hang around, even into other tests!!!! ***

Do build_lcd() for, say, test_root_logger.py and get the root logger:
it will still have the two filters!, from the above/this module.

Simply ensuring that the default is used ("disable_existing_loggers=True")
doesn't remove the filters on the root.

SO, delete them manually:

    >>> root = logging.getLogger()
    >>> filters = root.filters[:]
    >>> for f in filters:
    ...     root.removeFilter(f)

    """
    pass

#############################################################################
import doctest

# For unittest integration
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests

if __name__ == '__main__':
    doctest.testmod()
