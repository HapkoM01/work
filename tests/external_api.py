import pytest
from unittest.mock import patch, MagicMock
from src.external_api import convert_to_rub


@patch("requests.get")
def test_convert_to_rub_api_missing_result(mock_get):
    """Тест случая, когда API вернул JSON, но в нем нет ключа 'result'."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"status": "success"}  # Ключа 'result' нет

    transaction = {
        "operationAmount": {"amount": "50.0", "currency": {"code": "USD"}}
    }

    # Функция должна безопасно вернуть 0.0
    assert convert_to_rub(transaction) == 0.0


@patch("requests.get")
def test_convert_to_rub_http_error(mock_get):
    """Тест обработки HTTP ошибок (например, 401 Unauthorized или 404)."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    # Имитируем вызов raise_for_status, который выбрасывает исключение
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {"amount": "100.0", "currency": {"code": "EUR"}}
    }

    assert convert_to_rub(transaction) == 0.0


def test_convert_to_rub_unsupported_currency():
    """Тест валюты, которая не входит в список поддерживаемых (не RUB, USD, EUR)."""
    transaction = {
        "operationAmount": {"amount": "100.0", "currency": {"code": "GBP"}}
    }
    # Согласно логике кода, для прочих валют возвращается 0.0
    assert convert_to_rub(transaction) == 0.0
