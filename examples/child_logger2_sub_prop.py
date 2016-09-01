import logging


def report_name_package():
    logging.getLogger(__name__).info("__name__ = %r    __package__ = %r"
                                     % (__name__, __package__))


def logging_config_sub(lcd):
    lcd.add_logger(__name__)   # propagate=True, logging default


def do_something_boring(n):
    logging.getLogger(__name__).debug("Doing something boring with %d" % n)


def do_something_special(n):
    logging.getLogger(__name__).info("Doing something SPECIAL with %d" % n)

