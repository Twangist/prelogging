import logging


def report_name_package():
    logging.getLogger(__name__).info("__name__ = %r    __package__ = %r"
                                     % (__name__, __package__))


def logging_config_sub(lcd):
    """
    Set this logger to propagate=False:
    the handlers of parent_loggername WON'T be used.
    So this logger will need its own handlers.
    """
    # # clone console handler, DON'T add to root, set loglevel = DEBUG
    lcd.clone_handler(clone='console_DEBUG',
                      handler='console',
                      attach_to_root=False)
    lcd.set_handler_level('console_DEBUG', 'DEBUG')

    # use file handler 'app_file' (magic string eh)
    lcd.add_logger(__name__,
                   handlers=['console_DEBUG', 'app_file'],
                   propagate=False)   # propagate=True, logging default


def do_something_boring(n):
    logging.getLogger(__name__).debug("Doing something boring with %d" % n)


def do_something_special(n):
    logging.getLogger(__name__).info("Doing something SPECIAL with %d" % n)

