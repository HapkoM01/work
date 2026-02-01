import json
import os

def get_financial_transactions(file_path):
    """
    Читает данные из JSON-файла.
    Возвращает список словарей или пустой список при ошибках.
    """
    # Проверка существования файла (требование из ТЗ)
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Проверка, что внутри именно список (требование из ТЗ)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []
