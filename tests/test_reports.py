"""
Тесты для модуля reports.py
"""

import os
from pathlib import Path

import pandas as pd
import pytest

from src.reports import (
    report_to_file,
)


@pytest.fixture
def sample_dataframe():
    """Фикстура с примером DataFrame транзакций"""
    data = {
        "Дата операции": [
            "31.12.2021 10:00:00",
            "30.12.2021 14:00:00",
            "29.12.2021 18:00:00",
            "28.12.2021 12:00:00",
            "27.12.2021 15:00:00",
            "15.11.2021 10:00:00",
            "10.10.2021 16:00:00",
            "05.09.2021 11:00:00",
        ],
        "Дата платежа": [
            "31.12.2021",
            "30.12.2021",
            "29.12.2021",
            "28.12.2021",
            "27.12.2021",
            "15.11.2021",
            "10.10.2021",
            "05.09.2021",
        ],
        "Номер карты": ["*7197"] * 8,
        "Статус": ["OK"] * 8,
        "Сумма операции": [
            -500.0,
            -300.0,
            -1200.0,
            -100.0,
            -200.0,
            -600.0,
            -400.0,
            -800.0,
        ],
        "Валюта операции": ["RUB"] * 8,
        "Сумма платежа": [
            -500.0,
            -300.0,
            -1200.0,
            -100.0,
            -200.0,
            -600.0,
            -400.0,
            -800.0,
        ],
        "Валюта платежа": ["RUB"] * 8,
        "Кэшбэк": [None] * 8,
        "Категория": [
            "Супермаркеты",
            "Супермаркеты",
            "Различные товары",
            "Транспорт",
            "Супермаркеты",
            "Супермаркеты",
            "Супермаркеты",
            "Различные товары",
        ],
        "MCC": [5411] * 8,
        "Описание": [
            "Лента",
            "Перекресток",
            "Ozon.ru",
            "Метро",
            "Магнит",
            "Лента",
            "Дикси",
            "Wildberries",
        ],
        "Бонусы": [1, 2, 3, 1, 2, 1, 2, 3],
        "Округление": [0] * 8,
        "Сумма с округлением": [
            500.0,
            300.0,
            1200.0,
            100.0,
            200.0,
            600.0,
            400.0,
            800.0,
        ],
    }
    return pd.DataFrame(data)


def test_spending_by_category_with_data(sample_dataframe):
    """Тест отчета по категории с данными"""
    # Удаляем декоратор для тестирования
    from src.reports import spending_by_category as original_func

    # Получаем оригинальную функцию без декоратора
    if hasattr(original_func, "__wrapped__"):
        func = original_func.__wrapped__
    else:
        # Если декоратор не применен, используем саму функцию
        func = original_func

    result = func(sample_dataframe, "Супермаркеты", "31.12.2021")

    # Проверяем структуру результата
    assert isinstance(result, pd.DataFrame)
    assert "Месяц" in result.columns
    assert "Общая сумма" in result.columns
    assert "Количество операций" in result.columns

    # Должны быть данные за 3 месяца (октябрь, ноябрь, декабрь)
    assert len(result) >= 1


def test_spending_by_category_no_data(sample_dataframe):
    """Тест отчета по категории без данных"""
    from src.reports import spending_by_category as original_func

    if hasattr(original_func, "__wrapped__"):
        func = original_func.__wrapped__
    else:
        func = original_func

    result = func(sample_dataframe, "Несуществующая категория", "31.12.2021")

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0


def test_spending_by_category_default_date(sample_dataframe):
    """Тест отчета по категории с датой по умолчанию"""
    from src.reports import spending_by_category as original_func

    if hasattr(original_func, "__wrapped__"):
        func = original_func.__wrapped__
    else:
        func = original_func

    result = func(sample_dataframe, "Супермаркеты")

    assert isinstance(result, pd.DataFrame)


def test_spending_by_weekday_with_data(sample_dataframe):
    """Тест отчета по дням недели с данными"""
    from src.reports import spending_by_weekday as original_func

    if hasattr(original_func, "__wrapped__"):
        func = original_func.__wrapped__
    else:
        func = original_func

    result = func(sample_dataframe, "31.12.2021")

    assert isinstance(result, pd.DataFrame)
    assert "День недели" in result.columns
    assert "Средняя сумма" in result.columns
    assert "Количество операций" in result.columns

    # Должны быть данные хотя бы за некоторые дни недели
    assert len(result) >= 1


def test_spending_by_weekday_default_date(sample_dataframe):
    """Тест отчета по дням недели с датой по умолчанию"""
    from src.reports import spending_by_weekday as original_func

    if hasattr(original_func, "__wrapped__"):
        func = original_func.__wrapped__
    else:
        func = original_func

    result = func(sample_dataframe)

    assert isinstance(result, pd.DataFrame)


def test_spending_by_workday_with_data(sample_dataframe):
    """Тест отчета по рабочим/выходным дням с данными"""
    from src.reports import spending_by_workday as original_func

    if hasattr(original_func, "__wrapped__"):
        func = original_func.__wrapped__
    else:
        func = original_func

    result = func(sample_dataframe, "31.12.2021")

    assert isinstance(result, pd.DataFrame)
    assert "Тип дня" in result.columns
    assert "Средняя сумма" in result.columns
    assert "Количество операций" in result.columns

    # Должны быть данные за рабочие и/или выходные дни
    assert len(result) >= 1


def test_spending_by_workday_default_date(sample_dataframe):
    """Тест отчета по рабочим/выходным дням с датой по умолчанию"""
    from src.reports import spending_by_workday as original_func

    if hasattr(original_func, "__wrapped__"):
        func = original_func.__wrapped__
    else:
        func = original_func

    result = func(sample_dataframe)

    assert isinstance(result, pd.DataFrame)


def test_report_to_file_decorator_default_filename(sample_dataframe, tmp_path):
    """Тест декоратора с именем файла по умолчанию"""
    # Меняем директорию для отчетов на временную
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:

        @report_to_file()
        def test_func():
            return pd.DataFrame({"A": [1, 2, 3]})

        result = test_func()

        # Проверяем, что результат вернулся
        assert isinstance(result, pd.DataFrame)

        # Проверяем, что файл создан
        reports_dir = Path(tmp_path) / "reports"
        assert reports_dir.exists()

        files = list(reports_dir.glob("report_test_func_*.txt"))
        assert len(files) > 0

    finally:
        os.chdir(original_cwd)


def test_report_to_file_decorator_custom_filename(sample_dataframe, tmp_path):
    """Тест декоратора с пользовательским именем файла"""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:

        @report_to_file(filename="custom_report.txt")
        def test_func():
            return pd.DataFrame({"A": [1, 2, 3]})

        result = test_func()

        # Проверяем, что результат вернулся
        assert isinstance(result, pd.DataFrame)

        # Проверяем, что файл создан с нужным именем
        reports_dir = Path(tmp_path) / "reports"
        custom_file = reports_dir / "custom_report.txt"
        assert custom_file.exists()

    finally:
        os.chdir(original_cwd)


def test_report_to_file_decorator_with_dict(tmp_path):
    """Тест декоратора со словарем"""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:

        @report_to_file(filename="dict_report.txt")
        def test_func():
            return {"key": "value", "number": 123}

        result = test_func()

        # Проверяем, что результат вернулся
        assert isinstance(result, dict)

        # Проверяем, что файл создан
        reports_dir = Path(tmp_path) / "reports"
        report_file = reports_dir / "dict_report.txt"
        assert report_file.exists()

        # Проверяем содержимое файла
        content = report_file.read_text(encoding="utf-8")
        assert "key" in content
        assert "value" in content

    finally:
        os.chdir(original_cwd)


def test_report_to_file_decorator_with_string(tmp_path):
    """Тест декоратора со строкой"""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:

        @report_to_file(filename="string_report.txt")
        def test_func():
            return "Test report content"

        result = test_func()

        # Проверяем, что результат вернулся
        assert result == "Test report content"

        # Проверяем, что файл создан
        reports_dir = Path(tmp_path) / "reports"
        report_file = reports_dir / "string_report.txt"
        assert report_file.exists()

        # Проверяем содержимое файла
        content = report_file.read_text(encoding="utf-8")
        assert content == "Test report content"

    finally:
        os.chdir(original_cwd)


def test_empty_dataframe():
    """Тест с пустым DataFrame"""
    from src.reports import spending_by_category as original_func

    if hasattr(original_func, "__wrapped__"):
        func = original_func.__wrapped__
    else:
        func = original_func

    empty_df = pd.DataFrame()
    result = func(empty_df, "Супермаркеты", "31.12.2021")

    assert isinstance(result, pd.DataFrame)
