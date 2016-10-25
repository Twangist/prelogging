import logging


_logger_name = None         # set by logging_config_sub


def logging_config_sub(lcd,
                       parent_loggername,
                       # *,
                       file_handler=None):
    """
    Set this logger to propagate=False:
    the handlers of parent_loggername WON'T be used,
    so this logger will need its own handlers.
    """
    global _logger_name
    _logger_name = parent_loggername + '.sub_noprop'

    # clone console handler, loglevel = DEBUG
    lcd.clone_handler(clone='console_DEBUG',
                      handler='console',
                      attach_to_root=False)
    lcd.set_handler_level('console_DEBUG', 'DEBUG')

    # Use handlers 'console_DEBUG' and file handler file_handler
    lcd.add_logger(_logger_name,
                   handlers=['console_DEBUG', file_handler],
                   propagate=False)   # propagate=True, logging default


def do_something_boring(n):
    logging.getLogger(_logger_name).debug("Doing something boring with %d" % n)


def do_something_special(n):
    logging.getLogger(_logger_name).info("Doing something SPECIAL with %d" % n)

