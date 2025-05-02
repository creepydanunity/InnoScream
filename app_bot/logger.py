# Standard library
import logging
import sys


def setup_bot_logger():
    """
    Configure and return a logger for the bot application.

    Behavior:
        - Sets up a logger named "app_bot" with DEBUG level.
        - Logs INFO-level messages to stdout using a stream handler.
        - Logs DEBUG-level messages to a file named "app_bot.log".
        - Clears any existing handlers to avoid duplicate logs.
        - Applies a consistent log message format.

    Returns:
        logging.Logger: The configured logger instance.
    """
    
    logger = logging.getLogger("app_bot")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("app_bot.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_bot_logger()