import json
import os
import logging
from .logging_config import setup_module_logger

logger = setup_module_logger("utils", level=logging.DEBUG)


def get_financial_transactions(file_path: str) -> list[dict]:
    logger.debug(f"Попытка чтения операций из файла: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info(f"Успешно прочитано {len(data)} операций из {file_path}")
                return data
            else:
                logger.error(f"Данные в файле не являются списком: {type(data)}")
                return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при чтении файла {file_path}")
        return []
