__author__ = 'brianoneill'

from .logging_config_dict_ex import LoggingConfigDictEx


class ConfiguratorABC():
    """
    A class for automatic multi-package / multi-module logging configuration.
    Every package/module that wants a say in the configuration of logging
    defines its own subclass ConfiguratorABC, which overrides the method

        @abstractmethod
        @classmethod
        def add_to_lcd(lcd: LoggingConfigDict):
            pass

    The application should call ``configure_logging()``, a driver classmethod
    which creates a "blank" LoggingConfigDict ``lcdx``, then calls
    ``subcls.add_to_lcd(lcdx)`` on every subclass ``subcls``,
    in a breadth-first way. For example, given the inheritance diagram ("<"
    means "is a superclass of":

        ConfiguratorABC < MainConfigurator < ConfiguratorModuleA
                                           < ConfiguratorModuleB
                                           < ConfiguratorPackage < ConfiguratorSubPackage

    ``add_to_lcd`` will be called first on MainConfigurator; then on
    ConfiguratorModuleA, ConfiguratorModuleB, and ConfiguratorPackage,
    in some order; then on ConfiguratorSubPackage.

    One possible approach:

         MainConfigurator adds all loggers used by the app, and configures
         them sufficiently for the top level. The more-derived subclasses
         might add handlers and attach them to loggers added by
         MainConfigurator, assuming some conventions about the name(s) of
         those loggers.

    __init__

    """
    def __init__(self):

        pass

    # @abstractmethod
    @classmethod
    def add_to_lcd(cls, lcdx):          # pragma: no cover
        """(Virtual callout)

        ``configure_logging`` calls this method
        on every ``ConfiguratorABC`` subclass that implements it.
        All implementations are passed the same ``LoggingConfigDictEx``.
        Implementations should call ``LoggingConfigDictEx`` methods to
        further augment and customize ``lcdx``.

        :param lcdx: a ``LoggingConfigDictEx``
        """
        pass

    @classmethod
    def configure_logging(cls,
                   root_level='WARNING',
                   log_path='',
                   locking=False,
                   attach_handlers_to_root=False,
                   disable_existing_loggers=False):
        """This "driver" method creates a LoggingConfigDictEx ``lcdx``,
        and calls ``subcls.add_to_lcd(lcdx)`` on all subclasses ``subcls``
        of ``ConfiguratorABC`` *which implement the method*, in breadth-first
        order, passing the same ``LoggingConfigDictEx`` instance to each.

        After calling all the ``add_to_lcd`` implementations,
        this method calls ``lcdx.config()`` to configure logging.

        Parameters are as for ``LoggingConfigDictEx``.
        """
        lcdx = LoggingConfigDictEx(
                    root_level=root_level,
                    log_path=log_path,
                    locking=locking,
                    attach_handlers_to_root=attach_handlers_to_root,
                    disable_existing_loggers=disable_existing_loggers
        )
        derived_classes = ConfiguratorABC.__subclasses__()

        while derived_classes:
            subcls = derived_classes.pop()
            if 'add_to_lcd' in vars(subcls):    # i.e. in subcls.__dict__
                subcls.add_to_lcd(lcdx)
            derived_classes.extend(subcls.__subclasses__())

        lcdx.config()

