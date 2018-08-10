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

check_for_NUL('mproc2_LOCKING.log')
check_for_NUL('mproc2_NOLOCKING.log')

'''
mproc2_LOCKING.log -- checking for NUL bytes

mproc2_NOLOCKING.log -- checking for NUL bytes
Line 51 has NUL
'''
