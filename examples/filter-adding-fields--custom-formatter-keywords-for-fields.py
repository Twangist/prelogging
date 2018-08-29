import logging
from prelogging import LCDict
from random import choice

"""
Illustrates adding custom fields and data to logged messages.

Loosely adapts the section
 `Using Filters to impart contextual information <https://docs.python.org/3/howto/logging-cookbook.html#using-filters-to-impart-contextual-information>`_
of The Logging Cookbook.
"""

USER = 0
IP = 1


class FilterThatAddsFields():
    def __init__(self, *args, **kwargs):
        # self.fieldname = kwargs.get('fieldname', '')
        self.datasource = kwargs.get('datasource', None)    # callable

    def filter(self, record):
        """ Add attributes to `record`.
        Attr names must be the same as keywords in format arg of `add_formatter`
        (below).
        """
        record.user = self.datasource(USER)
        record.ip = self.datasource(IP)
        return True


def get_data(keyword):
    """ Source of dynamic data, passed to filter via `add_class_filter` """
    IPS = ['192.0.0.1', '254.15.16.17']
    USERS = ['John', 'Mary', 'Arachnid']

    if keyword == IP:
        return choice(IPS)
    elif keyword == USER:
        return choice(USERS)
    return None


def config_logging():
    lcd = LCDict(attach_handlers_to_root=True,
                 root_level='DEBUG')
    lcd.add_formatter('user_ip_level_msg',
                      format='User: %(user)-10s  IP: %(ip)-15s  %(levelname)-8s  %(message)s')
    lcd.add_stdout_handler('console-out',
                           level='DEBUG',
                           formatter='user_ip_level_msg')
    lcd.add_class_filter('field-adding_filter', FilterThatAddsFields,
                         # extra, static data
                         datasource=get_data)
    lcd.attach_root_filters('field-adding_filter')

    lcd.config()


if __name__ == '__main__':
    LEVELS = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
    config_logging()
    # root = logging.getLogger()

    for i in range(10):
        logging.log(choice(LEVELS), "Msg %d", i)
    '''
    Prints something like (ymwv):
        User: Arachnid    IP: 254.15.16.17     CRITICAL  Msg 0
        User: John        IP: 192.0.0.1        INFO      Msg 1
        User: Mary        IP: 192.0.0.1        DEBUG     Msg 2
        User: John        IP: 192.0.0.1        CRITICAL  Msg 3
        User: Mary        IP: 254.15.16.17     WARNING   Msg 4
        User: John        IP: 254.15.16.17     CRITICAL  Msg 5
        User: John        IP: 254.15.16.17     DEBUG     Msg 6
        User: John        IP: 254.15.16.17     CRITICAL  Msg 7
        User: Arachnid    IP: 192.0.0.1        DEBUG     Msg 8
        User: Mary        IP: 254.15.16.17     ERROR     Msg 9
    '''
