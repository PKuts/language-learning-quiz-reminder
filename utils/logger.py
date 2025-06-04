import logging
from datetime import datetime
import os

ENABLE_LOGGING = False  # Global flag for manual logging control

def setup_logging(enable: bool, log_path: str = None):
    global ENABLE_LOGGING
    ENABLE_LOGGING = enable

    if not enable:
        return

    if not log_path:
        log_path = f"logs/project.{datetime.now().strftime('%Y-%m-%d')}.log"

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Logging started.")

def log_message(action, user_id, content):
    if ENABLE_LOGGING:
        logging.info(f"{action} | User: {user_id} | Content: {content}")