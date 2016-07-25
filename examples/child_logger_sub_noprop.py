import logging


_logger_name = None         # set by logging_config_sub


# print("__name__ = %r    __package__ = %r" % (__name__, __package__), flush=True)


def logging_config_sub(lcd_ex,
                       parent_loggername,
                       # *,
                       file_handler):
    """
    Set this logger to propagate=False:
    the handlers of parent_loggername WON'T be used.
    So this logger will need its own handlers.
    """
    global _logger_name
    _logger_name = parent_loggername + '.sub_noprop'

    # clone console handler, set loglevel = DEBUG
    #### # lcd_ex.handlers['console_DEBUG']['level'] = 'DEBUG'
    lcd_ex.clone_handler(clone='console_DEBUG', handler='console', attach_to_root=False)
    lcd_ex.set_handler_level('console_DEBUG', 'DEBUG')

    # Use handlers 'console_DEBUG' and file handler file_handler
    lcd_ex.add_logger(_logger_name,
                      handlers=['console_DEBUG', file_handler],
                      propagate=False)   # propagate=True, logging default


def do_something_boring(n):
    logging.getLogger(_logger_name).debug("Doing something boring with %d" % n)


def do_something_special(n):
    logging.getLogger(_logger_name).info("Doing something SPECIAL with %d" % n)

