__author__ = 'brianoneill'

try:
    import prelogging
except ImportError:
    import sys
    sys.path[0:0] = ['../..']

from prelogging import LCDictBuilderABC


##############################################################################
# LCDictBuilderABC subclasses
##############################################################################

class LCDictBuilder(LCDictBuilderABC):
    # override
    @classmethod
    def build_lcdict(cls,
                     root_level='WARNING',
                     log_path='',
                     locking=False,
                     attach_handlers_to_root=False,
                     disable_existing_loggers=False,
                     **kwargs):
        """(Virtual) Call ``LCDict`` methods to augment ``lcd``.
        :param lcd: an ``LCDict``
        """
        return super().build_lcdict(
            root_level=root_level,
            log_path=log_path,
            locking=locking,
            attach_handlers_to_root=attach_handlers_to_root,
            disable_existing_loggers=disable_existing_loggers,
            # kwargs
            common_file_handler_name='common_filehandler',
            console_handler_name='consolehandler',
        )

        lcd.add_stdout_handler('con-out',
                               formatter='logger_level_msg',
                               attach_to_root=True)

class LCDBuilderSub(LCDictBuilder):
    """An LCDBuilder class to organize a group of subclasses,
    perhaps to share data (class attributes).
    This class does **not** implement ``add_to_lcd``,
    which therefore will **not** be called on it
    (as that would call ``LCDBuilder.add_to_lcd`` a second time).
    """
    pass
