__author__ = 'brianoneill'

from unittest import TestCase
import logging

from lcd import LoggingConfigDict

import sys
import io   # for io.StringIO

_IS_PY2 = (sys.version_info.major == 2)

#############################################################################

class TestLoggingConfigDict(TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.foo = bar
        pass

    def setUp(self):
        """."""
        # for test_filters only, because Py2 lacks "nonlocal"
        self.debug_count = 0
        self.info_count = 0
        self.ge_warning_count = 0
        self.test_filters_on_handler__messages = []

    def test_1(self):
        lcd = LoggingConfigDict(root_level='DEBUG',
                                disable_existing_loggers=False)
        lcd.add_formatter(
            'minimal',
            format='%(message)s'
        ).add_formatter(
            'process_msg',
            format='%(processName)-10s: %(message)s'
        ).add_formatter(
            'logger_process_msg',
            format='%(name)-15s: %(processName)-10s: %(message)s'
        )

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(lcd, {
            'version': 1,
            'root': {'level': 'DEBUG', 'handlers': []},
            'loggers': {},
            'disable_existing_loggers': False,
            'formatters': {'minimal': {'class': 'logging.Formatter', 'format': '%(message)s'},
                           'process_msg': {'class': 'logging.Formatter',
                                           'format': '%(processName)-10s: %(message)s'},
                           'logger_process_msg': {'class': 'logging.Formatter',
                                                  'format': '%(name)-15s: %(processName)-10s: %(message)s'}
                          },
            'incremental': False,
            'filters': {},
            'handlers': {}
        })

        lcd.add_handler(
            'console',
            class_='logging.StreamHandler',
            level='INFO',
            formatter='minimal'
        ).add_file_handler(
            'default_file',
            filename='blather.log',
            level='DEBUG',
            formatter='minimal'
        )

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(lcd, {
            'version': 1,
            'root': {'level': 'DEBUG', 'handlers': []},
            'loggers': {},
            'disable_existing_loggers': False,
            'incremental': False,
            'formatters': {'minimal': {'class': 'logging.Formatter', 'format': '%(message)s'},
                           'process_msg': {'class': 'logging.Formatter',
                                           'format': '%(processName)-10s: %(message)s'},
                           'logger_process_msg': {'class': 'logging.Formatter',
                                                  'format': '%(name)-15s: %(processName)-10s: %(message)s'}
                          },
            'filters': {},
            'handlers': {'console': {'formatter': 'minimal', 'level': 'INFO',
                                     'class': 'logging.StreamHandler'},
                         'default_file': {'formatter': 'minimal', 'level': 'DEBUG',
                                          'class': 'logging.FileHandler',
                                          'filename': 'blather.log',
                                          'delay': False, 'mode': 'w'}}
        })

        lcd.add_logger(
            'default',
            handlers=('console', 'default_file'),
            level='DEBUG'
        )
        lcd.set_logger_level('default', level='DEBUG')  # coverage ho'

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(lcd, {
            'version': 1,
            'root': {'level': 'DEBUG', 'handlers': []},
            'loggers': {'default': {'level': 'DEBUG', 'handlers': ['console', 'default_file']}},
            'disable_existing_loggers': False,
            'incremental': False,
            'formatters': {'minimal': {'class': 'logging.Formatter', 'format': '%(message)s'},
                           'process_msg': {'class': 'logging.Formatter',
                                           'format': '%(processName)-10s: %(message)s'},
                           'logger_process_msg': {'class': 'logging.Formatter',
                                                  'format': '%(name)-15s: %(processName)-10s: %(message)s'}
                          },
            'filters': {},
            'handlers': {'console': {'formatter': 'minimal', 'level': 'INFO',
                                     'class': 'logging.StreamHandler'},
                         'default_file': {'formatter': 'minimal', 'level': 'DEBUG',
                                          'class': 'logging.FileHandler',
                                          'filename': 'blather.log',
                                          'delay': False, 'mode': 'w'}}
        })

    def test_add_logger_one_handler(self):

        lcd = LoggingConfigDict(root_level='DEBUG')
        lcd.add_formatter(
            'minimal',
            format='%(message)s'
        )
        lcd.add_handler(
            'console',
            class_='logging.StreamHandler',
            level='INFO',
            formatter='minimal'
        )
        lcd.add_logger(
            'default',
            handlers='console',
            level='DEBUG',
            propagate=False     # for coverage
        )
        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['handlers'],
            {'console': {'class': 'logging.StreamHandler',
                          'formatter': 'minimal',
                          'level': 'INFO'}}
        )
        self.assertEqual(
            lcd['loggers'],
            {'default': {'handlers': ['console'],
                         'level': 'DEBUG',
                         'propagate': False}}
        )
        lcd.config()

    def test_filters_on_logger(self):

        def _count_debug(record):
            """
            :param record: logging.LogRecord
            :return: bool -- True ==> let record through, False ==> squelch
            """
            # nonlocal debug_count
            if record.levelno == logging.DEBUG:
                self.debug_count += 1
            return True

        class CountInfo(logging.Filter):
            def filter(self_, record):
                """
                :param self_: "self" for the CountInfo object (unused)
                :param record: logging.LogRecord
                :return: bool -- True ==> let record through, False ==> squelch
                """
                if record.levelno == logging.INFO:
                    self.info_count += 1
                return True

        # Note: If Python 2.x, filter can't be just
        # .     any callable taking a logging record as arg;
        # .     it must have an attribute .filter
        # .     which must be a callable taking a logging record as arg.
        if _IS_PY2:
            _count_debug.filter = _count_debug

        lcd = LoggingConfigDict()
        lcd.set_root_level('DEBUG')

        lcd.add_formatter(
            'minimal',
            format='%(message)s'
        ).add_handler(
            'console',
            # class_='logging.StreamHandler',
            class_='logging.NullHandler',   # . <-- suppress output
            level='INFO',
            formatter='minimal'
        ).set_handler_level(
            'console', 'DEBUG')

        lcd.add_root_handlers('console')

        lcd.add_filter(
            'count_d',
            ** {'()': lambda: _count_debug }
        ).add_filter(
            'count_i',
            ** {'()': CountInfo}
        )

        lcd.add_logger('h', filters=['count_d', 'count_i'])

        # shameless bid for more coverage
        lcd.set_logger_level('h', level='DEBUG')

        lcd.config(disable_existing_loggers=False)
        logger = logging.getLogger('h')

        if _IS_PY2:
            logger.debug(u"Hi 1")
            logger.debug(u"Hi 2")
            logger.info(u"Hi 3")
        else:
            logger.debug("Hi 1")
            logger.debug("Hi 2")
            logger.info("Hi 3")

        self.assertEqual(self.debug_count, 2)
        self.assertEqual(self.info_count, 1)

    def test_one_filter_on_logger(self):

        class CountInfo(logging.Filter):
            def filter(self_, record):
                """
                :param self_: "self" for the CountInfo object (unused)
                :param record: logging.LogRecord
                :return: bool -- True ==> let record through, False ==> squelch
                """
                if record.levelno == logging.INFO:
                    self.info_count += 1
                return True

        lcd = LoggingConfigDict(root_level='DEBUG')

        lcd.add_formatter(
            'minimal',
            format='%(message)s'
        )

        my_stream = io.StringIO()

        lcd.add_handler(
            'console',
            class_='logging.StreamHandler',
            stream=my_stream,
            level='INFO',
            formatter='minimal'
        ).set_handler_level(
            'console', 'DEBUG')

        lcd.add_root_handlers('console')

        lcd.add_filter(
            'count_i',
            ** {'()': CountInfo}
        )

        lcd.add_logger('abc', filters='count_i')

        lcd.config()

        logger = logging.getLogger('abc')
        if _IS_PY2:
            logger.debug(u"Yo 1")
            logger.debug(u"Yo 2")
            logger.info(u"Yo 3")
        else:
            logger.debug("Yo 1")
            logger.debug("Yo 2")
            logger.info("Yo 3")

        self.assertEqual(self.info_count, 1)

    def test_filter_on_root(self):

        class CountGEWarning(logging.Filter):
            def filter(self_, record):
                """Filter that counts messages with loglevel >= WARNING.
                :param self_: "self" for CountGEWarning object (unused)
                :param record: logging.LogRecord
                :return: bool -- True ==> let record through, False ==> squelch
                """
                if record.levelno >= logging.WARNING:
                    self.ge_warning_count += 1
                return True

        lcd = LoggingConfigDict(root_level='DEBUG')

        lcd.add_formatter(
            'minimal',
            format='%(message)s'
        )
        my_stream = io.StringIO()

        lcd.add_handler(
            'console',
            class_='logging.StreamHandler',
            stream=my_stream,
            # class_='logging.NullHandler',   # . <-- suppress output
            level='INFO',
            formatter='minimal'
        ).add_root_handlers('console')

        lcd.add_filter(
            'count_gew',
            ** {'()': CountGEWarning}
        ).add_root_filters(                   # coverage ho'dom
        ).add_root_filters('count_gew')

        lcd.config()
        logger = logging.getLogger()
        if _IS_PY2:
            logger.debug(u"Hi 1")
            logger.debug(u"Hi 2")
            logger.info(u"Hi 3")
            logger.warning(u"Hi 4")
            logger.error(u"Hi 5")
            logger.critical(u"Hi 6")
        else:
            logger.debug("Hi 1")
            logger.debug("Hi 2")
            logger.info("Hi 3")
            logger.warning("Hi 4")
            logger.error("Hi 5")
            logger.critical("Hi 6")
        self.assertEqual(my_stream.getvalue(),
                         "Hi 3\n"
                         "Hi 4\n"
                         "Hi 5\n"
                         "Hi 6\n"
        )
        self.assertEqual(self.ge_warning_count, 3)

    def test_filters_on_handler(self):

        class FilterOutOddRecords(logging.Filter):
            def filter(_self_, record):
                """If level of record is >= INFO, let record through;
                o/w, increment self.info_count += 1;
                if self.info_count odd, allow record through.
                :param self_: "self" for the CountInfo object (unused)
                :param record: logging.LogRecord
                :return: bool -- True ==> let record through, False ==> squelch
                """
                if record.levelno < logging.INFO:
                    return True
                self.info_count += 1
                if self.info_count % 2:
                    self.test_filters_on_handler__messages.append(self.info_count - 1)
                return self.info_count % 2

        lcd = LoggingConfigDict()
        lcd.set_root_level('DEBUG')

        lcd.add_filter(
            'filter_odd',
            ** {'()': FilterOutOddRecords}
        ).add_formatter(
            'minimal',
            format='%(message)s'
        ).add_handler(
            'console',
            class_='logging.StreamHandler',     # writes messages
            # class_='logging.NullHandler',     # can't do this to suppress output: filter won't be called
            level='INFO',
            formatter='minimal',
            filters=['filter_odd']
        )
        lcd.add_root_handlers('console')

        # Swap stderr BEFORE lcd.config:
        _stderr = sys.stderr
        sio_err = io.StringIO()
        sys.stderr = sio_err

        # NOW do lcd.config:
        lcd.config(disable_existing_loggers=False)

        # log stuff
        logger = logging.getLogger()
        logger.debug("Hi 0")
        logger.debug("Hi 1")
        if _IS_PY2:
            logger.info(u"0")     # passes filter
            logger.info(u"1")
            logger.info(u"2")     # passes filter
            logger.info(u"3")
        else:
            logger.info("0")     # passes filter
            logger.info("1")
            logger.info("2")     # passes filter
            logger.info("3")

        # unswap stderr, unnecessarily
        sys.stderr = _stderr
        # print("sio_err.getvalue(): '%s'" % sio_err.getvalue())

        self.assertEqual(sio_err.getvalue(), "0\n2\n")
        self.assertEqual(self.info_count, 4)
        self.assertEqual(self.test_filters_on_handler__messages, [0, 2])
