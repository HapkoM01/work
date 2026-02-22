import logging
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_module_logger(module_name: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(level)

    # Удаляем старые handlers, если они были
    logger.handlers.clear()

    # File handler — перезапись при каждом запуске
    file_handler = logging.FileHandler(
        filename=LOGS_DIR / f"{module_name}.log", mode="w", encoding="utf-8"  # ← именно "w" — перезапись
    )

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)

    return logger
