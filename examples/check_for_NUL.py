#!/usr/bin/env python

__author__ = 'brianoneill'


def check_for_NUL(filename, verbose=False):
    """
    :param filename: file to check for ASCII 0 bytes
    :param verbose: if true, print stuff; if not, don't.
    :return: bool, True iff filename contains NUL
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    if verbose: print('%s -- checking for NUL bytes' % filename)
    has_NULs = False
    for i, line in enumerate(lines):
        if 0 in (ord(c) for c in line):
            has_NULs = True
            if verbose:
                print("Line %d has NUL" % i)
                print(line)
    if verbose: print()

    return has_NULs

if __name__ == '__main__':
    import sys
    check_for_NUL(sys.argv[1], verbose=True)

