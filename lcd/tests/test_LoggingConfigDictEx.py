__author__ = 'brianoneill'

from lcd import LoggingConfigDictEx
from unittest import TestCase
import logging
import sys
import io

#############################################################################

class TestLoggingConfigDictEx(TestCase):
    # class attrs

    @classmethod
    def setUpClass(cls):
        # cls.foo = bar
        pass

    def get_expected_starting_dict(self, level='WARNING'):
        """."""
        # use LoggingConfigDictEx.format_strs
        formatters_dict = {
            formatter: {'class': 'logging.Formatter',
                        'format': LoggingConfigDictEx.format_strs[formatter]
                       }
            for formatter in LoggingConfigDictEx.format_strs
        }

        return {
            'disable_existing_loggers': False,
            'loggers': {},
            'handlers': {},
            'filters': {},
            'formatters': formatters_dict,
            'incremental': False,
            'root': {'handlers': [], 'level': level},
            'version': 1
        }

    def test_no_root_handlers_no_lock(self):
        """
        DON'T add handlers to root, locking=False
        """
        lcd = LoggingConfigDictEx(root_level='DEBUG')

        self.assertEqual(lcd.locking, False)
        self.assertEqual(lcd.attach_handlers_to_root, False)

        # lcd.dump()      # | DEBUG comment out

        expected = self.get_expected_starting_dict('DEBUG')
        self.assertEqual(lcd, expected)

        lcd.add_stderr_console_handler(
            'console', formatter='minimal'
        ).add_file_handler(
            'default_file',
            filename='blather.log',
            # level='DEBUG',
            formatter='minimal'
        )

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['handlers'],
            {'console': {'class': 'logging.StreamHandler',
                         'formatter': 'minimal',
                         'level': 'WARNING',
                         'stream': 'ext://sys.stderr'},
             'default_file': {'class': 'logging.FileHandler',
                              'delay': False,
                              'filename': 'blather.log',
                              'formatter': 'minimal',
                              'level': 'NOTSET',
                              'mode': 'w'}}
        )

        lcd.add_logger(
            'default',
            handlers=('console', 'default_file'),
            level='DEBUG'
        )

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['loggers'],
            {'default': {'handlers': ['console', 'default_file'],
                         'level': 'DEBUG'}
            }
        )

    def test_root_handlers_lock(self):
        """
        DO add handlers to root, locking=True
        """
        lcd = LoggingConfigDictEx(attach_handlers_to_root=True,
                                  locking=True)

        self.assertEqual(lcd.locking, True)
        self.assertEqual(lcd.attach_handlers_to_root, True)

        # lcd.dump()      # | DEBUG comment out

        expected = self.get_expected_starting_dict()
        self.assertEqual(lcd, expected)

        lcd.add_stderr_console_handler(
            'console',
            # No formatter, use default
        ).add_file_handler(
            'default_file',
            filename='blather.log',
            # level='DEBUG'
            # No formatter, use default
        )

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['handlers'],
            {'console': {'()': 'ext://lcd.LockingStreamHandler',
                         'create_lock': True,
                         'formatter': 'process_logger_level_msg',
                         'level': 'WARNING',
                         'stream': 'ext://sys.stderr'},
             'default_file': {'()': 'ext://lcd.LockingFileHandler',
                              'create_lock': True,
                              'delay': False,
                              'filename': 'blather.log',
                              'formatter': 'process_time_logger_level_msg',
                              'level': 'NOTSET',
                              'mode': 'w'}}
        )

        lcd.clone_handler(clone='con2', handler='console')

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['handlers'],
            {'con2': {'()': 'ext://lcd.LockingStreamHandler',
                      'create_lock': True,
                      'formatter': 'process_logger_level_msg',
                      'level': 'WARNING',
                      'stream': 'ext://sys.stderr'},
             'console': {'()': 'ext://lcd.LockingStreamHandler',
                         'create_lock': True,
                         'formatter': 'process_logger_level_msg',
                         'level': 'WARNING',
                         'stream': 'ext://sys.stderr'},
             'default_file': {'()': 'ext://lcd.LockingFileHandler',
                              'create_lock': True,
                              'delay': False,
                              'filename': 'blather.log',
                              'formatter': 'process_time_logger_level_msg',
                              'level': 'NOTSET',
                              'mode': 'w'}}
        )

        # For more coverage (locking_handlers.py from 46% to 60%)
        lcd.config(disable_existing_loggers=True)

    def test_no_lock_clone_handler(self):
        """
        clone handler with locking=False (so 'class' is in its dict)
        """
        lcd = LoggingConfigDictEx()

        expected = self.get_expected_starting_dict()
        self.assertEqual(lcd, expected)

        lcd.add_stdout_console_handler('con', formatter='minimal')
        lcd.clone_handler(clone='con2', handler='con')

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['handlers'],
            {'con2': {'class': 'logging.StreamHandler',
                      'formatter': 'minimal',
                      'level': 'WARNING',
                      'stream': 'ext://sys.stdout'},
             'con': {'class': 'logging.StreamHandler',
                     'formatter': 'minimal',
                     'level': 'WARNING',
                     'stream': 'ext://sys.stdout'}}
        )


class TestLoggingConfigDictEx_check(TestCase):

    def test_check_bad1(self):

        lcd_ex = LoggingConfigDictEx(
            attach_handlers_to_root=True,
            root_level='DEBUG')

        #  NOW SCREW IT UP:
        lcd_ex.attach_root_filters('not-a-filter-1', 'not-a-filter-2')
        lcd_ex.attach_root_handlers('not-a-handler-1', 'not-a-handler-2')
        lcd_ex.add_file_handler(
            'fh', 'myfile.log',
            filters=['also-not-a-filter-1', 'also-not-a-filter-2'])

        # Swap stderr BEFORE lcd_ex.check():
        _stderr = sys.stderr
        sio_err = io.StringIO()
        sys.stderr = sio_err

        # check out ".check()"
        # We expect this call to have written to stderr, and to raise KeyError
        with self.assertRaises(KeyError):
            lcd_ex.check()

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

        lcd_ex = LoggingConfigDictEx()
        # handler w/bad formatter
        lcd_ex.add_stdout_console_handler('con', formatter='no-such-formatter')

        # non-root logger
        lcd_ex.add_logger(
            'mylogger',
            handlers=['no-such-handler-1', 'no-such-handler-2'],
            filters='no-such-filter-1',
        )

        # Swap stderr BEFORE lcd_ex.check():
        _stderr = sys.stderr
        sio_err = io.StringIO()
        sys.stderr = sio_err

        # check out ".check()"
        # We expect this call to have written to stderr, and to raise KeyError
        with self.assertRaises(KeyError):
            lcd_ex.check()

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

        lcd_ex = LoggingConfigDictEx()
        self.assertEqual(lcd_ex, lcd_ex.check())



#############################################################################

if __name__ == '__main__':
    pass
