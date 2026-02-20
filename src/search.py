import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет операции, в описании которых содержится заданная строка (регистронезависимо).

    Args:
        data: Список словарей с данными операций.
        search: Строка для поиска в поле 'description'.

    Returns:
        Список операций, где в 'description' найдена подстрока search.

    Examples:
        >>> data = [{"description": "Перевод на карту"}, {"description": "Оплата услуг"}]
        >>> process_bank_search(data, "карт")
        [{"description": "Перевод на карту"}]
        >>> process_bank_search(data, "нету")
        []
    """
    result = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for item in data:
        description = item.get("description", "")
        if description and pattern.search(description):
            result.append(item)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям в поле description.

    Args:
        data: Список словарей с данными операций.
        categories: Список категорий (строк) для поиска в description.

    Returns:
        Словарь {категория: количество операций}, где категория найдена в description.

    Examples:
        >>> data = [{"description": "Перевод на карту"}, {"description": "Оплата услуг"}]
        >>> process_bank_operations(data, ["карт", "оплата"])
        {'карт': 1, 'оплата': 1}
        >>> process_bank_operations(data, ["еда"])
        {'еда': 0}
    """
    counter = Counter()

    for item in data:
        description = item.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                counter[category] += 1

    return dict(counter)
