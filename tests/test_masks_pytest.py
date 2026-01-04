import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number."""

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("780079228966361", "7800 79** **** 6361"),
            ("1234567890123456", "1234 56** **** 3456"),
            ("1111222233334444", "1111 22** **** 4444"),
            ("1234567890", "1234 56** **** 7890"),  # Минимальная длина
        ]
    )
    def test_valid_card_numbers(self, card_number: str, expected: str) -> None:
        """Тест правильности маскирования валидных номеров карт."""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("7800 7922 8966 361", "7800 79** **** 6361"),
            ("1234-5678-9012-3456", "1234 56** **** 3456"),
            ("1111 2222 3333 4444", "1111 22** **** 4444"),
        ]
    )
    def test_card_numbers_with_separators(self, card_number: str, expected: str) -> None:
        """Тест номеров карт с разделителями."""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "",  # Пустая строка
            "123",  # Слишком короткий
            "abcdefghij",  # Нет цифр
            "123456789",  # 9 цифр (<10)
        ]
    )
    def test_invalid_card_numbers(self, invalid_input: str) -> None:
        """Тест обработки невалидных номеров карт."""
        with pytest.raises(ValueError):
            get_mask_card_number(invalid_input)

    def test_long_card_number(self) -> None:
        """Тест длинного номера карты."""
        card_number = "123456789012345678901234567890"
        result = get_mask_card_number(card_number)
        assert result.endswith("7890")
        assert "1234 56** ****" in result


class TestGetMaskAccount:
    """Тесты для функции get_mask_account."""

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("73654188438135874305", "**4305"),
            ("1234567890", "**7890"),
            ("11112222333344445555", "**5555"),
            ("1234", "**1234"),  # Минимальная длина
        ]
    )
    def test_valid_account_numbers(self, account_number: str, expected: str) -> None:
        """Тест правильности маскирования валидных номеров счетов."""
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("7365 4188 4381 3587 4305", "**4305"),
            ("1234-5678-90", "**7890"),
            ("1111 2222 3333 4444 5555", "**5555"),
        ]
    )
    def test_account_numbers_with_separators(self, account_number: str, expected: str) -> None:
        """Тест номеров счетов с разделителями."""
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "",  # Пустая строка
            "123",  # Слишком короткий
            "abc",  # Нет цифр
            "abc123",  # Слишком короткий после очистки
        ]
    )
    def test_invalid_account_numbers(self, invalid_input: str) -> None:
        """Тест обработки невалидных номеров счетов."""
        with pytest.raises(ValueError):
            get_mask_account(invalid_input)

    def test_mixed_characters(self) -> None:
        """Тест номера счета со смешанными символами."""
        account_number = "Acc1234567890End"
        result = get_mask_account(account_number)
        assert result == "**7890"
