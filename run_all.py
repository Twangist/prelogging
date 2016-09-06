#!/usr/bin/env python

__author__ = 'brianoneill'

import os
from _execfile import _execfile

_execfile('run_tests.py')       # cwd = prelogging/tests/
os.chdir('..')
_execfile('run_examples.py')    # cwd = examples/
# # print( ">>>>>>>>>>>>> CWD:", os.getcwd() )
# os.chdir('..')
# _execfile('run_examples2.py')
