import pytest
from unittest.mock import patch, mock_open
from src.utils import get_financial_transactions
from src.external_api import convert_to_rub


def test_get_financial_transactions_valid():
    """Тест успешного чтения корректного JSON-файла."""
    mock_data = '[{"id": 1, "amount": 100}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("os.path.exists", return_value=True):
            assert get_financial_transactions("data/operations.json") == [{"id": 1, "amount": 100}]


def test_get_financial_transactions_not_found():
    """Тест ситуации, когда файл не найден."""
    with patch("os.path.exists", return_value=False):
        assert get_financial_transactions("non_existent.json") == []


def test_get_financial_transactions_invalid_json():
    """Тест обработки битого JSON."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("os.path.exists", return_value=True):
            assert get_financial_transactions("data/operations.json") == []
