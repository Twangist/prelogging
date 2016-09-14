__author__ = 'brianoneill'

import logging

__all__ = ['do_package_thing', 'do_something', 'do_something_else']


def do_package_thing():
    logger = logging.getLogger(__package__)
    logger.info("INFO msg from package logger")
    print("Did package thing.")

def do_something():
    logger = logging.getLogger(__name__)
    logger.debug("DEBUG msg")
    logger.info("INFO msg")
    print("Did something.")

def do_something_else():
    logging.getLogger(__name__ + '.other').warning("WARNING msg")
    print("Did something else.")
