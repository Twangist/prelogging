__author__ = 'brianoneill'

from .logging_config_dict_ex import LoggingConfigDictEx
from _collections_abc import ABCMeta, abstractmethod

class ConfiguratorABC(metaclass=ABCMeta):
    """
    .. include:: _global.rst

    A class for automating multi-package / multi-module logging configuration.
    ``ConfiguratorABC`` is an abstract base class: its metaclass is ``ABCMeta``,
    defined in ``_collections_abc.py`` of the standard library. You can't
    directly instantiate this class: it has an `abstractmethod`
    ``add_to_lcd(lcdx: LoggingConfigDictEx)``. Every package or module that
    wants a say in the configuration of logging should define its own
    (sub*)subclass of ``ConfiguratorABC`` which implements ``add_to_lcd``.

    Once (and once only), the application should call ``configure_logging()``,
    a classmethod which

        * creates a "blank" ``LoggingConfigDict``, ``lcdx``, and then
        * calls ``subcls.add_to_lcd(lcdx)`` on every subclass ``subcls``
          that implements ``add_to_lcd``, in a breadth-first way.

    For example, given the following inheritance tree (where "<" means
    "is a superclass of"):

    .. code::

        ConfiguratorABC < MainConfigurator < ConfiguratorModuleA
                                           < ConfiguratorModuleB
                                           < ConfiguratorPackage < ConfiguratorSubPackage

    Assuming that all classes shown implement ``add_to_lcd``, that method
    will be called first on ``MainConfigurator``; then on
    ``ConfiguratorModuleA``, ``ConfiguratorModuleB``, and
    ``ConfiguratorPackage``, in some order; then on ``ConfiguratorSubPackage``.

    See the test ``test_configurator.py`` for a multi-module example
    that uses these capabilities.
    |hr|
    """
    @classmethod
    @abstractmethod
    def add_to_lcd(cls, lcdx):          # pragma: no cover
        """(abstractmethod) Customize the passed ``LoggingConfigDictEx``.

        :param lcdx: a ``LoggingConfigDictEx``

        ``configure_logging`` calls this method on every ``ConfiguratorABC``
        subclass that implements it. All implementations are passed the same
        object ``lcdx``. Implementations should call ``LoggingConfigDictEx``
        methods on ``lcdx`` to augment and customize it.

        **Note**: Implementations should *not* call ``super().add_to_lcd`` —
        it has already been called by ``configure_logging``!
        """
        pass

    @classmethod
    def configure_logging(cls,
                   root_level='WARNING',
                   log_path='',
                   locking=False,
                   attach_handlers_to_root=False,
                   disable_existing_loggers=False):
        """A single method which creates a ``LoggingConfigDictEx``,
        calls all ``add_to_lcd`` methods with that object, and then
        configures logging using that object. Your program should call
        this method once (only).

        Parameters are as for ``LoggingConfigDictEx``.

        This method creates a ``LoggingConfigDictEx`` ``lcdx``,
        and calls ``subcls.add_to_lcd(lcdx)`` on all subclasses ``subcls``
        of ``ConfiguratorABC`` *which implement the method*, in breadth-first
        order, passing the same ``LoggingConfigDictEx`` instance to each.

        After calling all the ``add_to_lcd`` implementations,
        this method calls ``lcdx.config()`` to configure logging.

        **Note**: ``configure_logging()`` will call ``add_to_lcd`` only on
        ``ConfiguratorABC`` subclasses that have actually been imported
        at the time ``configure_logging()`` is called.
        Thus, make sure that your program has imported all such subclasses
        before it calls this method. If the contributions of the ``add_to_lcd``
        method of some such subclass have no effect — its handlers and/or
        loggers do nothing — it may be because the subclass wasn't
        imported when ``configure_logging()`` was called.
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
