import logging
import os
from pathlib import Path
from unittest.mock import patch
import pandas as pd
import pytest
from src.readers import read_csv_transactions, read_excel_transactions

@pytest.fixture
def temp_csv(tmp_path: Path) -> str:
    """Создаёт временный CSV-файл для тестов."""
    file = tmp_path / "test.csv"
    file.write_text("id;state;date;amount\n1;EXECUTED;2023-01-01;1000\n", encoding="utf-8")
    return str(file)

def test_read_csv_success(temp_csv: str):
    """Тестирует успешное чтение CSV-файла."""
    result = read_csv_transactions(temp_csv)
    assert len(result) == 1
    assert result[0]["id"] == "1"

@patch("os.path.exists", return_value=False)
def test_read_csv_not_found(mock_exists):
    """Проверяет ошибку при отсутствии файла."""
    with pytest.raises(ValueError, match="CSV-файл не найден"):
        read_csv_transactions("missing.csv")

def test_read_csv_empty(tmp_path: Path):
    """Проверяет обработку пустого CSV-файла."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")
    result = read_csv_transactions(str(empty_file))
    assert result == []

@patch("os.path.exists", return_value=True)
@patch("pandas.read_excel")
def test_read_excel_success(mock_read_excel, mock_exists):
    """Тестирует успешное чтение Excel через Mock."""
    mock_df = pd.DataFrame({"id": ["1"], "amount": ["100"]})
    mock_read_excel.return_value = mock_df
    result = read_excel_transactions("test.xlsx")
    assert result[0]["id"] == "1"
