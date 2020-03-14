import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = \
    logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s:%(funcName)s:%(lineno)d : %(message)s')

LOG_FILE = '/tmp/patternomatic.log'


def get_console_handler():
    """
    Console handler logger
    Returns:

    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    """
    File handler logger
    Returns:

    """
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    """
    Returns a set up logger
    Args:
        logger_name: Name of the logger

    Returns: logger

    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.CRITICAL)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


LOG = get_logger('PatternOmatic')
