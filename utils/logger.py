import logging
from datetime import datetime
import os

ENABLE_LOGGING = False  # Global flag

def setup_logging(enable: bool, log_path: str = None, level: str = "INFO"):
    """
    Set up application-wide logging.

    :param enable: Whether to enable logging.
    :param log_path: Optional file path for the log file.
    :param level: Logging level (e.g., "INFO", "DEBUG", "WARNING").
    """
    global ENABLE_LOGGING
    ENABLE_LOGGING = enable

    if not enable:
        return

    # Convert level string to logging constant
    level_value = getattr(logging, level.upper(), logging.INFO)

    # Default log path
    if not log_path:
        log_path = f"logs/quiz.{datetime.now().strftime('%Y-%m-%d')}.log"

    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Avoid duplicate log handlers
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            filename=log_path,
            level=level_value,
            format="%(asctime)s - %(levelname)s - %(message)s"
            encoding="utf-8"
        )

    logging.info("Logging started.")

def log_message(action, user_id, content):
    """
    Logs a message if logging is enabled.

    :param action: Type of log (e.g., "Sent", "Error", "Feedback").
    :param user_id: Telegram user ID.
    :param content: Message content.
    """
    if ENABLE_LOGGING:
        logging.info(f"{action} | User: {user_id} | Content: {content}")