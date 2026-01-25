import pytest


@pytest.fixture
def common_operations():
    """Общая фикстура с операциями для тестов."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
def sample_transactions():
    """Sample transactions data for testing generators."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD",
                },
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD",
                },
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB",
                },
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD",
                },
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB",
                },
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
        # Edge cases
        {
            "id": 999999999,
            "state": "EXECUTED",
            "date": "2020-01-01T00:00:00.000000",
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "name": "EUR",
                    "code": "EUR",
                },
            },
            "description": "Международный перевод",
            "from": "MasterCard 5555555555554444",
            "to": "Счет 12345678901234567890",
        },
        # Malformed transaction (missing currency)
        {
            "id": 888888888,
            "state": "EXECUTED",
            "date": "2020-02-02T00:00:00.000000",
            "description": "Без валюты",
        },
        # Malformed transaction (missing operationAmount)
        {
            "id": 777777777,
            "state": "EXECUTED",
            "date": "2020-03-03T00:00:00.000000",
            "description": "Без суммы операции",
            "from": "Visa 4111111111111111",
            "to": "Visa 4222222222222222",
        },
    ]


@pytest.fixture
def empty_transactions():
    """Empty transactions list for testing."""
    return []


@pytest.fixture
def transactions_without_descriptions():
    """Transactions without descriptions."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T00:00:00.000000",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "from": "Card 1111",
            "to": "Card 2222",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2023-01-02T00:00:00.000000",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "",  # Empty description
            "from": "Card 3333",
            "to": "Card 4444",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2023-01-03T00:00:00.000000",
            "operationAmount": {
                "amount": "300.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": None,  # None description
            "from": "Card 5555",
            "to": "Card 6666",
        },
    ]