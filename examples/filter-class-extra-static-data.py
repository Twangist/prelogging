import logging
from prelogging import LCDict


class CountAndSquelchOdd():
    def __init__(self, *args, **kwargs):
        self.level_count = 0

        print(kwargs)
        # {'filtername': _____, 'loglevel_to_count': nnn}
        self.filtername = kwargs.get('filtername', '')
        self.loglevel_to_count = kwargs.get('loglevel_to_count', 0)

    def filter(self, record):
        """Suppress odd-numbered messages (records)
        whose level == self.loglevel_to_count,
        where the "first" message is 0-th hence even-numbered.

        Returns int or bool -- not great practice, but just to distinguish
        which branch of if-then-else was taken.
        """
        if record.levelno == self.loglevel_to_count:
            self.level_count += 1
            ret = self.level_count % 2          # int
        else:
            ret = True                          # bool

        print("{:11s} > record levelname = {}, self.level_count = {}; returning {}".
              format(self.filtername, record.levelname,
                     self.level_count, ret))
        return ret

def config_logging():
    lcd = LCDict(attach_handlers_to_root=True,
                 root_level='DEBUG')
    lcd.add_stdout_handler('console-out',
                           level='DEBUG',
                           formatter='level_msg')
    lcd.add_class_filter('count_debug', CountAndSquelchOdd,
                         # extra, static data
                         filtername='count_debug',
                         loglevel_to_count=logging.DEBUG)
    lcd.add_class_filter('count_info', CountAndSquelchOdd,
                         # extra, static data
                         filtername='count_info',
                         loglevel_to_count=logging.INFO)
    lcd.attach_root_filters('count_debug', 'count_info')

    lcd.config()

if __name__ == '__main__':
    config_logging()
    root = logging.getLogger()

    for i in range(2):
        print("\ni ==", i)
        root.debug(str(i))
        print("---")
        root.info(str(i))
