import logging


_logger_name = None         # set by logging_config_sub


# print("__name__ = %r    __package__ = %r" % (__name__, __package__), flush=True)


def logging_config_sub(lcd_ex,
                       loggername,
                       file_handler=None):
    global _logger_name
    _logger_name = loggername + '.sub_prop'
    lcd_ex.add_logger(_logger_name)   # propagate=True, logging default


def do_something_boring(n):
    logging.getLogger(_logger_name).debug("Doing something boring with %d" % n)


def do_something_special(n):
    logging.getLogger(_logger_name).info("Doing something SPECIAL with %d" % n)
