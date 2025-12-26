import unittest

from src.masks import get_mask_account, get_mask_card_number


class TestMasks(unittest.TestCase):
    """Тестовый класс для функций маскирования."""

    def test_get_mask_card_number_standard(self):
        """Тест маскирования стандартного номера карты."""
        self.assertEqual(get_mask_card_number("780079228966361"), "7800 79** **** 6361")

    def test_get_mask_card_number_16_digits(self):
        """Тест маскирования 16-значного номера карты."""
        self.assertEqual(get_mask_card_number("1234567890123456"), "1234 56** **** 3456")

    def test_get_mask_card_number_20_digits(self):
        """Тест маскирования длинного номера карты."""
        self.assertEqual(get_mask_card_number("12345678901234567890"), "1234 56** **** 7890")

    def test_get_mask_card_number_with_spaces(self):
        """Тест маскирования номера карты с пробелами."""
        self.assertEqual(get_mask_card_number("7800 7922 8966 361"), "7800 79** **** 6361")

    def test_get_mask_card_number_with_dashes(self):
        """Тест маскирования номера карты с дефисами."""
        self.assertEqual(get_mask_card_number("7800-7922-8966-361"), "7800 79** **** 6361")

    def test_get_mask_card_number_minimum_length(self):
        """Тест маскирования минимально допустимого номера карты."""
        self.assertEqual(get_mask_card_number("1234567890"), "1234 56** **** 7890")

    def test_get_mask_card_number_invalid_short(self):
        """Тест с слишком коротким номером карты."""
        with self.assertRaises(ValueError):
            get_mask_card_number("123456789")  # 9 цифр < 10

    def test_get_mask_card_number_invalid_empty(self):
        """Тест с пустым номером карты."""
        with self.assertRaises(ValueError):
            get_mask_card_number("")

    def test_get_mask_card_number_invalid_no_digits(self):
        """Тест с номером без цифр."""
        with self.assertRaises(ValueError):
            get_mask_card_number("abcdefghij")

    def test_get_mask_card_number_mixed_characters(self):
        """Тест с номером содержащим буквы и цифры."""
        self.assertEqual(get_mask_card_number("7800abc7922xyz8966361"), "7800 79** **** 6361")

    def test_get_mask_account_standard(self):
        """Тест маскирования стандартного номера счета."""
        self.assertEqual(get_mask_account("73654188438135874305"), "**4305")

    def test_get_mask_account_short(self):
        """Тест маскирования короткого номера счета."""
        self.assertEqual(get_mask_account("1234567890"), "**7890")

    def test_get_mask_account_exactly_4_digits(self):
        """Тест маскирования счета ровно из 4 цифр."""
        self.assertEqual(get_mask_account("1234"), "**1234")

    def test_get_mask_account_with_spaces(self):
        """Тест маскирования номера счета с пробелами."""
        self.assertEqual(get_mask_account("7365 4188 4381 3587 4305"), "**4305")

    def test_get_mask_account_with_dashes(self):
        """Тест маскирования номера счета с дефисами."""
        self.assertEqual(get_mask_account("7365-4188-4381-3587-4305"), "**4305")

    def test_get_mask_account_invalid_short(self):
        """Тест с слишком коротким номером счета."""
        with self.assertRaises(ValueError):
            get_mask_account("123")  # 3 цифры < 4

    def test_get_mask_account_invalid_empty(self):
        """Тест с пустым номером счета."""
        with self.assertRaises(ValueError):
            get_mask_account("")

    def test_get_mask_account_invalid_no_digits(self):
        """Тест с номером без цифр."""
        with self.assertRaises(ValueError):
            get_mask_account("abcd")

    def test_get_mask_account_mixed_characters(self):
        """Тест с номером содержащим буквы и цифры."""
        self.assertEqual(get_mask_account("7365abc4188xyz4381def3587gh4305"), "**4305")

    def test_edge_cases(self):
        """Тест пограничных случаев."""
        # Карта с максимально допустимым минимальным размером
        self.assertEqual(get_mask_card_number("1234567890"), "1234 56** **** 7890")

        # Счет с минимальным размером
        self.assertEqual(get_mask_account("1234"), "**1234")

        # Очень длинный номер счета
        self.assertEqual(get_mask_account("1234567890123456789012345678901234567890"), "**7890")


if __name__ == "__main__":
    unittest.main()
