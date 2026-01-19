from typing import Dict, Any, Iterator, List, Generator


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по коду валюты и возвращает итератор.

    Args:
        transactions: Список словарей с транзакциями
        currency_code: Код валюты для фильтрации (например, 'USD', 'RUB')

    Yields:
        Словарь транзакции, где валюта соответствует заданной

    Examples:
        >>> transactions = [
        ...     {
        ...         "id": 1,
        ...         "operationAmount": {"currency": {"code": "USD"}}
        ...     },
        ...     {
        ...         "id": 2,
        ...         "operationAmount": {"currency": {"code": "RUB"}}
        ...     }
        ... ]
        >>> usd_transactions = filter_by_currency(transactions, "USD")
        >>> next(usd_transactions)["id"]
        1
    """
    for transaction in transactions:
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
                yield transaction
        except (AttributeError, KeyError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генератор, который возвращает описания транзакций.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание транзакции (строка)

    Examples:
        >>> transactions = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод со счета на счет"}
        ... ]
        >>> descriptions = transaction_descriptions(transactions)
        >>> next(descriptions)
        'Перевод организации'
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Args:
        start: Начальный номер (включительно)
        stop: Конечный номер (исключительно)

    Yields:
        Номер карты в формате "XXXX XXXX XXXX XXXX"

    Examples:
        >>> for card in card_number_generator(1, 4):
        ...     print(card)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
    """
    for number in range(start, stop):
        # Форматируем номер: 16 цифр с ведущими нулями
        card_number = f"{number:016d}"
        # Разбиваем на группы по 4 цифры
        formatted = " ".join([card_number[i:i + 4] for i in range(0, 16, 4)])
        yield formatted


if __name__ == "__main__":
    # Примеры использования
    print("Примеры работы модуля generators:")
    print("=" * 60)

    # Тестовые данные
    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]

    print("\n1. Фильтрация по валюте (USD):")
    usd_transactions = filter_by_currency(sample_transactions, "USD")
    for i, transaction in enumerate(usd_transactions, 1):
        print(f"  Транзакция {i}: ID={transaction['id']}, Сумма={transaction['operationAmount']['amount']} USD")

    print("\n2. Описания транзакций:")
    descriptions = transaction_descriptions(sample_transactions)
    for i, description in enumerate(descriptions, 1):
        print(f"  Описание {i}: {description}")

    print("\n3. Генерация номеров карт (1-5):")
    for card_number in card_number_generator(1, 6):
        print(f"  {card_number}")
