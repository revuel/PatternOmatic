""" Logging module

This file is part of PatternOmatic.

Copyright © 2020  Miguel Revuelta Espinosa

PatternOmatic is free software: you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PatternOmatic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with PatternOmatic. If not, see <https://www.gnu.org/licenses/>.

"""
import logging
import sys
import tempfile
from logging.handlers import TimedRotatingFileHandler

FORMATTER = \
    logging.Formatter('[%(levelname)s] %(asctime)s %(filename)s:%(funcName)s:%(lineno)d : %(message)s')

LOG_FILE = tempfile.gettempdir() + '/patternomatic.log'


def _get_console_handler():
    """
    Console handler logger
    Returns:

    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def _get_file_handler():
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
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_console_handler())
    logger.addHandler(_get_file_handler())
    logger.propagate = False
    return logger


LOG = get_logger('PatternOmatic')
