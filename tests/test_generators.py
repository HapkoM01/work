from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Фикстуры для тестовых данных
@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком транзакций."""
    return []


@pytest.fixture
def transactions_without_currency() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями без информации о валюте."""
    return [
        {"id": 1, "description": "Транзакция 1"},
        {"id": 2, "operationAmount": {"amount": "100"}},
        {"id": 3, "operationAmount": {"amount": "200", "currency": {}}},
    ]


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_usd_transactions(self, sample_transactions):
        """Тест фильтрации USD транзакций."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 3
        assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_transactions)

    def test_filter_rub_transactions(self, sample_transactions):
        """Тест фильтрации RUB транзакций."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 1
        assert rub_transactions[0]["id"] == 873106923

    def test_filter_nonexistent_currency(self, sample_transactions):
        """Тест фильтрации по несуществующей валюте."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0

    def test_empty_transactions(self, empty_transactions):
        """Тест с пустым списком транзакций."""
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert result == []

    def test_transactions_without_currency(self, transactions_without_currency):
        """Тест с транзакциями без информации о валюте."""
        result = list(filter_by_currency(transactions_without_currency, "USD"))
        assert result == []

    def test_iterator_behavior(self, sample_transactions):
        """Тест поведения итератора."""
        usd_iterator = filter_by_currency(sample_transactions, "USD")
        # Проверяем что это итератор
        assert hasattr(usd_iterator, "__iter__")
        assert hasattr(usd_iterator, "__next__")

        # Получаем первый элемент
        first = next(usd_iterator)
        assert first["id"] == 939719570

        # Получаем второй элемент
        second = next(usd_iterator)
        assert second["id"] == 142264268


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    @pytest.mark.parametrize(
        "index, expected",
        [
            (0, "Перевод организации"),
            (1, "Перевод со счета на счет"),
            (2, "Перевод со счета на счет"),
            (3, "Перевод с карты на карту"),
        ],
    )
    def test_descriptions_order(self, sample_transactions, index, expected):
        """Тест порядка описаний."""
        descriptions = list(transaction_descriptions(sample_transactions))
        assert descriptions[index] == expected

    def test_all_descriptions(self, sample_transactions):
        """Тест всех описаний."""
        descriptions = list(transaction_descriptions(sample_transactions))
        assert len(descriptions) == 4
        assert all(isinstance(desc, str) for desc in descriptions)

    def test_empty_transactions(self, empty_transactions):
        """Тест с пустым списком транзакций."""
        descriptions = list(transaction_descriptions(empty_transactions))
        assert descriptions == []

    def test_transactions_without_description(self):
        """Тест с транзакциями без описания."""
        transactions = [{"id": 1}, {"id": 2, "description": "Есть описание"}, {"id": 3, "description": " "}]
        descriptions = list(transaction_descriptions(transactions))
        assert descriptions == ["Есть описание", " "]

    def test_generator_behavior(self, sample_transactions):
        """Тест поведения генератора."""
        desc_generator = transaction_descriptions(sample_transactions)
        assert hasattr(desc_generator, "__iter__")
        assert hasattr(desc_generator, "__next__")

        first = next(desc_generator)
        assert first == "Перевод организации"


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    @pytest.mark.parametrize(
        "start, stop, expected_count", [(1, 5, 4), (10, 15, 5), (1, 1, 0), (9999999999999990, 9999999999999999, 9)]
    )
    def test_range_length(self, start, stop, expected_count):
        """Тест длины диапазона."""
        cards = list(card_number_generator(start, stop))
        assert len(cards) == expected_count

    @pytest.mark.parametrize(
        "number, expected_format",
        [
            (1, "0000 0000 0000 0001"),
            (1234, "0000 0000 0000 1234"),
            (9999999999999999, "9999 9999 9999 9999"),
            (1000200030004000, "1000 2000 3000 4000"),
        ],
    )
    def test_card_format(self, number, expected_format):
        """Тест формата номеров карт."""
        cards = list(card_number_generator(number, number + 1))
        assert len(cards) == 1
        assert cards[0] == expected_format

    def test_sequential_numbers(self):
        """Тест последовательных номеров."""
        cards = list(card_number_generator(1, 6))
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]
        assert cards == expected

    def test_large_range(self):
        """Тест большого диапазона."""
        cards = list(card_number_generator(9999999999999995, 10000000000000000))
        assert len(cards) == 5
        assert cards[0] == "9999 9999 9999 9995"
        assert cards[-1] == "9999 9999 9999 9999"

    def test_generator_behavior(self):
        """Тест поведения генератора."""
        gen = card_number_generator(1, 3)
        assert hasattr(gen, "__iter__")
        assert hasattr(gen, "__next__")

        first = next(gen)
        assert first == "0000 0000 0000 0001"

        second = next(gen)
        assert second == "0000 0000 0000 0002"

        with pytest.raises(StopIteration):
            next(gen)

    def test_invalid_range(self):
        """Тест с некорректным диапазоном."""
        cards = list(card_number_generator(5, 3))  # start > stop
        assert cards == []


def test_all_functions_integration(sample_transactions):
    """Интеграционный тест всех функций."""
    # Фильтрация
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 3

    # Описания
    descriptions = list(transaction_descriptions(usd_transactions))
    assert len(descriptions) == 3

    # Генерация карт
    cards = list(card_number_generator(1, 4))
    assert cards == ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
