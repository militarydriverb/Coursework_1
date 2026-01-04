import json
import os
from unittest.mock import patch

import pandas as pd

from src.csv_excel_data import get_csv_data_reading, get_excel_data_reading


@patch("pandas.read_csv")
def test_get_csv_data_reading(mock_get, transactions_list) -> None:
    """Тестирование успешной работы функции по чтению данных из CSV файла"""
    mock_get_return_value = transactions_list
    mock_get.return_value = pd.DataFrame(mock_get_return_value)

    file1_path = os.path.join("data", "transactions.csv")

    assert get_csv_data_reading(file1_path) == transactions_list


def test_get_csv_data_reading_not_file():
    """Тестирование работы функции в случае, если CSV файл не найден"""
    file1_path = os.path.join("data", "transactions1.csv")
    assert get_csv_data_reading(file1_path) == []


@patch("pandas.read_excel")
def test_get_excel_data_reading(mock_get, transactions_list) -> None:
    """Тестирование успешной работы функции по чтению данных из Excel файла"""
    mock_get.return_value = pd.DataFrame(transactions_list)
    expected_output = json.dumps(transactions_list, ensure_ascii=False, indent=4)

    file2_path = os.path.join("data", "transactions_excel.xlsx")

    assert get_excel_data_reading(file2_path) == expected_output


def test_get_excel_data_reading_not_file():
    """Тестирование работы функции в случае, если Excel файл не найден"""
    file1_path = os.path.join("data", "transactions_excel1.xlsx")
    assert get_excel_data_reading(file1_path) == ""
