"""Logger utility for the FastAPI application."""

import logging
import sys


def setup_logger() -> logging.Logger:
    """Set up and return a logger for the FastAPI application.

    The logger is configured to log messages at the DEBUG level and outputs
    them to the console with a specific format that includes the timestamp,
    log level, and message.

    Returns:
        logging.Logger: Configured logger instance.

    """
    logger = logging.getLogger("fastapi_app")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
