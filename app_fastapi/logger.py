# Standard library
import logging
import sys


def setup_fastapi_logger():
    """
    Configure and return a logger for the FastAPI application.

    This function:
      - Retrieves or creates a logger named "app_fastapi".
      - Sets the overall log level to DEBUG.
      - Defines a log message format including timestamp, logger name, level,
        module, line number, and message.
      - Adds two handlers:
          1. Console handler (stdout) at INFO level.
          2. File handler ("app_fastapi.log") at DEBUG level.
      - Clears any existing handlers to avoid duplicate logs.
      - Attaches the new handlers to the logger.
    Returns:
        logging.Logger: Configured FastAPI application logger.
    """
    logger = logging.getLogger("app_fastapi")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s "
        "| %(module)s:%(lineno)d | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("app_fastapi.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


logger = setup_fastapi_logger()
