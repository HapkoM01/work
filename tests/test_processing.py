import unittest

from src.processing import filter_by_state, sort_by_date


class TestProcessing(unittest.TestCase):
    """Тестовый класс для функций обработки операций."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.operations = [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]

    def test_filter_by_state_default(self):
        """Тест фильтрации со статусом по умолчанию (EXECUTED)."""
        result = filter_by_state(self.operations)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(op["state"] == "EXECUTED" for op in result))

    def test_filter_by_state_executed(self):
        """Тест фильтрации по статусу EXECUTED."""
        result = filter_by_state(self.operations, "EXECUTED")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(op["state"] == "EXECUTED" for op in result))
        self.assertEqual([op["id"] for op in result], [41428829, 939719570])

    def test_filter_by_state_canceled(self):
        """Тест фильтрации по статусу CANCELED."""
        result = filter_by_state(self.operations, "CANCELED")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(op["state"] == "CANCELED" for op in result))
        self.assertEqual([op["id"] for op in result], [594226727, 615064591])

    def test_filter_by_state_invalid_state(self):
        """Тест фильтрации по несуществующему статусу."""
        result = filter_by_state(self.operations, "INVALID")
        self.assertEqual(len(result), 0)

    def test_filter_by_state_empty_list(self):
        """Тест фильтрации пустого списка."""
        result = filter_by_state([])
        self.assertEqual(result, [])

    def test_filter_by_state_operations_without_state(self):
        """Тест фильтрации операций без ключа state."""
        ops = [{"id": 1}, {"id": 2, "state": "EXECUTED"}]
        result = filter_by_state(ops, "EXECUTED")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 2)

    def test_sort_by_date_descending_default(self):
        """Тест сортировки по убыванию (по умолчанию)."""
        result = sort_by_date(self.operations)
        dates = [op["date"] for op in result]
        self.assertEqual(
            dates,
            [
                "2019-07-03T18:35:29.512364",
                "2018-10-14T08:21:33.419441",
                "2018-09-12T21:27:25.241689",
                "2018-06-30T02:08:58.425572",
            ],
        )

    def test_sort_by_date_descending_true(self):
        """Тест сортировки по убыванию (descending=True)."""
        result = sort_by_date(self.operations, True)
        dates = [op["date"] for op in result]
        self.assertEqual(dates[0], "2019-07-03T18:35:29.512364")
        self.assertEqual(dates[-1], "2018-06-30T02:08:58.425572")

    def test_sort_by_date_ascending_false(self):
        """Тест сортировки по возрастанию (descending=False)."""
        result = sort_by_date(self.operations, False)
        dates = [op["date"] for op in result]
        self.assertEqual(dates[0], "2018-06-30T02:08:58.425572")
        self.assertEqual(dates[-1], "2019-07-03T18:35:29.512364")

    def test_sort_by_date_empty_list(self):
        """Тест сортировки пустого списка."""
        result = sort_by_date([])
        self.assertEqual(result, [])

    def test_sort_by_date_operations_without_date(self):
        """Тест сортировки операций без ключа date."""
        ops = [
            {"id": 1, "date": "2023-02-01"},
            {"id": 2},  # Без даты
            {"id": 3, "date": "2023-01-01"},
        ]
        result = sort_by_date(ops)
        # Операции без даты должны быть в конце
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[1]["id"], 3)
        self.assertEqual(result[2]["id"], 2)

    def test_sort_by_date_single_operation(self):
        """Тест сортировки одного элемента."""
        ops = [{"id": 1, "date": "2023-01-01"}]
        result = sort_by_date(ops)
        self.assertEqual(result, ops)

    def test_sort_by_date_equal_dates(self):
        """Тест сортировки с одинаковыми датами."""
        ops = [
            {"id": 1, "date": "2023-01-01"},
            {"id": 2, "date": "2023-01-01"},
            {"id": 3, "date": "2023-01-01"},
        ]
        result = sort_by_date(ops)
        # Порядок должен сохраниться при одинаковых датах
        self.assertEqual([op["id"] for op in result], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
