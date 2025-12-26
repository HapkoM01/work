import unittest
from src.widget import mask_account_card, get_date


class TestWidget(unittest.TestCase):
    """Тестовый класс для функций виджета."""

    def test_mask_account_card_visa(self):
        """Тест маскирования карты Visa."""
        result = mask_account_card("Visa Platinum 7000792289606361")
        self.assertEqual(result, "Visa Platinum 7000 79** **** 6361")

    def test_mask_account_card_maestro(self):
        """Тест маскирования карты Maestro."""
        result = mask_account_card("Maestro 1596837868705199")
        self.assertEqual(result, "Maestro 1596 83** **** 5199")

    def test_mask_account_card_account(self):
        """Тест маскирования счета."""
        result = mask_account_card("Счет 64686473678894779589")
        self.assertEqual(result, "Счет **9589")

    def test_mask_account_card_multiple_words(self):
        """Тест с названием из нескольких слов."""
        result = mask_account_card("Visa Classic 6831982476737658")
        self.assertEqual(result, "Visa Classic 6831 98** **** 7658")

    def test_mask_account_card_invalid_input(self):
        """Тест с некорректным вводом."""
        with self.assertRaises(ValueError):
            mask_account_card("ТолькоНазвание")

    def test_get_date(self):
        """Тест форматирования даты."""
        result = get_date("2024-03-11T02:26:18.671407")
        self.assertEqual(result, "11.03.2024")

    def test_get_date_without_time(self):
        """Тест с датой без времени."""
        result = get_date("2024-12-31")
        self.assertEqual(result, "31.12.2024")

    def test_get_date_invalid_format(self):
        """Тест с некорректным форматом даты."""
        with self.assertRaises(ValueError):
            get_date("неправильная дата")


if __name__ == "__main__":
    unittest.main()
