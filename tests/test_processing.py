import unittest

from src.processing import filter_by_state, sort_by_date

# Тестовые данные
TEST_DATA = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def test_filter_by_state_executed():
    """
    Тест фильтрации по статусу EXECUTED (значение по умолчанию).
    """
    result = filter_by_state(TEST_DATA)

    # Проверяем количество найденных операций
    assert len(result) == 2

    # Проверяем, что все операции имеют статус EXECUTED
    assert all(operation["state"] == "EXECUTED" for operation in result)

    # Проверяем ID найденных операций
    result_ids = {operation["id"] for operation in result}
    expected_ids = {41428829, 939719570}
    assert result_ids == expected_ids


def test_filter_by_state_canceled():
    """
    Тест фильтрации по статусу CANCELED.
    """
    result = filter_by_state(TEST_DATA, "CANCELED")

    assert len(result) == 2
    assert all(operation["state"] == "CANCELED" for operation in result)

    result_ids = {operation["id"] for operation in result}
    expected_ids = {594226727, 615064591}
    assert result_ids == expected_ids


def test_filter_by_state_empty_result():
    """
    Тест фильтрации по несуществующему статусу.
    """
    result = filter_by_state(TEST_DATA, "PENDING")
    assert len(result) == 0
    assert result == []


def test_filter_by_state_empty_input():
    """
    Тест фильтрации пустого списка.
    """
    result = filter_by_state([], "EXECUTED")
    assert result == []


def test_sort_by_date_descending():
    """
    Тест сортировки по убыванию (по умолчанию).
    """
    result = sort_by_date(TEST_DATA, descending=True)

    # Проверяем порядок дат (от новой к старой)
    dates = [operation["date"] for operation in result]
    expected_dates = [
        "2019-07-03T18:35:29.512364",
        "2018-10-14T08:21:33.419441",
        "2018-09-12T21:27:25.241689",
        "2018-06-30T02:08:58.425572",
    ]
    assert dates == expected_dates

    # Проверяем первый элемент (самая новая операция)
    assert result[0]["id"] == 41428829
    assert result[0]["date"] == "2019-07-03T18:35:29.512364"


def test_sort_by_date_ascending():
    """
    Тест сортировки по возрастанию.
    """
    result = sort_by_date(TEST_DATA, descending=False)

    dates = [operation["date"] for operation in result]
    expected_dates = [
        "2018-06-30T02:08:58.425572",
        "2018-09-12T21:27:25.241689",
        "2018-10-14T08:21:33.419441",
        "2019-07-03T18:35:29.512364",
    ]
    assert dates == expected_dates

    # Первый элемент - самая старая операция
    assert result[0]["id"] == 939719570
    assert result[0]["date"] == "2018-06-30T02:08:58.425572"


def test_sort_by_date_single_element():
    """
    Тест сортировки списка с одним элементом.
    """
    single_data = [{"id": 1, "state": "EXECUTED", "date": "2023-01-01T00:00:00.000000"}]
    result = sort_by_date(single_data)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_sort_by_date_empty_list():
    """
    Тест сортировки пустого списка.
    """
    result = sort_by_date([])
    assert result == []


def test_combined_filter_and_sort():
    """
    Тест комбинирования фильтрации и сортировки.
    """
    # Фильтруем EXECUTED и сортируем по убыванию
    executed = filter_by_state(TEST_DATA, "EXECUTED")
    sorted_executed = sort_by_date(executed, descending=True)

    assert len(sorted_executed) == 2
    assert sorted_executed[0]["id"] == 41428829  # Более новая EXECUTED
    assert sorted_executed[1]["id"] == 939719570  # Более старая EXECUTED


if __name__ == "__main__":
    # Запуск тестов вручную
    pytest.main([__file__, "-v"])
