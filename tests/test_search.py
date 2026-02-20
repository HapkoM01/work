import pytest

from src.search import process_bank_operations, process_bank_search


@pytest.fixture
def sample_operations():
    return [
        {"description": "Перевод на карту"},
        {"description": "Оплата услуг"},
        {"description": "Открытие вклада"},
        {"description": "Перевод организации"},
    ]


def test_process_bank_search_found(sample_operations):
    result = process_bank_search(sample_operations, "перевод")
    assert len(result) == 2
    assert all("перевод" in r["description"].lower() for r in result)


def test_process_bank_search_not_found(sample_operations):
    result = process_bank_search(sample_operations, "еда")
    assert result == []


def test_process_bank_operations(sample_operations):
    result = process_bank_operations(sample_operations, ["перевод", "оплата"])
    assert result == {"перевод": 2, "оплата": 1}


def test_process_bank_operations_empty():
    """Пустой список транзакций → пустой словарь категорий."""
    result = process_bank_operations([], ["перевод"])
    assert result == {}
