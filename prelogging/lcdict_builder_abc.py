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
    ``add_to_lcdict(lcd: LCDict)``. Every package or module that
    wants a say in the configuration of logging should define its own
    (sub*)subclass of ``LCDictBuilderABC`` implementing ``add_to_lcdict``.

    Once (and once only), the application should call the classmethod
    ``LCDict.build_lcdict(...)``, which returns an ``LCDict``. The parameters
    of ``build_lcdict`` are the same as those of ``LCDict.__init__``.
    ``build_lcdict`` does the following:

        * creates a new ``LCDict``, ``lcd``, with the parameters provided;
        * calls ``subcls.add_to_lcdict(lcd)`` on every subclass ``subcls``
          that implements ``add_to_lcdict``, in a breadth-first way;
        * returns ``lcd``, the logging config dict built by the previous
          steps.

    Your program should then call ``config()`` on the returned logging config
    dict.

    For example, given the following inheritance tree (where "<" means
    "is a superclass of"):

    .. code::

        LCDictBuilderABC < MainBuilder < BuilderModuleA
                                       < BuilderModuleB
                                       < BuilderPackage < BuilderSubPackage

    Assuming that all classes shown implement ``add_to_lcdict``, that method
    will be called first on ``MainBuilder``; then on
    ``BuilderModuleA``, ``BuilderModuleB``, and
    ``BuilderPackage``, in some order; then on ``BuilderSubPackage``.

    See the test ``test_lcd_builder.py`` for a multi-module example
    of these capabilities.
    |hr|
    """
    @classmethod
    @abstractmethod
    def add_to_lcdict(cls, lcd):          # pragma: no cover
        """(abstractmethod) Customize the passed ``LCDict``.

        :param lcd: an ``LCDict``

        ``build_lcd`` calls this method on every ``LCDictBuilderABC``
        subclass that implements it, **in breadth-first order**.
        All implementations are passed the same
        object ``lcd``. Implementations should call ``LCDict``
        methods on ``lcd`` to augment and customize it.

        **Note**: Implementations should *not* call ``super().add_to_lcdict`` —
        it has already been called by ``build_lcdict``!
        """
        pass

    @classmethod
    def build_lcdict(cls,
                     root_level='WARNING',
                     log_path='',
                     locking=False,
                     attach_handlers_to_root=False,
                     disable_existing_loggers=False):
        """A single method which creates an ``LCDict``, and returns it
        after calling all ``add_to_lcdict`` methods with that object. Your
        program should call this method once (only), and then call ``config()``
        on the returned logging config dict.

        Parameters are as for ``LCDict.__init__``.

        This method creates an ``LCDict`` ``lcd``, and calls
        ``subcls.add_to_lcdict(lcd)`` on all subclasses ``subcls``
        of ``LCDictBuilderABC`` *which implement the method*, in breadth-first
        order, passing the same ``LCDict`` instance to each.

        **Note**: ``build_lcdict()`` will call ``add_to_lcdict`` only on
        ``LCDictBuilderABC`` subclasses that have actually been imported
        at the time ``build_lcdict()`` is called.
        Thus, make sure that your program has imported all such subclasses
        before it calls this method. If the contributions of the ``add_to_lcdict``
        method of some such subclass have no effect — its handlers and/or
        loggers do nothing — it may be because the subclass wasn't imported
        when ``build_lcdict()`` was called.

        :return: the built ``LCDict``
        """
        lcd = LCDict(
                    root_level=root_level,
                    log_path=log_path,
                    locking=locking,
                    attach_handlers_to_root=attach_handlers_to_root,
                    disable_existing_loggers=disable_existing_loggers
        )
        derived_classes = LCDictBuilderABC.__subclasses__()

        while derived_classes:
            subcls = derived_classes.pop()
            if 'add_to_lcdict' in vars(subcls):    # i.e. in subcls.__dict__
                subcls.add_to_lcdict(lcd)
            derived_classes.extend(subcls.__subclasses__())

        return lcd
