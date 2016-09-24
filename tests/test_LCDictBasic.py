__author__ = 'brianoneill'

from prelogging import LCDictBasic
from prelogging.six import PY2

from unittest import TestCase
import logging
import sys
import io   # for io.StringIO


#############################################################################

class TestLCD(TestCase):

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
        lcd = LCDictBasic(root_level='DEBUG',
                                disable_existing_loggers=False)
        lcd.add_formatter(
            'msg',
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
            'formatters': {'msg': {'class': 'logging.Formatter', 'format': '%(message)s'},
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
            formatter='msg'
        ).add_file_handler(
            'default_file',
            filename='blather.log',
            level='DEBUG',
            formatter='msg'
        )

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(lcd, {
            'version': 1,
            'root': {'level': 'DEBUG', 'handlers': []},
            'loggers': {},
            'disable_existing_loggers': False,
            'incremental': False,
            'formatters': {'msg': {'class': 'logging.Formatter', 'format': '%(message)s'},
                           'process_msg': {'class': 'logging.Formatter',
                                           'format': '%(processName)-10s: %(message)s'},
                           'logger_process_msg': {'class': 'logging.Formatter',
                                                  'format': '%(name)-15s: %(processName)-10s: %(message)s'}
                          },
            'filters': {},
            'handlers': {'console': {'formatter': 'msg', 'level': 'INFO',
                                     'class': 'logging.StreamHandler'},
                         'default_file': {'formatter': 'msg', 'level': 'DEBUG',
                                          'class': 'logging.FileHandler',
                                          'filename': 'blather.log',
                                          'delay': False, 'mode': 'a'}}
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
            'formatters': {'msg': {'class': 'logging.Formatter', 'format': '%(message)s'},
                           'process_msg': {'class': 'logging.Formatter',
                                           'format': '%(processName)-10s: %(message)s'},
                           'logger_process_msg': {'class': 'logging.Formatter',
                                                  'format': '%(name)-15s: %(processName)-10s: %(message)s'}
                          },
            'filters': {},
            'handlers': {'console': {'formatter': 'msg', 'level': 'INFO',
                                     'class': 'logging.StreamHandler'},
                         'default_file': {'formatter': 'msg', 'level': 'DEBUG',
                                          'class': 'logging.FileHandler',
                                          'filename': 'blather.log',
                                          'delay': False, 'mode': 'a'}}
        })

    def test_add_logger_one_handler(self):

        lcd = LCDictBasic(root_level='DEBUG')
        lcd.add_formatter(
            'msg',
            format='%(message)s'
        ).add_handler(
            'console',
            class_='logging.StreamHandler',
            level='INFO',
            # formatter='msg'
        ).set_handler_formatter(     # coverage
            'console', 'msg'
        )
        lcd.warnings = 0
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
                         'formatter': 'msg',
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

        lcd = LCDictBasic()
        lcd.set_root_level('DEBUG')

        lcd.add_formatter(
            'msg',
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

        lcd = LCDictBasic(root_level='DEBUG')

        lcd.add_formatter(
            'msg',
            format='%(message)s'
        )

        my_stream = io.StringIO()

        lcd.add_handler(
            'console',
            class_='logging.StreamHandler',
            stream=my_stream,
            # level='INFO',
            formatter='msg'
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

        lcd = LCDictBasic(root_level='DEBUG')

        lcd.add_formatter(
            'msg',
            format='%(message)s'
        )
        my_stream = io.StringIO()

        lcd.add_handler(
            'console',
            class_='logging.StreamHandler',
            stream=my_stream,
            # class_='logging.NullHandler',   # . <-- suppress output
            level='INFO',
            formatter='msg'
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

        lcd = LCDictBasic()
        lcd.set_root_level('DEBUG')

        lcd.add_filter(
            'filter_odd',
            ** {'()': FilterOutOddRecords}
        ).add_formatter(
            'msg',
            format='%(message)s'
        ).add_handler(
            'console',
            class_='logging.StreamHandler',     # writes messages
            # class_='logging.NullHandler',     # can't do this to suppress output: filter won't be called
            level='INFO',
            formatter='msg',
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

    def test_add_stream_handler(self):

        lcd = LCDictBasic()
        lcd.set_root_level('DEBUG'
        ).add_stream_handler('h_stream', 'ext://sys.stderr'
        ).attach_root_handlers('h_stream')

        # Swap stderr BEFORE lcd.config:
        _stderr = sys.stderr
        sio_err = io.StringIO()
        sys.stderr = sio_err

        lcd.config()

        # log stuff
        logger = logging.getLogger()
        if PY2:
            logger.debug(u"Hi 0")
            logger.debug(u"Hi 1")
        else:
            logger.debug("Hi 0")
            logger.debug("Hi 1")

        # unswap stderr, needlessly
        sys.stderr = _stderr

        # print("sio_err.getvalue(): '%s'" % sio_err.getvalue())  # TODO DEBUG COMMENT OUT

        self.assertEqual(sio_err.getvalue(), "Hi 0\nHi 1\n")


# ---------------------------------------------------------------------------
# check()
# ---------------------------------------------------------------------------

class TestLCD_check(TestCase):

    def test_check_bad1(self):

        d = LCDictBasic(
            root_level='DEBUG',
            warnings=0)

        #  NOW SCREW IT UP:
        d.attach_root_filters('not-a-filter-1', 'not-a-filter-2')
        d.attach_root_handlers('not-a-handler-1', 'not-a-handler-2')
        d.add_file_handler(
            'fh', 'myfile.log',
            filters=['also-not-a-filter-1', 'also-not-a-filter-2'])

        # Swap stderr BEFORE d.check():
        _stderr = sys.stderr
        sio_err = io.StringIO()
        sys.stderr = sio_err

        # check out ".check()"
        # We expect this call to have written to stderr, and to raise KeyError
        with self.assertRaises(KeyError):
            d.check()

        self.assertEqual(
            sio_err.getvalue(),
            "Problems -- nonexistent things mentioned\n"
            "   handler            'fh' mentions     filter 'also-not-a-filter-1'\n"
            "   handler            'fh' mentions     filter 'also-not-a-filter-2'\n"
            "    logger              '' mentions     filter 'not-a-filter-1'\n"
            "    logger              '' mentions     filter 'not-a-filter-2'\n"
            "    logger              '' mentions    handler 'not-a-handler-1'\n"
            "    logger              '' mentions    handler 'not-a-handler-2'\n"
        )
        # unswap stderr, unnecessarily
        sys.stderr = _stderr

    def test_check_bad2(self):

        d = LCDictBasic(warnings=0)
        # handler w/bad formatter
        d.add_handler('con', formatter='no-such-formatter')

        # non-root logger
        d.add_logger(
            'mylogger',
            handlers=['no-such-handler-1', 'no-such-handler-2'],
            filters='no-such-filter-1',
        )

        # Swap stderr BEFORE d.check():
        _stderr = sys.stderr
        sio_err = io.StringIO()
        sys.stderr = sio_err

        # check out ".check()"
        # We expect this call to have written to stderr, and to raise KeyError
        with self.assertRaises(KeyError):
            d.check()

        # print(sio_err.getvalue())       # | DEBUG comment out

        self.assertEqual(
            sio_err.getvalue(),
            "Problems -- nonexistent things mentioned\n"
            "   handler           'con' mentions  formatter 'no-such-formatter'\n"
            "    logger      'mylogger' mentions     filter 'no-such-filter-1'\n"
            "    logger      'mylogger' mentions    handler 'no-such-handler-1'\n"
            "    logger      'mylogger' mentions    handler 'no-such-handler-2'\n"
        )
        # unswap stderr, unnecessarily
        sys.stderr = _stderr

    def test_check_ok(self):
        lcd = LCDictBasic(warnings=0)
        self.assertEqual(lcd, lcd.check())

# ---------------------------------------------------------------------------
# no Warnings, Warnings
# ---------------------------------------------------------------------------

# class _TestLCD_Warn(TestCase):
class TestLCD_NoWarnings(TestCase):
    class F():
        def filter(self, record):
            return True

    def setUp(self):
        "Subclass(es) may change .warning property"

        # Swap stderr, save existing:
        self._stderr = sys.stderr
        self.sio_err = io.StringIO()    # new "stderr"
        sys.stderr = self.sio_err
        # create an LCDictBasic that doesn't issue any warnings
        self.lcd = LCDictBasic(warnings=0)      # 0 == LCDictBasic.WARNINGS.NONE

    def tearDown(self):
        "."
        # restore
        sys.stderr = self._stderr

    def _verify_errmsg(self, ends=''):
        " utility method"
        errmsg = self.sio_err.getvalue()
        if self.lcd.warnings:
            self.assertEqual(
                errmsg.startswith("Warning") and errmsg.endswith(ends),
                True
            )
        else:
            self.assertEqual(errmsg, '')

    #-------------------
    # re-add
    #-------------------

    def test_warn_formatter_readd(self):

        self.lcd.add_formatter('my_formatter', format='%(message)s')
        # Now readd -- check for warning to stderr

        self.lcd.add_formatter('my_formatter', format='%(message)s')

        self._verify_errmsg(": redefinition of formatter 'my_formatter'.\n")
        self.assertEqual(list(self.lcd.formatters.keys()), ['my_formatter'])

    def test_warn_filter_readd(self):
        self.lcd.add_filter('my_filter', ** {'()': self.F})
        # Now readd -- check for warning to stderr
        self.lcd.add_filter('my_filter', ** {'()': self.F})

        self._verify_errmsg(": redefinition of filter 'my_filter'.\n")
        self.assertEqual(list(self.lcd.filters.keys()), ['my_filter'])

    def test_warn_handler_readd(self):
        self.lcd.add_handler(
                        'my_handler',
                        class_='logging.StreamHandler',
                        stream='sys.stdout')
        # Now readd -- check for warning to stderr
        self.lcd.add_handler(
                        'my_handler',
                        class_='logging.StreamHandler',
                        stream='sys.stdout')

        self._verify_errmsg(": redefinition of handler 'my_handler'.\n")
        self.assertEqual(list(self.lcd.handlers.keys()), ['my_handler'])

    def test_warn_logger_readd(self):
        self.lcd = LCDictBasic()
        self.lcd.add_logger('my_logger')
        # Now readd -- check for warning to stderr
        self.lcd.add_logger('my_logger')

        self._verify_errmsg(": redefinition of logger 'my_logger'.\n")
        self.assertEqual(list(self.lcd.loggers.keys()), ['my_logger'])

    #-------------------
    # handler/formatter
    #-------------------
    def test_add_handler_no_formatter__then_attach(self):
        self.lcd.add_formatter('f1', format='< a bad format string >')
        self.lcd.add_handler('my_handler')
        self.lcd.set_handler_formatter('my_handler', 'f1')

        self.assertEqual(self.lcd.handlers['my_handler']['formatter'],
                         'f1'
        )

    def test_warn_reattach_formatter(self):
        # attach same formatter twice
        self.lcd.add_formatter('f1',
                               format='%(message)s'
        ).add_handler('my_handler',
                      formatter='f1')
        # Now reattach -- check for warning to stderr
        self.lcd.set_handler_formatter('my_handler', 'f1')

        self._verify_errmsg(": formatter 'f1' already attached to handler 'my_handler'.\n")
        self.assertEqual(
            self.lcd.handlers['my_handler']['formatter'],
            'f1'
        )

    def test_warn_redefine_formatter(self):
        # attach two diff formatters
        self.lcd.add_formatter('f1',  format='%(message)s'
        ).add_formatter('f2',  format=''
        ).add_handler('my_handler',
                      formatter='f1')
        # Now attach f2 -- check for warning to stderr
        self.lcd.set_handler_formatter('my_handler', 'f2')

        self._verify_errmsg(": formatter 'f2' replaces 'f1' in handler 'my_handler'.\n")
        self.assertEqual(
            self.lcd.handlers['my_handler']['formatter'],
            'f2'
        )

    #====================================
    # test duplicates in add_* lists
    #      and attach_*_* reattachments
    #====================================

    #-------------------
    # handler/filters
    #-------------------

    def test_warn__add_handler__dup_filters(self):
                # add_handler -- dup filters in list
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).add_filter('filter2', ** {'()': self.F})
        self.lcd.add_handler('my_handler',
                             filters=['filter1', 'filter2', 'filter1', 'filter2'])

        self._verify_errmsg(": list of filters to attach to handler 'my_handler'"
                            " contains duplicates: 'filter1', 'filter2'.\n")
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
        self._verify_errmsg(": list of filters to attach to handler 'my_handler'"
                            " contains duplicates: 'filter1'.\n")
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
        self._verify_errmsg(": these filters are already attached to handler 'my_handler'"
                            ": 'filter1'.\n")
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

        if self.lcd.warnings:
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
        else:
            self.assertEqual(errmsg, '')

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
        self._verify_errmsg(": list of filters to attach to logger 'my_logger'"
                            " contains duplicates: 'filter1', 'filter2'.\n")
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
        self._verify_errmsg(": list of filters to attach to logger 'my_logger'"
                            " contains duplicates: 'filter1'.\n")
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
        self._verify_errmsg(": these filters are already attached to logger 'my_logger'"
                            ": 'filter1'.\n")
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

        self._verify_errmsg(": list of handlers to attach to logger 'my_logger'"
                            " contains duplicates: 'handler1', 'handler2'.\n")
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

        self._verify_errmsg(": list of handlers to attach to logger 'my_logger'"
                            " contains duplicates: 'handler1'.\n")
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
        self._verify_errmsg(": these handlers are already attached to logger 'my_logger'"
                            ": 'handler1'.\n")
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

        self._verify_errmsg(": list of filters to attach to logger ''"
                            " contains duplicates: 'filter1', 'filter2'.\n")
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

        self._verify_errmsg(": list of filters to attach to logger ''"
                            " contains duplicates: 'filter1'.\n")
        self.assertEqual(
            self.lcd.root['filters'],
            ['filter1']
        )

    def test_warn__attach_root_filters__reattach_filters(self):
        self.lcd.add_filter('filter1', ** {'()': self.F}
        ).attach_root_filters('filter1'
        ).attach_root_filters('filter1'
                              )
        self._verify_errmsg(": these filters are already attached to logger ''"
                            ": 'filter1'.\n")
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

        self._verify_errmsg(": list of handlers to attach to logger ''"
                            " contains duplicates: 'handler1', 'handler2'.\n")
        self.assertEqual(
            self.lcd.root['handlers'],
            ['handler1', 'handler2']
        )

    def test_warn__attach_root_handlers__reattach_handlers(self):
        self.lcd.add_handler('handler1',
        ).attach_root_handlers('handler1'
        ).attach_root_handlers('handler1'
        )

        self._verify_errmsg(": these handlers are already attached to logger ''"
                            ": 'handler1'.\n")
        self.assertEqual(
            self.lcd.root['handlers'],
            ['handler1']
        )

    # Testing ATTACH_UNDEFINED -- which means testing ``_check_defined`` logic,
    # and that the correct args are passed to it by each of the 10 calls to it:
    """
    add_handler
        formatter   (undefined)
        filters     (one or more filters undefined. Similarly below)

    add_logger
        filters
        handlers

    set_handler_formatter
    attach_handler_filters

    attach_logger_filters
    attach_logger_handlers

    attach_root_filters
    attach_root_handlers
    """
    def test_warn_undef__add_handler__formatter(self):
        "with formatter undefined"
        self.lcd.add_handler('h', formatter='no-such-thing')

        self._verify_errmsg(": attaching undefined formatter 'no-such-thing'"
                            " to handler 'h'.\n")
        self.assertEqual(
            self.lcd.handlers['h']['formatter'],
            'no-such-thing'
        )

    def _add_filters_F1_F2_to_lcd(self):
        "Whenever you need a couple of filters,"
        class F1():
            def filter(self): return True
        class F2():
            def filter(self): return False

        self.lcd.add_filter('F1', ** {'()': F1})
        self.lcd.add_filter('F2', ** {'()': F2})

    def test_warn_undef__add_handler__filters(self):
        "with some filter undefined"
        self._add_filters_F1_F2_to_lcd()

        self.lcd.add_handler('h',
                             filters=['F1', 'no-such-filter', 'F2'])
        self._verify_errmsg(": attaching undefined filter 'no-such-filter'"
                            " to handler 'h'.\n")
        self.assertEqual(
            self.lcd.handlers['h']['filters'],
            ['F1', 'no-such-filter', 'F2']
        )

    def test_warn_undef__add_logger__filters(self):
        "with some filter undefined"
        self._add_filters_F1_F2_to_lcd()

        self.lcd.add_logger('my_logger',
                             filters=['no-such-filter', 'F1', 'F2'])
        self._verify_errmsg(": attaching undefined filter 'no-such-filter'"
                            " to logger 'my_logger'.\n")
        self.assertEqual(
            self.lcd.loggers['my_logger']['filters'],
            ['no-such-filter', 'F1', 'F2']
        )

    def test_warn_undef__add_logger__handlers(self):
        "with some handler undefined"
        self.lcd.add_handler('real-handler')
        self.lcd.add_logger('my_logger',
                            handlers=['real-handler', 'no-such-handler'])
        self._verify_errmsg(": attaching undefined handler 'no-such-handler'"
                            " to logger 'my_logger'.\n")
        self.assertEqual(
            self.lcd.loggers['my_logger']['handlers'],
            ['real-handler', 'no-such-handler']
        )

    def test_warn_undef__set_handler_formatter(self):
        "with formatter undefined"
        self.lcd.add_handler('h')
        self.lcd.set_handler_formatter('h', 'no-such-formatter')
        self._verify_errmsg(": attaching undefined formatter 'no-such-formatter'"
                            " to handler 'h'.\n")
        self.assertEqual(
            self.lcd.handlers['h']['formatter'],
            'no-such-formatter'
        )

    def test_warn_undef__attach_handler_filters(self):
        "with one or more filters undefined"
        self.lcd.add_handler('h')
        self.lcd.attach_handler_filters('h', 'no-such-filter')
        self._verify_errmsg(": attaching undefined filter 'no-such-filter'"
                            " to handler 'h'.\n")
        self.assertEqual(
            self.lcd.handlers['h']['filters'],
            ['no-such-filter']
        )

    def test_warn_undef__attach_logger_filters(self):
        "with one or more filters undefined"
        self._add_filters_F1_F2_to_lcd()

        self.lcd.add_logger('elle')
        self.lcd.attach_logger_filters('elle', 'no-such-filter', 'F1', 'F2')
        self._verify_errmsg(": attaching undefined filter 'no-such-filter'"
                            " to logger 'elle'.\n")
        self.assertEqual(
            self.lcd.loggers['elle']['filters'],
            ['no-such-filter', 'F1', 'F2']
        )

    def test_warn_undef__attach_logger_handlers(self):
        "with one or more handlers undefined"
        self.lcd.add_logger('elle')
        self.lcd.add_handler('h1') \
                .add_handler('h2')
        self.lcd.attach_logger_handlers('elle', 'h1', 'no-such-handler', 'h2')
        self._verify_errmsg(": attaching undefined handler 'no-such-handler'"
                            " to logger 'elle'.\n")
        self.assertEqual(
            self.lcd.loggers['elle']['handlers'],
            ['h1', 'no-such-handler', 'h2']
        )

    def test_warn_undef__attach_root_filters(self):
        "with one or more filters undefined"
        self._add_filters_F1_F2_to_lcd()

        self.lcd.attach_root_filters('no-such-filter1', 'F1', 'no-such-filter2')
        self._verify_errmsg(": attaching undefined filters 'no-such-filter1', 'no-such-filter2'"
                            " to logger ''.\n")
        self.assertEqual(
            self.lcd.root['filters'],
            ['no-such-filter1', 'F1', 'no-such-filter2']
        )

    def test_warn_undef__attach_root_handlers(self):
        "with one or more handlers undefined"
        self.lcd.add_handler('h1') \
                .add_handler('h2')
        self.lcd.attach_root_handlers('h1', 'h2', 'no-such-handler')
        self._verify_errmsg(": attaching undefined handler 'no-such-handler'"
                            " to logger ''.\n")
        self.assertEqual(
            self.lcd.root['handlers'],
            ['h1', 'h2', 'no-such-handler']
        )


# class TestLCD_Warnings(_TestLCD_Warn):
class TestLCD_Warnings(TestLCD_NoWarnings):

    def setUp(self):
        # parent class creates self.lcd = LCDictBasic()
        super(TestLCD_Warnings, self).setUp()
        # change warnings to ALL
        self.lcd.warnings = LCDictBasic.Warnings.ALL

