__author__ = 'brianoneill'

from lcd import LoggingConfigDictEx
from unittest import TestCase

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
        lcd = LoggingConfigDictEx(add_handlers_to_root=True,
                                  locking=True)

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

#############################################################################

if __name__ == '__main__':
    pass
