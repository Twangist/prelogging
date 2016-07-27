__author__ = 'brianoneill'

import os
import sys


def get_locking_pref():
    """Uppercase everything in a copy of sys.argv.
    Return True if a unique prefix of --LOCKING was passed, or or -L;
    return False if a unique prefix of --NOLOCKING was passed, or -N.
    Anything else passed: write help & exit(1).
    Nothing passed -> return True.

    :return: bool -- True => use locking, False => don't.
    """
    argv=[s.upper() for s in sys.argv[1:]]
    if not argv:
        return True     # locking, yes

    help_str =  (
        'Usage:\n'
        '    ./%(PROGNAME)s [--LOCKING | --NOLOCKING]\n'
        '    ./%(PROGNAME)s -h | --help\n'
        ' \n'
        ' Options (case-insensitive, initial letter suffices '
            'e.g. "--L" or "--n" or even -L):\n'
        ' \n'
        '  -L, --LOCKING      Use LockingRotatingFileHandler    [default: True]\n'
        '  -N, --NOLOCKING    Use logging.RotatingFileHandler   [default: False]\n'
        '  -h, --help         Write this help message and exit.\n'
    ) % {'PROGNAME': os.path.basename(sys.argv[0])}

    if len(argv) > 1:
        exit(help_str)

    arg = argv[0]

    if arg[0] != '-':   exit(help_str)

    arg = arg[1:]
    if not arg:         exit(help_str)

    if arg[0] != '-':       # just one initial '-'
        # arg has to be 'L' or 'N'
        if arg == 'L':      return True
        elif arg == 'N':    return False
        # (else fall through to exit)
    else:                   # # two initial '-'s
        # arg[1:] has to be a substring of either 'LOCKING' or 'NOLOCKING'
        arg = arg[1:]
        if arg in 'L':      return True
        elif arg in 'N':    return False
        # (else fall through to exit)

    exit(help_str)

