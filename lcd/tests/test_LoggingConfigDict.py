__author__ = 'brianoneill'

from lcd import LoggingConfigDict
from lcd.six import PY2

from unittest import TestCase
import logging
import sys
import io   # for io.StringIO


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
            level='DEBUG',
            # handlers='console',
            propagate=False     # for coverage
        )

        # lcd.dump()      # | DEBUG comment out

        lcd.attach_logger_handlers('default', 'console')

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
        if PY2:
            _count_debug.filter = _count_debug

        lcd = LoggingConfigDict()
        lcd.set_root_level('DEBUG')

        lcd.add_formatter(
            'minimal',
            format='%(message)s'
        ).add_null_handler(
            'console',
            level='INFO',
        ).set_handler_level(
            'console', 'DEBUG')

        lcd.attach_root_handlers('console')

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

        if PY2:
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
            # level='INFO',
            formatter='minimal'
        ).set_handler_level(
            'console', 'DEBUG')

        lcd.attach_logger_handlers('', 'console')   # coverage; defers to attach_root_handlers

        lcd.add_filter(
            'count_i',
            ** {'()': CountInfo}
        )

        lcd.add_logger('abc')       # , filters='count_i'
        lcd.attach_logger_filters('abc', 'count_i')

        lcd.config()

        logger = logging.getLogger('abc')
        if PY2:
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
        ).attach_root_handlers('console')

        lcd.add_filter(
            'count_gew',
            ** {'()': CountGEWarning}
        ).attach_root_filters(                      # coverage ho'dom
        ).attach_logger_filters(''                  # coverage ho'dom
        ).attach_logger_filters('', 'count_gew')    # coverage; defers to attach_root_filters

        lcd.config()
        logger = logging.getLogger()
        if PY2:
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
        )
        lcd.attach_handler_filters('console')               # coverage
        lcd.attach_handler_filters('console', 'filter_odd')
        lcd.attach_root_handlers('console')

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
        if PY2:
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


class TestLoggingConfigDict_WarnStrict(TestCase):

    def test_warn(self):
        w = LoggingConfigDict.warn()
        self.assertEqual(w, False)

        wT = LoggingConfigDict.warn(True)
        self.assertEqual(wT, True)
        self.assertEqual(LoggingConfigDict.warn(), True)

        wF = LoggingConfigDict.warn(False)
        self.assertEqual(wF, False)
        self.assertEqual(LoggingConfigDict.warn(), False)

    def test_strict(self):
        s = LoggingConfigDict.strict()
        self.assertEqual(s, False)

        sT = LoggingConfigDict.strict(True)
        self.assertEqual(sT, True)
        self.assertEqual(LoggingConfigDict.strict(), True)

        sF = LoggingConfigDict.strict(False)
        self.assertEqual(sF, False)
        self.assertEqual(LoggingConfigDict.strict(), False)


class TestLoggingConfigDict_Warnings(TestCase):
    class F():
        def filter(self, record):
            return True

    def setUp(self):
        LoggingConfigDict.warn(True)
        # Swap stderr, save existing:
        self._stderr = sys.stderr
        self.sio_err = io.StringIO()    # new "stderr"
        sys.stderr = self.sio_err
        # create an LCD
        self.lcd = LoggingConfigDict()

    def tearDown(self):
        # restore
        sys.stderr = self._stderr
        LoggingConfigDict.warn(False)

    #-------------------
    # re-add
    #-------------------

    def test_warn_formatter_readd(self):

        self.lcd.add_formatter('my_formatter', format='%(message)s')
        # Now readd -- check for warning to stderr

        self.lcd.add_formatter('my_formatter', format='%(message)s')

        errmsg = self.sio_err.getvalue()
        self.assertEqual(
            errmsg.startswith("Warning")
                and ": redefinition of formatter 'my_formatter'" in errmsg,
            True
        )

    def test_warn_filter_readd(self):
        self.lcd.add_filter('my_filter', ** {'()': self.F})
        # Now readd -- check for warning to stderr
        self.lcd.add_filter('my_filter', ** {'()': self.F})

        errmsg = self.sio_err.getvalue()
        self.assertEqual(
            errmsg.startswith("Warning")
                and ": redefinition of filter 'my_filter'" in errmsg,
            True
        )

    def test_warn_handler_readd(self):
        self.lcd.add_handler(
                        'console',
                        class_='logging.StreamHandler',
                        stream='sys.stdout')
        # Now readd -- check for warning to stderr
        self.lcd.add_handler(
                        'console',
                        class_='logging.StreamHandler',
                        stream='sys.stdout')

        errmsg = self.sio_err.getvalue()
        self.assertEqual(
            errmsg.startswith("Warning")
                and ": redefinition of handler 'console'" in errmsg,
            True
        )

    def test_warn_logger_readd(self):
        self.lcd = LoggingConfigDict()
        self.lcd.add_logger('my_logger')
        # Now readd -- check for warning to stderr
        self.lcd.add_logger('my_logger')

        errmsg = self.sio_err.getvalue()
        self.assertEqual(
            errmsg.startswith("Warning") and
                ": redefinition of logger 'my_logger'" in errmsg,
            True
        )

    #====================================
    # test duplicates in add_* lists
    #      and attach_*_* reattachments
    #====================================

    #-------------------
    # handler/formatter
    #-------------------

    def test_warn_reattach_formatter(self):
        # attach same formatter twice
        self.lcd.add_formatter('f1',
                               format='%(message)s'
        ).add_handler('my_handler',
                      formatter='f1')
        # Now reattach -- check for warning to stderr
        self.lcd.attach_handler_formatter('my_handler', 'f1')

        errmsg = self.sio_err.getvalue()
        self.assertEqual(
            errmsg.startswith("Warning") and
                ": formatter 'f1' already attached to handler 'my_handler'" in errmsg,
            True
        )

    def test_warn_redefine_formatter(self):
        # attach two diff formatters
        self.lcd.add_formatter('f1',  format='%(message)s'
        ).add_formatter('f2',  format=''
        ).add_handler('my_handler',
                      formatter='f1')
        # Now attach f2 -- check for warning to stderr
        self.lcd.attach_handler_formatter('my_handler', 'f2')

        errmsg = self.sio_err.getvalue()
        self.assertEqual(
            errmsg.startswith("Warning") and
                ": formatter 'f2' replaces 'f1' in handler 'my_handler'" in errmsg,
            True
        )

    #-------------------
    # handler/filters
    #-------------------

    def test_warn__add_handler__dup_filters(self):
                # add_handler -- dup filters in list
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).add_filter('filter2', ** {'()': self.F})
        self.lcd.add_handler('my_handler',
                             filters=['filter1', 'filter2', 'filter1', 'filter2'])
        errmsg = self.sio_err.getvalue()
        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": list of filters to attach to handler 'my_handler'"
                             " contains duplicates: 'filter1', 'filter2'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.handlers['my_handler']['filters'],
            ['filter1', 'filter2']
        )

    def test_warn__attach_handler_filters__dup_filters(self):
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).add_handler('my_handler'
        ).attach_handler_filters(
            'my_handler',
            'filter1', 'filter1'
        )
        errmsg = self.sio_err.getvalue()
        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": list of filters to attach to handler 'my_handler'"
                             " contains duplicates: 'filter1'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.handlers['my_handler']['filters'],
            ['filter1']
        )

    def test_warn__attach_handler_filters__reattach_filters(self):
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).add_handler('my_handler',
                      filters='filter1'
        ).attach_handler_filters(
            'my_handler',
            'filter1'
        )
        errmsg = self.sio_err.getvalue()
        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": these filters are already attached to handler 'my_handler'"
                             ": 'filter1'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.handlers['my_handler']['filters'],
            ['filter1']
        )

    def test_warn__attach_handler_filters__dup_filters_reattach_filters(self):
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).add_handler('my_handler',
                      filters='filter1'
        ).attach_handler_filters(
            'my_handler',
            'filter1', 'filter1'
        )
        errmsg = self.sio_err.getvalue()
        # print(errmsg)           # TODO COMMENT OUT

        errmsg1, errmsg2 = errmsg.splitlines()

        self.assertEqual(
            (errmsg1.startswith("Warning (") and
             errmsg1.endswith(": list of filters to attach to handler 'my_handler'"
                              " contains duplicates: 'filter1'.")
            ),
            True
        )
        self.assertEqual(
            (errmsg2.startswith("Warning (") and
             errmsg2.endswith(": these filters are already attached to handler 'my_handler'"
                              ": 'filter1'.")
            ),
            True
        )
        self.assertEqual(
            self.lcd.handlers['my_handler']['filters'],
            ['filter1']
        )

    #-------------------
    # logger/filters
    #-------------------

    def test_warn__add_logger__dup_filters(self):
                # add_handler -- dup filters in list
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).add_filter('filter2', ** {'()': self.F})
        self.lcd.add_logger('my_logger',
                            filters=['filter1', 'filter2', 'filter1', 'filter2'])
        errmsg = self.sio_err.getvalue()
        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": list of filters to attach to logger 'my_logger'"
                             " contains duplicates: 'filter1', 'filter2'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.loggers['my_logger']['filters'],
            ['filter1', 'filter2']
        )

    def test_warn__attach_logger_filters__dup_filters(self):
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).add_logger('my_logger'
        ).attach_logger_filters(
            'my_logger',
            'filter1', 'filter1'
        )
        errmsg = self.sio_err.getvalue()

        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": list of filters to attach to logger 'my_logger'"
                             " contains duplicates: 'filter1'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.loggers['my_logger']['filters'],
            ['filter1']
        )

    def test_warn__attach_logger_filters__reattach_filters(self):
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).add_logger('my_logger',
                     filters='filter1'
        ).attach_logger_filters(
            'my_logger',
            'filter1'
        )
        errmsg = self.sio_err.getvalue()

        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": these filters are already attached to logger 'my_logger'"
                             ": 'filter1'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.loggers['my_logger']['filters'],
            ['filter1']
        )

    #-------------------
    # logger/handlers
    #-------------------

    def test_warn__add_logger__dup_handlers(self):
                # add_handler -- dup filters in list
        self.lcd.add_handler('handler1'
        ).add_handler('handler2')
        self.lcd.add_logger('my_logger',
                            handlers=['handler1', 'handler2', 'handler1', 'handler2'])
        errmsg = self.sio_err.getvalue()
        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": list of handlers to attach to logger 'my_logger'"
                             " contains duplicates: 'handler1', 'handler2'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.loggers['my_logger']['handlers'],
            ['handler1', 'handler2']
        )

    def test_warn__attach_logger_handlers__dup_handlers(self):
        self.lcd.add_handler('handler1'
        ).add_logger('my_logger'
        ).attach_logger_handlers(
            'my_logger',
            'handler1', 'handler1'
        )
        errmsg = self.sio_err.getvalue()

        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": list of handlers to attach to logger 'my_logger'"
                             " contains duplicates: 'handler1'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.loggers['my_logger']['handlers'],
            ['handler1']
        )

    def test_warn__attach_logger_handlers__reattach_handlers(self):
        self.lcd.add_handler('handler1',
        ).add_logger('my_logger',
                     handlers='handler1'
        ).attach_logger_handlers(
            'my_logger',
            'handler1'
        )
        errmsg = self.sio_err.getvalue()

        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": these handlers are already attached to logger 'my_logger'"
                             ": 'handler1'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.loggers['my_logger']['handlers'],
            ['handler1']
        )

    #-------------------
    # root/filters
    #-------------------

    def test_warn__add_root__dup_filters(self):
                # add_handler -- dup filters in list
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).add_filter('filter2', ** {'()': self.F})
        self.lcd.attach_root_filters('filter1', 'filter2', 'filter1', 'filter2')
        errmsg = self.sio_err.getvalue()
        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": list of filters to attach to logger ''"
                             " contains duplicates: 'filter1', 'filter2'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.root['filters'],
            ['filter1', 'filter2']
        )

    def test_warn__attach_root_filters__dup_filters(self):
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).attach_logger_filters(
            '',
            'filter1', 'filter1'
        )
        errmsg = self.sio_err.getvalue()

        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": list of filters to attach to logger ''"
                             " contains duplicates: 'filter1'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.root['filters'],
            ['filter1']
        )

    def test_warn__attach_root_filters__reattach_filters(self):
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).attach_root_filters('filter1'
        ).attach_root_filters('filter1'
                              )
        errmsg = self.sio_err.getvalue()

        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": these filters are already attached to logger ''"
                             ": 'filter1'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.root['filters'],
            ['filter1']
        )

    #-------------------
    # root/handlers
    #-------------------

    def test_warn__attach_root_handlers__dup_handlers(self):
                # add_handler -- dup filters in list
        self.lcd.add_handler('handler1'
        ).add_handler('handler2')
        self.lcd.attach_root_handlers(
                            'handler1', 'handler2', 'handler1', 'handler2')
        errmsg = self.sio_err.getvalue()
        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": list of handlers to attach to logger ''"
                             " contains duplicates: 'handler1', 'handler2'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.root['handlers'],
            ['handler1', 'handler2']
        )

    def test_warn__attach_root_handlers__reattach_handlers(self):
        self.lcd.add_handler('handler1',
        ).attach_root_handlers('handler1'
        ).attach_root_handlers('handler1'
        )
        errmsg = self.sio_err.getvalue()

        # print(errmsg)           # TODO COMMENT OUT

        self.assertEqual(
            (errmsg.startswith("Warning (") and
             errmsg.endswith(": these handlers are already attached to logger ''"
                             ": 'handler1'.\n")
            ),
            True
        )
        self.assertEqual(
            self.lcd.root['handlers'],
            ['handler1']
        )


# TODO **also** test that dups are eliminated & entities aren't reattached,
#  |   even when "warn" is false (no warnings are written to stderr in that case,
#  |   but o/w no change in behavior)
#  | SOOO, maybe put the tests in a mixin,
#  |   and mix that into two classes which differ only in setUp/tearDown
#  |   ("warn" stays false).


# | <<<<<<<<<<<<<<<<<<<<<<<<<<< RESUME >>>>>>>>>>>>>>>>>>>>>>>>>>>

class TestLoggingConfigDict_StrictErrors(TestCase):

    def setUp(self):
        LoggingConfigDict.strict(True)
        # Swap stderr, save existing:
        self._stderr = sys.stderr
        self.sio_err = io.StringIO()    # new "stderr"
        sys.stderr = self.sio_err
        # create an LCD
        self.lcd = LoggingConfigDict()

    def tearDown(self):
        # restore
        sys.stderr = self._stderr
        LoggingConfigDict.strict(False)

    def test_strict_attach_handler_formatter(self):
        "with formatter undefined"
        pass    # TODO

    def test_strict_attach_handler_filters(self):
        "with one or more filters undefined"
        pass    # TODO

    def test_strict_attach_logger_filters(self):
        "with one or more filters undefined"
        pass    # TODO

    def test_strict_attach_logger_handlers(self):
        "with one or more handlers undefined"
        pass    # TODO
