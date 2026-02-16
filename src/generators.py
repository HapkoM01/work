from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по указанному коду валюты.

    Возвращает итератор (ленивый), содержащий только те транзакции,
    у которых код валюты совпадает с переданным. Некорректные транзакции пропускаются.

    Args:
        transactions: Список словарей с данными транзакций.
                      Каждый словарь должен содержать вложенную структуру
                      "operationAmount" → "currency" → "code".
        currency_code: Трёхбуквенный код валюты (например, "USD", "RUB", "EUR").

    Yields:
        Словарь транзакции, если её валюта соответствует currency_code.

    Raises:
        ValueError: Если передан пустой код валюты (currency_code == "").

    Examples:
        >>> transactions = [
        ...     {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        ...     {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}},
        ...     {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
        ... ]
        >>> usd_list = list(filter_by_currency(transactions, "USD"))
        >>> len(usd_list)
        2
        >>> usd_list[0]["operationAmount"]["currency"]["code"]
        'USD'

        >>> list(filter_by_currency(transactions, ""))
        Traceback (most recent call last):
            ...
        ValueError: Код валюты не может быть пустым
    """
    if not currency_code:
        raise ValueError("Код валюты не может быть пустым")

    for transaction in transactions:
        try:
            if transaction["operationAmount"]["currency"]["code"] == currency_code:
                yield transaction
        except (KeyError, TypeError):
            continue  # Пропускаем транзакции с некорректной структурой


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генератор описаний транзакций.

    Возвращает описание каждой транзакции. Если описание отсутствует — возвращает пустую строку.

    Args:
        transactions: Список словарей с данными транзакций.

    Yields:
        Описание транзакции (строка) или пустая строка "".

    Examples:
        >>> transactions = [
        ...     {"description": "Перевод"},
        ...     {"description": "Покупка"},
        ...     {},
        ...     {"description": None},
        ... ]
        >>> list(transaction_descriptions(transactions))
        ['Перевод', 'Покупка', '', '']
    """
    for transaction in transactions:
        yield transaction.get("description", "") or ""


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генератор номеров кредитных карт от start до stop-1.

    Каждый номер форматируется как 16-значная строка с пробелами каждые 4 цифры.

    Args:
        start: Начальный номер (включительно).
        stop: Конечный номер (не включительно).

    Yields:
        Форматированный номер карты в виде "XXXX XXXX XXXX XXXX".

    Examples:
        >>> list(card_number_generator(1, 4))
        ['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003']

        >>> list(card_number_generator(5, 5))
        []  # пустой диапазон

        >>> next(card_number_generator(1234567890123456, 1234567890123457))
        '1234 5678 9012 3456'
    """
    for num in range(start, stop):
        # Дополняем до 16 цифр нулями слева
        card_num = f"{num:016d}"
        # Форматируем с пробелами каждые 4 цифры
        formatted = " ".join(card_num[i : i + 4] for i in range(0, 16, 4))
        yield formatted
