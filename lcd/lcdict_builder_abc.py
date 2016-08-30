# coding=utf-8

__author__ = 'brianoneill'

from .lcdict import LCDict
from .six import add_metaclass

from abc import ABCMeta, abstractmethod

__all__ = [
    'LCDictBuilderABC',
]

@add_metaclass(ABCMeta)
class LCDictBuilderABC():
    """
    .. include:: _global.rst

    A class for automating multi-package / multi-module logging configuration.
    ``LCDictBuilderABC`` is an abstract base class: its metaclass is ``ABCMeta``,
    defined in ``_collections_abc.py`` of the standard library. You can't
    directly instantiate this class: it has an `abstractmethod`
    ``add_to_lcd(lcdx: LCDict)``. Every package or module that
    wants a say in the configuration of logging should define its own
    (sub*)subclass of ``LCDictBuilderABC`` that implements ``add_to_lcd``.

    Once (and once only), the application should call ``build_lcd()``,
    a classmethod which

        * creates a "blank" ``LCDict``, ``lcdx``;
        * calls ``subcls.add_to_lcd(lcdx)`` on every subclass ``subcls``
          that implements ``add_to_lcd``, in a breadth-first way;
        * returns ``lcdx``, the logging config dict built by the previous
          steps.

    Your program should then call ``config()`` on the returned logging config
    dict.

    For example, given the following inheritance tree (where "<" means
    "is a superclass of"):

    .. code::

        LCDictBuilderABC < MainBuilder < BuilderModuleA
                                    < BuilderModuleB
                                    < BuilderPackage < BuilderSubPackage

    Assuming that all classes shown implement ``add_to_lcd``, that method
    will be called first on ``MainBuilder``; then on
    ``BuilderModuleA``, ``BuilderModuleB``, and
    ``BuilderPackage``, in some order; then on ``BuilderSubPackage``.

    See the test ``test_lcd_builder.py`` for a multi-module example
    that uses these capabilities.
    |hr|
    """
    @classmethod
    @abstractmethod
    def add_to_lcd(cls, lcdx):          # pragma: no cover
        """(abstractmethod) Customize the passed ``LCDict``.

        :param lcdx: a ``LCDict``

        ``build_lcd`` calls this method on every ``LCDictBuilderABC``
        subclass that implements it. All implementations are passed the same
        object ``lcdx``. Implementations should call ``LCDict``
        methods on ``lcdx`` to augment and customize it.

        **Note**: Implementations should *not* call ``super().add_to_lcd`` —
        it has already been called by ``build_lcd``!
        """
        pass

    @classmethod
    def build_lcd(cls,
                   root_level='WARNING',
                   log_path='',
                   locking=False,
                   attach_handlers_to_root=False,
                   disable_existing_loggers=False):
        """A single method which creates a ``LCDict``,
        calls all ``add_to_lcd`` methods with that object. Your program
        should call this method once (only), and then call ``config()``
        on the returned logging config dict.

        Parameters are as for ``LCDict``.

        This method creates a ``LCDict`` ``lcdx``,
        and calls ``subcls.add_to_lcd(lcdx)`` on all subclasses ``subcls``
        of ``LCDictBuilderABC`` *which implement the method*, in breadth-first
        order, passing the same ``LCDict`` instance to each.

        **Note**: ``build_lcd()`` will call ``add_to_lcd`` only on
        ``LCDictBuilderABC`` subclasses that have actually been imported
        at the time ``build_lcd()`` is called.
        Thus, make sure that your program has imported all such subclasses
        before it calls this method. If the contributions of the ``add_to_lcd``
        method of some such subclass have no effect — its handlers and/or
        loggers do nothing — it's quite likely because the subclass wasn't
        imported when ``build_lcd()`` was called.

        return: the built ``LCDict``
        """
        lcdx = LCDict(
                    root_level=root_level,
                    log_path=log_path,
                    locking=locking,
                    attach_handlers_to_root=attach_handlers_to_root,
                    disable_existing_loggers=disable_existing_loggers
        )
        derived_classes = LCDictBuilderABC.__subclasses__()

        while derived_classes:
            subcls = derived_classes.pop()
            if 'add_to_lcd' in vars(subcls):    # i.e. in subcls.__dict__
                subcls.add_to_lcd(lcdx)
            derived_classes.extend(subcls.__subclasses__())

        return lcdx
