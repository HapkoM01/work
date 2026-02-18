from unittest.mock import MagicMock, patch

import pytest
import requests  # ← обязательно импортируем для exceptions

from src.external_api import convert_to_rub


@pytest.mark.parametrize(
    "currency, amount, expected",
    [
        ("RUB", "1500.0", 1500.0),
        ("USD", "1500.0", 0.0),
        ("EUR", "1000.0", 0.0),
        ("GBP", "2000.0", 0.0),
        ("JPY", "5000.0", 0.0),
    ],
    ids=["RUB direct", "USD fallback", "EUR fallback", "GBP unsupported", "JPY unsupported"],
)
def test_convert_to_rub_basic_cases(currency, amount, expected):
    """Базовые случаи без обращения к API."""
    transaction = {"operationAmount": {"amount": amount, "currency": {"code": currency}}}
    result = convert_to_rub(transaction)
    assert result == expected


@patch("requests.get")
def test_convert_to_rub_api_success(mock_get):
    """Успешный ответ от API."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 135000.75}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "1500.0", "currency": {"code": "USD"}}}

    result = convert_to_rub(transaction)

    assert result == 135000.75
    mock_get.assert_called_once()
    # Можно проверить URL, если хочешь
    args, kwargs = mock_get.call_args
    assert "convert?to=RUB&from=USD&amount=1500.0" in args[0]


@patch("requests.get")
def test_convert_to_rub_api_missing_result_key(mock_get):
    """API вернул 200, но без ключа 'result' → 0.0"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}  # нет result
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "100.0", "currency": {"code": "EUR"}}}

    result = convert_to_rub(transaction)
    assert result == 0.0


@patch("requests.get")
def test_convert_to_rub_api_http_error(mock_get):
    """HTTP-ошибка (например 401) → 0.0"""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "500.0", "currency": {"code": "USD"}}}

    result = convert_to_rub(transaction)
    assert result == 0.0


@patch("requests.get")
def test_convert_to_rub_connection_error(mock_get):
    """Сетевая ошибка → 0.0"""
    mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")

    transaction = {"operationAmount": {"amount": "300.0", "currency": {"code": "EUR"}}}

    result = convert_to_rub(transaction)
    assert result == 0.0


def test_convert_to_rub_invalid_transaction_structure():
    """Некорректная структура данных → 0.0"""
    assert convert_to_rub({}) == 0.0
    assert convert_to_rub({"operationAmount": {}}) == 0.0
    assert convert_to_rub({"operationAmount": {"amount": "abc"}}) == 0.0
    assert convert_to_rub({"operationAmount": {"currency": {"code": "USD"}}}) == 0.0


@patch("requests.get")
def test_convert_to_rub_timeout_error(mock_get):
    """Таймаут запроса → 0.0"""
    mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

    transaction = {"operationAmount": {"amount": "400.0", "currency": {"code": "USD"}}}

    result = convert_to_rub(transaction)
    assert result == 0.0
