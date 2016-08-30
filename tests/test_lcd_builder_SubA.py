__author__ = 'brianoneill'

from test_lcd_builders_top import LCDBuilderSub


class LCDBuilderSubA(LCDBuilderSub):
    @classmethod
    def add_to_lcd(cls, lcdx):
        """(Virtual) Call ``LCDEx`` methods to augment ``lcdx``.

        :param lcdx: a ``LCDEx``
        """
        # Set up a logger 'subA' and a file handler it exclusively uses.
        # Assume the code that uses this module is well-debugged and stable,
        # so we an set logger's level = ``ERROR``.
        #
        #   Messages logged by logger 'subA' will be written
        #       to logfile 'subA.log', and
        #       to root logger (propagate=True).
        #   Root logger will NOT log to 'subA.log' (attach_to_root=False)
        lcdx.add_file_handler('subA-fh',
                              filename='subA.log',
                              mode='w',
                              formatter='logger_level_msg',
                              attach_to_root=False)
        lcdx.add_logger('subA',
                        handlers='subA-fh',
                        level='ERROR',
                        propagate=True)