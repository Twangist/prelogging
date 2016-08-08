__author__ = 'brianoneill'

import logging
try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['..']
from lcd import LCDEx


def main():
    """
    Not a test because... your mileage *will* vary (hard to test).
    """
    lcdx = LCDEx(attach_handlers_to_root=True)

    # style='%' is the default, & could be omitted
    lcdx.add_formatter('fmtr1',
                       format='%(asctime)s %(levelname)s: %(message)s',
                       dateformat='%H:%M:%S')

    lcdx.add_formatter('fmtr2',
                       format='%(asctime)s -- %(message)s',
                       datefmt='%y.%m.%d')

    lcdx.add_stdout_handler('con1', formatter='fmtr1')
    lcdx.add_stdout_handler('con2', formatter='fmtr2')

    lcdx.config()

    logging.getLogger().warning('Danger, Will Robinson!')
    # Prints, for example:
    #     02:32:07 WARNING: Danger, Will Robinson!
    #     16.08.08 -- Danger, Will Robinson!

if __name__ == "__main__":
    main()
