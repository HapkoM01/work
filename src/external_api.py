import pytest
from unittest.mock import patch

from src.external_api import convert_to_rub


@pytest.mark.parametrize("currency, expected", [
    ("RUB", 1500.0),
    ("USD", 0.0),          # без API вернёт 0
    ("EUR", 0.0),
    ("GBP", 0.0),          # неподдерживаемая → 0
])
def test_convert_to_rub_basic_cases(currency, expected):
    transaction = {
        "operationAmount": {
            "amount": "1500.0",
            "currency": {"code": currency}
        }
    }
    result = convert_to_rub(transaction)
    assert result == expected


@patch("requests.get")
def test_convert_to_rub_api_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 135000.0}

    transaction = {
        "operationAmount": {
            "amount": "1500.0",
            "currency": {"code": "USD"}
        }
    }

    result = convert_to_rub(transaction)
    assert result == 135000.0
    mock_get.assert_called_once()


@patch("requests.get")
def test_convert_to_rub_api_failure(mock_get):
    mock_get.side_effect = Exception("Connection error")

    transaction = {
        "operationAmount": {
            "amount": "1000.0",
            "currency": {"code": "EUR"}
        }
    }

    result = convert_to_rub(transaction)
    assert result == 0.0
