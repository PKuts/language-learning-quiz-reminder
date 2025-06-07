ef setup_logging(enable: bool, log_path: str = None, level: str = "INFO"):
    global ENABLE_LOGGING
    ENABLE_LOGGING = enable

    if not enable:
        return

    level_value = getattr(logging, level.upper(), logging.INFO)

    if not log_path:
        log_path = f"logs/quiz.{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # 🔧 Clear existing handlers
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    logging.basicConfig(
        filename=log_path,
        level=level_value,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    logging.info("Logging started.")