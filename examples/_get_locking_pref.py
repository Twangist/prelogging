__author__ = 'brianoneill'

from docopt import docopt
import os
import sys

def get_locking_pref(version='1'):
    """Uppercase everything in a copy of sys.argv,
    :param args: dict returned by docopt: command line switches
    :return: bool -- True => use locking, False => don't.
    """
    docopt_str =  (
        'Usage:\n'
        '    ./%(PROGNAME)s [--LOCKING | --NOLOCKING]\n'
        '    ./%(PROGNAME)s -h | --help | --version\n'
        '\n'
        'Options (case-insensitive, initial letter suffices e.g. "--L" or "--n" or just "-l" or "-N"):\n'
        '\n'
        '  -L, --LOCKING      Use LockingRotatingFileHandler    [default: True]\n'
        '  -N, --NOLOCKING    Use logging.RotatingFileHandler   [default: False]\n'
    ) % {'PROGNAME': os.path.basename(sys.argv[0])}

    args = docopt(docopt_str,
                  argv=[s.upper() for s in sys.argv[1:]],
                  version=version)

    return not args['--NOLOCKING']
