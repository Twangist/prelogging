__author__ = 'brianoneill'

from test_lcd_builders_top import LCDBuilderSub

class LCDBuilderSubB(LCDBuilderSub):
    @classmethod
    def add_to_lcdict(cls, lcd):
        """(Virtual) Call ``LCDict`` methods to augment ``lcd``.

        :param lcd: a ``LCDict``
        """
        # Configure so that:
        #   Messages logged by logger 'subB'
        #       will be written to logfile 'subB.log', and
        #       will NOT be written to root logger (propagate=False)
        #
        #   Root logger will NOT log to 'subB.log' (attach_to_root=False)
        # Assume the code that uses this logger is in development,
        # so we'll set level to ``DEBUG``.
        lcd.add_file_handler('subB-fh',
                             filename='subB.log',
                             mode='w',
                             formatter='logger_level_msg',
                             attach_to_root=False)
        lcd.add_logger('subB',
                       handlers='subB-fh',
                       level='DEBUG',
                       propagate=False)

