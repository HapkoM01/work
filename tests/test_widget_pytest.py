import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    """Тесты для функции mask_account_card."""

    @pytest.fixture
    def card_examples(self):
        """Фикстура с примерами карт."""
        return [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
            ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
            ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
            ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ]

    @pytest.fixture
    def account_examples(self):
        """Фикстура с примерами счетов."""
        return [
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Счет 64686473678894779589", "Счет **9589"),
            ("Счет 35383833484447895560", "Счет **5560"),
        ]

    def test_card_masking(self, card_examples):
        """Тест маскирования карт."""
        for input_str, expected in card_examples:
            result = mask_account_card(input_str)
            assert result == expected, f"Failed for: {input_str}"

    def test_account_masking(self, account_examples):
        """Тест маскирования счетов."""
        for input_str, expected in account_examples:
            result = mask_account_card(input_str)
            assert result == expected, f"Failed for: {input_str}"

    @pytest.mark.parametrize(
        "input_str",
        [
            "Invalid String",
            "",  # Пустая строка
            "Visa",  # Только тип
            "1234567890123456",  # Только номер
        ]
    )
    def test_invalid_inputs(self, input_str: str) -> None:
        """Тест обработки некорректных входных данных."""
        with pytest.raises(ValueError):
            mask_account_card(input_str)

    def test_case_insensitive_account(self):
        """Тест нечувствительности к регистру для слова 'счет'."""
        result_lower = mask_account_card("счет 73654108430135874305")
        result_upper = mask_account_card("Счет 73654108430135874305")
        assert result_lower == "счет **4305"
        assert result_upper == "Счет **4305"


class TestGetDate:
    """Тесты для функции get_date."""

    @pytest.fixture
    def date_examples(self):
        """Фикстура с примерами дат."""
        return [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2019-07-03T18:35:29.512364", "03.07.2019"),
            ("2018-06-30T02:08:58.425572", "30.06.2018"),
            ("2023-12-31T23:59:59.999999", "31.12.2023"),
            ("2023-01-01T00:00:00.000000", "01.01.2023"),
        ]

    def test_date_formatting(self, date_examples):
        """Тест форматирования дат."""
        for input_date, expected in date_examples:
            result = get_date(input_date)
            assert result == expected, f"Failed for: {input_date}"

    @pytest.mark.parametrize(
        "date_string, expected",
        [
            ("2024-03-11", "11.03.2024"),  # Без времени
            ("2024-03-11T", "11.03.2024"),  # Пустое время
        ]
    )
    def test_partial_date_strings(self, date_string: str, expected: str) -> None:
        """Тест частичных строк с датой."""
        result = get_date(date_string)
        assert result == expected

    @pytest.mark.parametrize(
        "invalid_date",
        [
            "",  # Пустая строка
            "invalid-date",  # Неправильный формат
            "2024/03/11",  # Неправильный разделитель
            "2024-13-11T00:00:00",  # Неправильный месяц
        ]
    )
    def test_invalid_dates(self, invalid_date: str) -> None:
        """Тест обработки невалидных дат."""
        with pytest.raises((ValueError, IndexError)):
            get_date(invalid_date)

    def test_edge_cases(self):
        """Тест пограничных случаев."""
        # Високосный год
        assert get_date("2024-02-29T12:00:00") == "29.02.2024"
        # Разные часовые поясы (должны игнорироваться)
        assert get_date("2024-03-11T02:26:18+03:00") == "11.03.2024"
