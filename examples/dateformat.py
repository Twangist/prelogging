__author__ = 'brianoneill'

import logging
try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['..']
from prelogging import LCDict


def main():
    """
    Not a test because... your mileage *will* vary (hard to test).
    """
    lcd = LCDict(attach_handlers_to_root=True)

    # style='%' is the default
    lcd.add_formatter('fmtr1',
                       format='%(asctime)s %(levelname)s: %(message)s',
                       dateformat='%H:%M:%S')

    lcd.add_formatter('fmtr2',
                       fmt='%(asctime)s -- %(message)s',
                       datefmt='%Y.%m.%d')  # %Y: 4-digit years; %y: 2-digit years

    lcd.add_stdout_handler('con1', formatter='fmtr1')
    lcd.add_stdout_handler('con2', formatter='fmtr2')

    lcd.config()

    logging.getLogger().warning('Danger, Will Robinson!')
    # Prints, for example:
    #     02:32:07 WARNING: Danger, Will Robinson!
    #     2018.08.08 -- Danger, Will Robinson!

if __name__ == "__main__":
    main()
