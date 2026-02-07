import logging

import pytest

from src.masks import get_mask_card_number
from src.utils import get_financial_transactions


def test_masks_success_logging(caplog):
    caplog.set_level(logging.INFO, logger="masks")

    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"

    # Проверяем наличие INFO-сообщения
    assert "Успешно замаскирован номер карты" in caplog.text
    assert "masks" in caplog.text  # имя логгера

    # Можно проверять конкретные записи
    assert any(r.levelno == logging.INFO and "замаскирован номер карты" in r.message for r in caplog.records)


def test_masks_error_logging(caplog):
    caplog.set_level(logging.DEBUG, logger="masks")

    with pytest.raises(ValueError):
        get_mask_card_number("123")  # слишком короткий

    assert "Слишком короткий номер карты" in caplog.text
    assert any(r.levelno == logging.ERROR and "короткий номер карты" in r.message for r in caplog.records)


def test_utils_file_not_found_logging(caplog, tmp_path):
    caplog.set_level(logging.DEBUG, logger="utils")

    fake_path = tmp_path / "nonexistent.json"
    result = get_financial_transactions(str(fake_path))

    assert result == []
    assert "Файл не найден" in caplog.text
    assert "WARNING" in caplog.text  # или проверяйте уровень


def test_utils_success_read_logging(caplog, tmp_path):
    caplog.set_level(logging.INFO, logger="utils")

    # Создаём временный файл
    data_file = tmp_path / "ops.json"
    data_file.write_text('[{"id":1,"amount":100}]', encoding="utf-8")

    result = get_financial_transactions(str(data_file))

    assert len(result) == 1
    assert "Успешно прочитано 1 операций" in caplog.text

    def test_get_mask_card_number_success_logging(caplog):
        caplog.set_level(logging.INFO, logger="masks")

        result = get_mask_card_number("4444555566667777")
        assert result == "4444 55** **** 7777"

        assert "Успешно замаскирован номер карты" in caplog.text

    def test_get_mask_card_number_error_logging(caplog):
        caplog.set_level(logging.ERROR, logger="masks")

        with pytest.raises(ValueError):
            get_mask_card_number("12345")

        assert "Слишком короткий номер карты" in caplog.text
        assert any(r.levelno == logging.ERROR for r in caplog.records)
