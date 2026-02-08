from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует операции по статусу.

    Args:
        operations: Список словарей с данными операций
        state: Статус для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Отфильтрованный список операций

    Examples:
        >>> ops = [
        ...     {'id': 1, 'state': 'EXECUTED'},
        ...     {'id': 2, 'state': 'CANCELED'},
        ... ]
        >>> filter_by_state(ops, 'EXECUTED')
        [{'id': 1, 'state': 'EXECUTED'}]
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует операции по дате.

    Args:
        operations: Список словарей с данными операций
        descending: Порядок сортировки (True - по убыванию, False - по возрастанию)

    Returns:
        Отсортированный список операций

    Examples:
        >>> ops = [
        ...     {'id': 1, 'date': '2023-01-01'},
        ...     {'id': 2, 'date': '2023-02-01'},
        ... ]
        >>> sort_by_date(ops, True)
        [{'id': 2, 'date': '2023-02-01'}, {'id': 1, 'date': '2023-01-01'}]
    """
    return sorted(operations, key=lambda x: x.get("date", ""), reverse=descending)


if __name__ == "__main__":
    # Примеры использования
    test_operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    print("Фильтрация по статусу 'EXECUTED':")
    executed = filter_by_state(test_operations, "EXECUTED")
    for op in executed:
        print(f"  ID: {op['id']}, Date: {op['date']}")

    print("\nФильтрация по статусу 'CANCELED':")
    canceled = filter_by_state(test_operations, "CANCELED")
    for op in canceled:
        print(f"  ID: {op['id']}, Date: {op['date']}")

    print("\nСортировка по убыванию (новые сначала):")
    sorted_desc = sort_by_date(test_operations, True)
    for op in sorted_desc:
        print(f"  ID: {op['id']}, Date: {op['date']}")

    print("\nСортировка по возрастанию (старые сначала):")
    sorted_asc = sort_by_date(test_operations, False)
    for op in sorted_asc:
        print(f"  ID: {op['id']}, Date: {op['date']}")
