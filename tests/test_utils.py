import json
import os

from src.utils import dic_list


def test_dic_list(transactions) -> None:
    """Тестирование успешного выполнения функции"""
    file_path = "data/test_operation.json"
    try:
        with open(file_path, "w", encoding="utf-8") as file_json:
            json.dump(transactions, file_json, indent=4, ensure_ascii=False)
        assert dic_list(file_path) == transactions
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def test_dic_list_empty_list() -> None:
    """Тестирование функции, если файл содержит пустой список"""
    file_path = "data/test_operation.json"
    try:
        with open(file_path, "w", encoding="utf-8") as file_json:
            json.dump([], file_json, indent=4, ensure_ascii=False)
        assert dic_list(file_path) == []
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def test_dic_list_not_list() -> None:
    """Тестирование функции, если передается не список"""
    file_path = "data/test_operation.json"
    try:
        with open(file_path, "w", encoding="utf-8") as file_json:
            json.dump("", file_json, indent=4, ensure_ascii=False)
        assert dic_list(file_path) == []
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def test_dic_list_json_decode_error() -> None:
    """Тестирование функции, в случае ошибки JSONDecodeError"""
    file_path = "data/test_bad_data.json"
    data_to_write = '{"invalid_key" "invalid_value", "number": 123, "boolean": true'
    try:
        with open(file_path, "w", encoding="utf-8") as file_json:
            file_json.write(data_to_write)
        assert dic_list(file_path) == []
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def test_dic_list_file_not_found() -> None:
    """Тестирование функции, если файл не найден"""
    assert dic_list("not.json") == []
