__author__ = 'brianoneill'

from test_lcd_builders_top import LCDBuilderSub

class LCDBuilderSubB(LCDBuilderSub):
    @classmethod
    def add_to_lcd(cls, lcdx):
        """(Virtual) Call ``LCDEx`` methods to augment ``lcdx``.

        :param lcdx: a ``LCDEx``
        """
        # Configure so that:
        #   Messages logged by logger 'subB'
        #       will be written to logfile 'subB.log', and
        #       will NOT be written to root logger (propagate=False)
        #
        #   Root logger will NOT log to 'subB.log' (attach_to_root=False)
        # Assume the code that uses this logger is in development,
        # so we'll set level to ``DEBUG``.
        lcdx.add_file_handler('subB-fh',
                              filename='subB.log',
                              mode='w',
                              formatter='logger_level_msg',
                              attach_to_root=False)
        lcdx.add_logger('subB',
                        handlers='subB-fh',
                        level='DEBUG',
                        propagate=False)

