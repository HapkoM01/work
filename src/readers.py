import logging
import os
from typing import Any, Dict, List

import pandas as pd

from .logging_config import setup_module_logger

logger = setup_module_logger("readers", level=logging.DEBUG)


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые транзакции из CSV-файла.

    Функция ожидает, что файл использует разделитель ';'.
    Возвращает данные в формате списка словарей, совместимом с остальной логикой проекта.

    Args:
        file_path: Путь к CSV-файлу.

    Returns:
        Список словарей с данными транзакций.

    Raises:
        ValueError: Если файл не найден, пустой или содержит некорректные данные.
    """
    logger.debug(f"Попытка чтения транзакций из CSV: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"CSV-файл не найден: {file_path}")
        raise ValueError(f"CSV-файл не найден: {file_path}")

    try:
        df = pd.read_csv(file_path, sep=";", dtype=str)

        # Если файл пустой или содержит только заголовок — возвращаем []
        if df.empty or len(df.columns) == 0:
            logger.info(f"CSV-файл {file_path} пустой или содержит только заголовки")
            return []

        df.columns = df.columns.str.lower().str.strip()
        records = df.to_dict(orient="records")
        logger.info(f"Успешно прочитано {len(records)} транзакций из CSV {file_path}")
        return records

    except pd.errors.EmptyDataError:
        # Специально обрабатываем пустой файл / только заголовок
        logger.info(f"CSV-файл {file_path} пустой или содержит только заголовки")
        return []
    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга CSV-файла {file_path}: {e}")
        raise ValueError(f"Невозможно разобрать CSV-файл: {e}")
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при чтении CSV {file_path}")
        raise ValueError(f"Ошибка при чтении CSV-файла: {str(e)}")


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые транзакции из Excel-файла (.xlsx).

    Читает первый лист файла. Возвращает данные в формате списка словарей.

    Args:
        file_path: Путь к XLSX-файлу.

    Returns:
        Список словарей с данными транзакций.

    Raises:
        ValueError: Если файл не найден, пустой или содержит некорректные данные.
    """
    logger.debug(f"Попытка чтения транзакций из Excel: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"Excel-файл не найден: {file_path}")
        raise ValueError(f"Excel-файл не найден: {file_path}")

    try:
        df = pd.read_excel(file_path, engine="openpyxl", dtype=str)
        if df.empty:
            logger.info(f"Excel-файл {file_path} пустой")
            return []

        # Приводим названия столбцов к нижнему регистру и убираем лишние пробелы
        df.columns = df.columns.str.lower().str.strip()

        records = df.to_dict(orient="records")
        logger.info(f"Успешно прочитано {len(records)} транзакций из Excel {file_path}")
        return records

    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга Excel-файла {file_path}: {e}")
        raise ValueError(f"Невозможно разобрать Excel-файл: {e}")
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при чтении Excel {file_path}")
        raise ValueError(f"Ошибка при чтении Excel-файла: {str(e)}")
