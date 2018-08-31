__author__ = 'brianoneill'

from prelogging import LCDict
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
        lcd = LCDict(root_level='DEBUG')

        self.assertEqual(lcd.locking, False)
        self.assertEqual(lcd.attach_handlers_to_root, False)

        # lcd.dump()      # | DEBUG comment out

        expected = self.get_expected_starting_dict('DEBUG')
        self.assertEqual(lcd, expected)

        lcd.add_stderr_handler(
            'console', level='WARNING', formatter='msg'
        )
        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['formatters'],
            {'msg': {'class': 'logging.Formatter',
                     'format': '%(message)s'},
            }
        )

        lcd.add_file_handler(
            'default_file',
            filename='blather.log',
            formatter='msg'
        )

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['handlers'],
            {'console': {'class': 'logging.StreamHandler',
                         'formatter': 'msg',
                         'level': 'WARNING',
                         'stream': 'ext://sys.stderr'},
             'default_file': {'class': 'logging.FileHandler',
                              'delay': False,
                              'filename': 'blather.log',
                              'formatter': 'msg',
                              # 'level': 'NOTSET',
                              'mode': 'a'}}
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
        lcd = LCDict(attach_handlers_to_root=True,
                    locking=True)

        self.assertEqual(lcd.locking, True)
        self.assertEqual(lcd.attach_handlers_to_root, True)

        # lcd.dump()      # | DEBUG comment out

        expected = self.get_expected_starting_dict()
        self.assertEqual(lcd, expected)

        # No formatters, use default
        lcd.add_stderr_handler(
            'console',
            level='WARNING'
        ).add_file_handler(
            'default_file',
            filename='blather.log',
            formatter='process_time_logger_level_msg'
        )

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['handlers'],
            {'console': {'()': 'ext://prelogging.LockingStreamHandler',
                         'create_lock': True,
                         'level': 'WARNING',
                         'stream': 'ext://sys.stderr'},
             'default_file': {'()': 'ext://prelogging.LockingFileHandler',
                              'create_lock': True,
                              'delay': False,
                              'filename': 'blather.log',
                              'formatter': 'process_time_logger_level_msg',
                              # 'level': 'NOTSET',
                              'mode': 'a'}}
        )

        lcd.clone_handler(clone='con2', handler='console')

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['handlers'],
            {'con2': {'()': 'ext://prelogging.LockingStreamHandler',
                      'create_lock': True,
                      'level': 'WARNING',
                      'stream': 'ext://sys.stderr'},
             'console': {'()': 'ext://prelogging.LockingStreamHandler',
                         'create_lock': True,
                         'level': 'WARNING',
                         'stream': 'ext://sys.stderr'},
             'default_file': {'()': 'ext://prelogging.LockingFileHandler',
                              'create_lock': True,
                              'delay': False,
                              'filename': 'blather.log',
                              'formatter': 'process_time_logger_level_msg',
                              # 'level': 'NOTSET',
                              'mode': 'a'}}
        )

        # For more coverage (locking_handlers.py from 46% to 60%)
        lcd.config(disable_existing_loggers=True)

    def test_no_lock_clone_handler(self):
        """
        clone handler with locking=False (so 'class' is in its dict)
        """
        lcd = LCDict()

        expected = self.get_expected_starting_dict()
        self.assertEqual(lcd, expected)

        lcd.add_stdout_handler('con', level='WARNING', formatter='msg')
        lcd.clone_handler(clone='con2', handler='con')

        # lcd.dump()      # | DEBUG comment out

        self.assertEqual(
            lcd['handlers'],
            {'con': {'class': 'logging.StreamHandler',
                     'formatter': 'msg',
                     'level': 'WARNING',
                     'stream': 'ext://sys.stdout'},
             'con2': {'class': 'logging.StreamHandler',
                      'formatter': 'msg',
                      'level': 'WARNING',
                      'stream': 'ext://sys.stdout'}}
        )

# ---------------------------------------------------------------------------
# set_handler_formatter (the override)
# ---------------------------------------------------------------------------
class TestLCDEx_Misc(TestCase):

    def test_set_handler_formatter(self):
        d = LCDict()
        d.add_handler('h')
        d.set_handler_formatter('h', 'msg')
        self.assertEqual(
            d.handlers['h']['formatter'],
            'msg'
        )
        # d.dump()         # TODO Comment out
        # In fact,
        self.assertEqual(
            d,
            {'disable_existing_loggers': False,
             'filters': {},
             'formatters': {'msg': {'class': 'logging.Formatter',
                                    'format': '%(message)s'}},
             'handlers': {'h': { # 'level': 'NOTSET',
                                'formatter': 'msg'}},
             'incremental': False,
             'loggers': {},
             'root': {'handlers': [], 'level': 'WARNING'},
             'version': 1}
        )


#############################################################################

if __name__ == '__main__':
    pass
