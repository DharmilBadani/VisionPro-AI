"""
Centralized logging configuration.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from config.settings import Config
from utils.constants import LOG_FORMAT


def setup_logger(name="visionai"):
    """
    Configure and return a reusable logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(
        getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
    )

    log_directory = os.path.dirname(Config.LOG_FILE)

    if log_directory:
        os.makedirs(log_directory, exist_ok=True)

    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )

    file_handler.setFormatter(
        logging.Formatter(LOG_FORMAT)
    )

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(
        logging.Formatter(LOG_FORMAT)
    )

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.propagate = False

    return logger


logger = setup_logger()