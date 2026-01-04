import json

import pandas as pd


def get_csv_data_reading(file_path: str) -> list[dict]:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу (разделитель ";")

    Returns:
        list[dict]: Список словарей с транзакциями или пустой список при ошибке

    Example:
        >>> get_csv_data_reading("data/transactions.csv")
        [{"id": 1, "amount": 100, ...}, ...]
    """
    try:
        df = pd.read_csv(file_path, delimiter=";")
        return df.to_dict("records")
    except FileNotFoundError:
        return []

def get_excel_data_reading(file_path1: str) -> str:
    """
    Считывает финансовые операции из Excel-файла.

    Args:
        file_path1: Путь к Excel-файлу (.xlsx)

    Returns:
        str: JSON-строка с транзакциями или пустая строка при ошибке

    Example:
        >>> get_excel_data_reading("data/operations.xlsx")
        '[{\"id\": 1, \"amount\": 100, ...}, ...]'
    """
    try:
        df = pd.read_excel(file_path1, engine="openpyxl")
        transaction = df.to_dict("records")
        return json.dumps(transaction, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        return ""
    except Exception:
        return ""
