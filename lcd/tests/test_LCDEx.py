__author__ = 'brianoneill'

from lcd import LCDEx
from unittest import TestCase
import logging
import sys
import io

#############################################################################

class TestLCDEx(TestCase):
    # class attrs

    @classmethod
    def setUpClass(cls):
        # cls.foo = bar
        pass

    def get_expected_starting_dict(self, level='WARNING'):
        """."""
        # # use LCDEx._format_strs
        # formatters_dict = {
        #     formatter: {'class': 'logging.Formatter',
        #                 'format': LCDEx._format_strs[formatter]
        #                }
        #     for formatter in LCDEx._format_strs
        # }

        return {
            'disable_existing_loggers': False,
            'loggers': {},
            'handlers': {},
            'filters': {},
            'formatters': {},
            'incremental': False,
            'root': {'handlers': [], 'level': level},
            'version': 1
        }

    def test_no_root_handlers_no_lock(self):
        """
        DON'T add handlers to root, locking=False
        """
        lcd = LCDEx(root_level='DEBUG')

        self.assertEqual(lcd.locking, False)
        self.assertEqual(lcd.attach_handlers_to_root, False)

        # lcd.dump()      # | DEBUG comment out

        expected = self.get_expected_starting_dict('DEBUG')
        self.assertEqual(lcd, expected)

        lcd.add_stderr_handler(
            'console', formatter='minimal'
        )
        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['formatters'],
            {'minimal': {'class': 'logging.Formatter',
                         'format': '%(message)s'},
            }
        )

        lcd.add_file_handler(
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
        lcd = LCDEx(attach_handlers_to_root=True,
                                  locking=True)

        self.assertEqual(lcd.locking, True)
        self.assertEqual(lcd.attach_handlers_to_root, True)

        # lcd.dump()      # | DEBUG comment out

        expected = self.get_expected_starting_dict()
        self.assertEqual(lcd, expected)

        lcd.add_stderr_handler(
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
        lcd = LCDEx()

        expected = self.get_expected_starting_dict()
        self.assertEqual(lcd, expected)

        lcd.add_stdout_handler('con', formatter='minimal')
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

# ---------------------------------------------------------------------------
# set_handler_formatter (the override)
# create_formatter_preset
# ---------------------------------------------------------------------------
class TestLCDEx_Misc(TestCase):

    def test_attach_handler_formatter(self):
        d = LCDEx()
        d.add_handler('h')
        d.set_handler_formatter('h', 'minimal')
        self.assertEqual(
            d.handlers['h']['formatter'],
            'minimal'
        )
        # d.dump()         # TODO Comment out
        # In fact,
        self.assertEqual(
            d,
            {'disable_existing_loggers': False,
             'filters': {},
             'formatters': {'minimal': {'class': 'logging.Formatter',
                                        'format': '%(message)s'}},
             'handlers': {'h': {'formatter': 'minimal'}},
             'incremental': False,
             'loggers': {},
             'root': {'handlers': [], 'level': 'WARNING'},
             'version': 1}
        )

    def test_create_formatter_preset(self):
        num_presets = len(LCDEx._formatter_presets)
        LCDEx.create_formatter_preset(
            '_simple_',
            format="{levelname: <8s}: %(message)s",
            style='{'
        )
        self.assertEqual(
            len(LCDEx._formatter_presets),
            num_presets + 1
        )

        d = LCDEx()
        d.add_handler('h', formatter='_simple_')
        self.assertEqual(
            d.handlers['h']['formatter'],
            '_simple_'
        )
        # d.dump()          # TODO Comment out
        # In fact,
        self.assertEqual(
            d,
            {'disable_existing_loggers': False,
             'filters': {},
             'formatters': {'_simple_': {'class': 'logging.Formatter',
                                         'format': '{levelname: <8s}: %(message)s',
                                         'style': '{'}},
             'handlers': {'h': {'formatter': '_simple_'}},
             'incremental': False,
             'loggers': {},
             'root': {'handlers': [], 'level': 'WARNING'},
             'version': 1}
        )



# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------




#############################################################################

if __name__ == '__main__':
    pass
