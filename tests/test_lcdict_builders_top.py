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
    @classmethod
    def add_to_lcdict(cls, lcd):
        """(Virtual) Call ``LCDict`` methods to augment ``lcd``.

        :param lcd: an ``LCDict``
        """
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
