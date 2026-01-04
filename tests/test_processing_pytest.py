import pytest
from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    @pytest.fixture
    def sample_operations(self):
        """Фикстура с тестовыми операциями."""
        return [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
            {"id": 2, "state": "EXECUTED", "date": "2024-01-02"},
            {"id": 3, "state": "CANCELED", "date": "2024-01-03"},
            {"id": 4, "state": "CANCELED", "date": "2024-01-04"},
            {"id": 5, "state": "PENDING", "date": "2024-01-05"},
            {"id": 6, "state": "EXECUTED", "date": "2024-01-06"},
        ]

    def test_filter_by_executed(self, sample_operations):
        """Тест фильтрации по статусу EXECUTED."""
        result = filter_by_state(sample_operations, "EXECUTED")
        assert len(result) == 3
        assert all(op["state"] == "EXECUTED" for op in result)
        assert [op["id"] for op in result] == [1, 2, 6]

    def test_filter_by_canceled(self, sample_operations):
        """Тест фильтрации по статусу CANCELED."""
        result = filter_by_state(sample_operations, "CANCELED")
        assert len(result) == 2
        assert all(op["state"] == "CANCELED" for op in result)
        assert [op["id"] for op in result] == [3, 4]

    def test_filter_by_default(self, sample_operations):
        """Тест фильтрации со статусом по умолчанию (EXECUTED)."""
        result = filter_by_state(sample_operations)
        assert len(result) == 3
        assert all(op["state"] == "EXECUTED" for op in result)

    def test_filter_none_found(self, sample_operations):
        """Тест когда нет операций с указанным статусом."""
        result = filter_by_state(sample_operations, "NON_EXISTENT")
        assert len(result) == 0
        assert result == []

    def test_empty_list(self):
        """Тест фильтрации пустого списка."""
        result = filter_by_state([], "EXECUTED")
        assert result == []

    def test_operations_without_state(self):
        """Тест операций без ключа state."""
        operations = [
            {"id": 1},
            {"id": 2, "state": "EXECUTED"},
            {"id": 3, "other_key": "value"},
        ]
        result = filter_by_state(operations, "EXECUTED")
        assert len(result) == 1
        assert result[0]["id"] == 2

    @pytest.mark.parametrize(
        "state, expected_count",
        [
            ("EXECUTED", 3),
            ("CANCELED", 2),
            ("PENDING", 1),
            ("INVALID", 0),
        ]
    )
    def test_parametrized_states(self, sample_operations, state, expected_count):
        """Параметризованный тест для разных статусов."""
        result = filter_by_state(sample_operations, state)
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(op["state"] == state for op in result)


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    @pytest.fixture
    def unsorted_operations(self):
        """Фикстура с неотсортированными операциями."""
        return [
            {"id": 1, "date": "2024-03-01", "state": "EXECUTED"},
            {"id": 2, "date": "2024-01-01", "state": "EXECUTED"},
            {"id": 3, "date": "2024-02-01", "state": "CANCELED"},
            {"id": 4, "date": "2024-04-01", "state": "EXECUTED"},
            {"id": 5, "date": "2023-12-31", "state": "CANCELED"},
        ]

    def test_sort_descending_default(self, unsorted_operations):
        """Тест сортировки по убыванию (по умолчанию)."""
        result = sort_by_date(unsorted_operations)
        dates = [op["date"] for op in result]
        assert dates == ["2024-04-01", "2024-03-01", "2024-02-01", "2024-01-01", "2023-12-31"]
        assert result[0]["id"] == 4  # Самая новая
        assert result[-1]["id"] == 5  # Самая старая

    def test_sort_descending_true(self, unsorted_operations):
        """Тест сортировки по убыванию (descending=True)."""
        result = sort_by_date(unsorted_operations, True)
        dates = [op["date"] for op in result]
        assert dates == ["2024-04-01", "2024-03-01", "2024-02-01", "2024-01-01", "2023-12-31"]

    def test_sort_ascending_false(self, unsorted_operations):
        """Тест сортировки по возрастанию (descending=False)."""
        result = sort_by_date(unsorted_operations, False)
        dates = [op["date"] for op in result]
        assert dates == ["2023-12-31", "2024-01-01", "2024-02-01", "2024-03-01", "2024-04-01"]
        assert result[0]["id"] == 5  # Самая старая
        assert result[-1]["id"] == 4  # Самая новая

    def test_empty_list(self):
        """Тест сортировки пустого списка."""
        result = sort_by_date([])
        assert result == []

    def test_single_element(self):
        """Тест сортировки одного элемента."""
        operations = [{"id": 1, "date": "2024-01-01"}]
        result = sort_by_date(operations)
        assert result == operations

    def test_equal_dates(self):
        """Тест сортировки с одинаковыми датами."""
        operations = [
            {"id": 1, "date": "2024-01-01"},
            {"id": 2, "date": "2024-01-01"},
            {"id": 3, "date": "2024-01-01"},
        ]
        result = sort_by_date(operations)
        # Должна сохраняться стабильная сортировка
        assert [op["id"] for op in result] == [1, 2, 3]

    def test_operations_without_date(self):
        """Тест операций без ключа date."""
        operations = [
            {"id": 1, "date": "2024-02-01"},
            {"id": 2},  # Без даты
            {"id": 3, "date": "2024-01-01"},
            {"id": 4, "other": "value"},  # Без даты
        ]
        result = sort_by_date(operations)
        # Операции без даты должны быть в конце
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3
        # Операции без даты в конце (порядок может сохраняться)
        assert {op["id"] for op in result[2:]} == {2, 4}

    @pytest.mark.parametrize(
        "descending, first_date, last_date",
        [
            (True, "2024-04-01", "2023-12-31"),  # По убыванию
            (False, "2023-12-31", "2024-04-01"),  # По возрастанию
        ]
    )
    def test_parametrized_sorting(self, unsorted_operations, descending, first_date, last_date):
        """Параметризованный тест для разных направлений сортировки."""
        result = sort_by_date(unsorted_operations, descending)
        assert result[0]["date"] == first_date
        assert result[-1]["date"] == last_date
