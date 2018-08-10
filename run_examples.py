#!/usr/bin/env python
from __future__ import print_function

__author__ = 'brianoneill'

import sys

from examples import root_logger
from examples import child_logger_main
from examples import child_logger2_main
from examples import mproc
from examples import mproc2
from examples import mproc_approach__locking_handlers
from examples import mproc_approach__queue_handler_logging_thread
from examples import queue_handler_listener
from examples import SMTP_handler_just_one
from examples import SMTP_handler_two
from examples import dateformat
from examples import syslog

from examples.check_for_NUL import check_for_NUL


# cd to examples/
import os
os.chdir('examples/')

root_logger.main()
child_logger_main.main()
child_logger2_main.main()

# ............................
# . Multiprocessing examples .
# ............................

mproc.main(use_locking=True)
mproc.main(use_locking=False)
locking_NULs = check_for_NUL('_log/mproc/mproc_LOCKING.log')       # , verbose=True
nolocking_NULs = check_for_NUL('_log/mproc/mproc_NOLOCKING.log')   # , verbose=True
print("'_log/mproc/mproc_LOCKING.log %s NUL (0) bytes" %
      ('*** does *** contain' if locking_NULs else 'has no'))
print("'_log/mproc/mproc_NOLOCKING.log %s NUL (0) bytes" %
      ('*** does *** contain' if nolocking_NULs else 'has no'))

mproc2.main(use_locking=True)
mproc2.main(use_locking=False)
locking_NULs = check_for_NUL('_log/mproc2/mproc2_LOCKING.log')       # , verbose=True
nolocking_NULs = check_for_NUL('_log/mproc2/mproc2_NOLOCKING.log')   # , verbose=True
print("'_log/mproc2/mproc2_LOCKING.log %s NUL (0) bytes" %
      ('*** does *** contain' if locking_NULs else 'has no'))
print("'_log/mproc2/mproc2_NOLOCKING.log %s NUL (0) bytes" %
      ('*** does *** contain' if nolocking_NULs else 'has no'))


# "deco" examples, each in a subdir
try:
    from examples import mproc_deco
    from examples import mproc_deco_rot_fh
    from examples import mproc_deco_syslog

    mproc_deco.main(use_locking=True)
    mproc_deco.main(use_locking=False)
    locking_NULs = check_for_NUL('_log/mproc_deco/logfile (LOCKING).log')       # , verbose=True
    nolocking_NULs = check_for_NUL('_log/mproc_deco/logfile (NOLOCKING).log')   # , verbose=True
    print("_log/mproc_deco/logfile (LOCKING).log %s NUL (0) bytes"
          % ('*** does *** contain' if locking_NULs else 'has no'))
    print("_log/mproc_deco/logfile (NOLOCKING).log %s NUL (0) bytes"
          % ('*** does *** contain' if nolocking_NULs else 'has no'))

    # --------------------------------------------------------------
    mproc_deco_rot_fh.main(use_locking=True)
    print("*** mproc_deco_rot_fh.py worked with locking.")

    try:
        mproc_deco_rot_fh.main(use_locking=False)
        # Py3.5: None of the workers write anything,
        # logfiles aren't even created for their logged output
    except Exception as e:
        # report this
        print("*** without locking, mproc_deco_rot_fh.py failed:\n"
              "\tException: %s" % str(e))
        # raise

    # --------------------------------------------------------------
    if sys.platform.startswith('darwin'):
        syslog.main()
        mproc_deco_syslog.main()
    else:
        print("*** Syslog examples are for macOS / OS X only; skipping them. ***")

except ImportError as e:
    print("Skipping some examples that require the `deco` package - "
          "https://github.com/alex-sherman/deco",
          file=sys.stderr)

# New kids, non-deco:
dateformat.main()
queue_handler_listener.main()
mproc_approach__locking_handlers.main()
mproc_approach__queue_handler_logging_thread.main()
SMTP_handler_just_one.main()
SMTP_handler_two.main()

