import logging
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from src.readers import read_csv_transactions, read_excel_transactions


@pytest.fixture
def temp_csv(tmp_path: Path):
    file = tmp_path / "test.csv"
    file.write_text("id;state;date;amount\n1;EXECUTED;2023-01-01;1000\n", encoding="utf-8")
    return str(file)


@patch("os.path.exists", return_value=False)
def test_read_csv_not_found(mock_exists):
    with pytest.raises(ValueError, match="CSV-файл не найден"):
        read_csv_transactions("fake.csv")


def test_read_csv_success(temp_csv, caplog):
    caplog.set_level(logging.INFO, logger="readers")
    result = read_csv_transactions(temp_csv)
    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert "Успешно прочитано 1 транзакций" in caplog.text


@patch("pandas.read_csv", side_effect=pd.errors.ParserError("bad format"))
@patch("os.path.exists", return_value=True)
def test_read_csv_parse_error(mock_exists, mock_read):
    with pytest.raises(ValueError, match="Невозможно разобрать CSV"):
        read_csv_transactions("bad.csv")
