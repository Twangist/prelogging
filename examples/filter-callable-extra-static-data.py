import logging
from prelogging import LCDict

_level_count = 0


def filter_fn(record, **kwargs):
    """ Returns int or bool -- not great practice, but just to distinguish
    which branch of if-then-else was taken.
    """
    filtername = kwargs.get('filtername', '')
    loglevel_to_count = kwargs.get('loglevel_to_count', 0)

    """Suppress odd-numbered messages (records)
    whose level == loglevel_to_count,
    where the "first" message is 0-th hence even-numbered.
    """
    global _level_count
    if record.levelno == loglevel_to_count:
        _level_count += 1
        ret = _level_count % 2      # int
    else:
        ret = True                  # bool

    print("{}: record levelname = {}, _level_count = {}; returning {}".
          format(filtername, record.levelname,
                 _level_count, ret))
    return ret


def config_logging():
    lcd = LCDict(attach_handlers_to_root=True,
                 root_level='DEBUG')
    lcd.add_stdout_handler('console-out',
                           level='DEBUG',
                           formatter='level_msg')
    lcd.add_callable_filter('count_info', filter_fn,
                            # extra, static data
                            filtername='count_info',
                            loglevel_to_count=logging.INFO)
    lcd.attach_root_filters('count_info')

    lcd.config()


if __name__ == '__main__':
    config_logging()

    root = logging.getLogger()

    for i in range(2):
        print("\ni ==", i)
        root.debug(str(i))
        root.info(str(i))
