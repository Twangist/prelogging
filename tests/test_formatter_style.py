__author__ = 'brianoneill'

import sys
sys.path[0:0] = ['../..']          # prepend
from lcd import LCDEx
import logging
from lcd.six import PY2

if PY2:
    def test_formatter_style():
        """
        """
        pass
else:
    def test_formatter_style():
        """
        >>> lcdx = LCDEx(attach_handlers_to_root=True)

        >>> # style='%' is the default, & could be omitted
        >>> _ = lcdx.add_formatter('testform-%',
        ...                        format='%(levelname)s: %(name)s: %(message)s',
        ...                        style='%')
        >>> _ = lcdx.add_formatter('testform-{',
        ...                        format='{levelname}: {name}: {message}',
        ...                        style='{')
        >>> _ = lcdx.add_formatter('testform-$',
        ...                        format='$levelname: $name: $message',
        ...                        style='$')

        >>> _ = lcdx.add_stdout_handler('con-%', formatter='testform-%')
        >>> _ = lcdx.add_stdout_handler('con-{', formatter='testform-{')
        >>> _ = lcdx.add_stdout_handler('con-$', formatter='testform-$')
        >>> _ = lcdx.config()

        >>> root = logging.getLogger()
        >>> root.warning('Hi there')
        WARNING: root: Hi there
        WARNING: root: Hi there
        WARNING: root: Hi there
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
