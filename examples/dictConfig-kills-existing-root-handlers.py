from prelogging import LCDict
import logging

__doc__ = """\
A call to ``logging.config.dictConfig(d)`` kills existing handlers on any logger
that's configured -- even with ``'disable_existing_loggers': False``. The root logger
*always* get configured. Thus, multiple calls to ``logging.config.dictConfig(d)``
leave the root with only the handlers specified for it in the last logging
config dict passed.

The same is of course true of ``LCDict.config()``.

This program demonstrates the phenomenon, using either `prelogging` or pure
`logging` APIs depending on the value of USE_PRELOGGING. Its purpose is to
make the case for LCDictBuilderABC.

More generally it's true that a call to lcd.config() annihilates any handlers
attached to loggers configured in lcd.

Thus, it's chancy to do "collaborative configuration" by having separate "areas"
of a program build their own ``LCDict``\s and each call ``config()`` on them.
Not only does that approach sacrifice `prelogging`'s consistency checking, but it
also opens the door to hard-to-diagnose logging bugs.

"""

USE_PRELOGGING = False


def config_1():
    """ Attach stdout handler to root. """
    if USE_PRELOGGING:
        lcd = LCDict()
        lcd.add_formatter('my-fmt', format='** %(message)s')
        lcd.add_stdout_handler('root-out', formatter='my-fmt')
        lcd.attach_root_handlers('root-out')
        lcd.config()
        # lcd.dump()    # generates the dict below
    else:
        d = {'disable_existing_loggers': False,
             'filters': {},
             'formatters': {'my-fmt': {'class': 'logging.Formatter',
                                       'format': '** %(message)s'}},
             'handlers': {'root-out': {'class': 'logging.StreamHandler',
                                       'formatter': 'my-fmt',
                                       'stream': 'ext://sys.stdout'}},
             'incremental': False,
             'loggers': {},
             'root': {'handlers': ['root-out'], 'level': 'WARNING'},
             'version': 1}
        logging.config.dictConfig(d)


def config_2():
    """ Attach a stdout handler to logger 'L'. """
    if USE_PRELOGGING:
        lcd = LCDict()
        lcd.add_formatter('my-other-fmt',
                          format='%(name)s - %(levelname)s - %(message)s')
        lcd.add_stdout_handler('L-out', formatter='my-other-fmt')
        lcd.add_logger('L', handlers='L-out', propagate=False)
        lcd.config()
        # lcd.dump()    # generates the dict below
    else:
        d = {'disable_existing_loggers': False,
             'filters': {},
             'formatters': {'my-other-fmt': {'class': 'logging.Formatter',
                                             'format': '%(name)s - %(levelname)s - '
                                                       '%(message)s'}},
             'handlers': {'L-out': {'class': 'logging.StreamHandler',
                                    'formatter': 'my-other-fmt',
                                    'stream': 'ext://sys.stdout'}},
             'incremental': False,
             'loggers': {'L': {'handlers': ['L-out'],
                               'level': 'NOTSET',
                               'propagate': False}},
             'root': {'handlers': [], 'level': 'WARNING'},
             'version': 1}
        logging.config.dictConfig(d)


def show_handlers(*loggernames):
    for name in loggernames:
        # Note: r/w ``name`` property of handlers is undoc'd
        print(("%r handlers:" % name),
              [h.name for h in logging.getLogger(name).handlers])


if __name__ == '__main__':
    config_1()
    show_handlers('')
    # '' handlers: ['root-out']

    logging.getLogger('').error('Problems.')
    # to stdout:
    # ** Problems.

    print('--------')

    config_2()
    show_handlers('', 'L')
    # '' handlers: []
    # 'L' handlers: ['L-out']
    # Note: root lost its handler 'root-out'

    logging.getLogger('L').warning("Hey, look out!")
    # To stdout
    # L - WARNING - Hey, look out!
    logging.getLogger('').error('Your bad!')
    logging.getLogger('newlogger').critical('Alert from newlogger')
    # These two lines write to stderr (with LastResort handler):
    # Alert from newlogger
    # Your bad!
