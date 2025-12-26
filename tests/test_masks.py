import unittest
from src.masks import get_mask_card_number, get_mask_account


class TestMasks(unittest.TestCase):
    """Тестовый класс для функций маскирования."""

    def test_get_mask_card_number(self):
        """Тест маскирования номера карты."""
        self.assertEqual(get_mask_card_number("780079228966361"), "7800 79** **** 6361")
        self.assertEqual(get_mask_card_number("1234567890123456"), "1234 56** **** 3456")
        self.assertEqual(get_mask_card_number("12345678901234567890"), "1234 56** **** 7890")

    def test_get_mask_card_number_with_spaces(self):
        """Тест маскирования номера карты с пробелами."""
        self.assertEqual(get_mask_card_number("7800 7922 8966 361"), "7800 79** **** 6361")

    def test_get_mask_card_number_invalid(self):
        """Тест с некорректным номером карты."""
        with self.assertRaises(ValueError):
            get_mask_card_number("123456")  # Меньше 10 цифр

    def test_get_mask_account(self):
        """Тест маскирования номера счета."""
        self.assertEqual(get_mask_account("73654188438135874305"), "**4305")
        self.assertEqual(get_mask_account("1234567890"), "**7890")

    def test_get_mask_account_with_spaces(self):
        """Тест маскирования номера счета с пробелами."""
        self.assertEqual(get_mask_account("7365 4188 4381 3587 4305"), "**4305")

    def test_get_mask_account_invalid(self):
        """Тест с некорректным номером счета."""
        with self.assertRaises(ValueError):
            get_mask_account("123")


if __name__ == "__main__":
    unittest.main()
