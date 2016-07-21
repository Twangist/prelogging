__author__ = 'brianoneill'


def check_for_NUL(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    print('%s -- checking for NUL bytes' % filename)
    for i, line in enumerate(lines):
        if 0 in (ord(c) for c in line):
            print("Line %d has NUL" % i)
            print(line)
    print('')

check_for_NUL('mproc_LOCKING.log')
check_for_NUL('mproc_NOLOCKING.log')

'''
'''
