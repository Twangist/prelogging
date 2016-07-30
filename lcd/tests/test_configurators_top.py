__author__ = 'brianoneill'

try:
    import lcd
except ImportError:
    import sys
    sys.path[0:0] = ['../..']

from lcd import ConfiguratorABC


##############################################################################
# ConfiguratorABC subclasses
##############################################################################

class Configurator(ConfiguratorABC):
    @classmethod
    def add_to_lcd(cls, lcdx):
        """(Virtual) Call ``LoggingConfigDictEx`` methods to augment ``lcdx``.

        :param lcdx: a ``LoggingConfigDictEx``
        """
        lcdx.add_stdout_handler('con-out',
                                        formatter='logger_level_msg',
                                        attach_to_root=True)

class ConfiguratorSub(Configurator):
    """A Configurator class to organize a group of subclasses,
    perhaps to share data (class attributes).
    This class does **not** implement ``add_to_lcd``,
    which therefore will **not** be called on it
    (as that would call ``Configurator.add_to_lcd`` a second time).
    """
    pass

