"""
Тесты для модуля services.py
"""

import json

import pytest

from src.services import (
    cashback_categories_analysis,
    investment_bank,
    search_by_phone_numbers,
    search_transfers_to_individuals,
    simple_search,
)


@pytest.fixture
def sample_transactions():
    """Фикстура с примерами транзакций"""
    return [
        {
            "Дата операции": "15.12.2021 10:00:00",
            "Категория": "Супермаркеты",
            "Описание": "Лента",
            "Сумма операции": -500.0,
        },
        {
            "Дата операции": "20.12.2021 14:00:00",
            "Категория": "Различные товары",
            "Описание": "Ozon.ru",
            "Сумма операции": -1200.0,
        },
        {
            "Дата операции": "25.12.2021 18:00:00",
            "Категория": "Супермаркеты",
            "Описание": "Перекресток",
            "Сумма операции": -300.0,
        },
        {
            "Дата операции": "28.12.2021 12:00:00",
            "Категория": "Переводы",
            "Описание": "МТС +7 921 123-45-67",
            "Сумма операции": -100.0,
        },
        {
            "Дата операции": "29.12.2021 15:00:00",
            "Категория": "Переводы",
            "Описание": "Перевод Сергей А.",
            "Сумма операции": -5000.0,
        },
    ]


def test_simple_search_found(sample_transactions):
    """Тест простого поиска с найденными результатами"""
    result = simple_search(sample_transactions, "Лента")
    parsed = json.loads(result)

    assert len(parsed) == 1
    assert parsed[0]["Описание"] == "Лента"


def test_simple_search_multiple_results(sample_transactions):
    """Тест простого поиска с несколькими результатами"""
    result = simple_search(sample_transactions, "Супермаркеты")
    parsed = json.loads(result)

    assert len(parsed) == 2


def test_simple_search_case_insensitive(sample_transactions):
    """Тест поиска без учета регистра"""
    result = simple_search(sample_transactions, "лента")
    parsed = json.loads(result)

    assert len(parsed) == 1


def test_simple_search_not_found(sample_transactions):
    """Тест поиска с отсутствием результатов"""
    result = simple_search(sample_transactions, "Несуществующее")
    parsed = json.loads(result)

    assert len(parsed) == 0


def test_simple_search_empty_string(sample_transactions):
    """Тест поиска с пустой строкой"""
    result = simple_search(sample_transactions, "")
    parsed = json.loads(result)

    assert len(parsed) == 0


def test_search_by_phone_numbers(sample_transactions):
    """Тест поиска транзакций с телефонными номерами"""
    result = search_by_phone_numbers(sample_transactions)
    parsed = json.loads(result)

    assert len(parsed) == 1
    assert "+7 921 123-45-67" in parsed[0]["Описание"]


def test_search_by_phone_numbers_no_results():
    """Тест поиска телефонных номеров без результатов"""
    transactions = [
        {
            "Дата операции": "15.12.2021",
            "Категория": "Супермаркеты",
            "Описание": "Лента",
            "Сумма операции": -500.0,
        }
    ]
    result = search_by_phone_numbers(transactions)
    parsed = json.loads(result)

    assert len(parsed) == 0


def test_search_transfers_to_individuals(sample_transactions):
    """Тест поиска переводов физическим лицам"""
    result = search_transfers_to_individuals(sample_transactions)
    parsed = json.loads(result)

    assert len(parsed) == 1
    assert "Сергей А." in parsed[0]["Описание"]


def test_search_transfers_to_individuals_no_results():
    """Тест поиска переводов физлицам без результатов"""
    transactions = [
        {
            "Дата операции": "15.12.2021",
            "Категория": "Супермаркеты",
            "Описание": "Лента",
            "Сумма операции": -500.0,
        },
        {
            "Дата операции": "20.12.2021",
            "Категория": "Переводы",
            "Описание": "Перевод организации",
            "Сумма операции": -1000.0,
        },
    ]
    result = search_transfers_to_individuals(transactions)
    parsed = json.loads(result)

    assert len(parsed) == 0


def test_investment_bank_calculation():
    """Тест расчета инвесткопилки"""
    transactions = [
        {
            "Дата операции": "15.12.2021 10:00:00",
            "Сумма операции": -112.50,  # Округление до 150 (50) = 37.50
        },
        {
            "Дата операции": "20.12.2021 14:00:00",
            "Сумма операции": -1234.00,  # Округление до 1250 (50) = 16.00
        },
        {
            "Дата операции": "25.01.2022 18:00:00",  # Другой месяц - не учитывается
            "Сумма операции": -500.0,
        },
    ]

    result = investment_bank("2021-12", transactions, 50)

    # 37.50 + 16.00 = 53.50
    assert result == 53.50


def test_investment_bank_limit_10():
    """Тест расчета инвесткопилки с лимитом 10"""
    transactions = [
        {
            "Дата операции": "15.12.2021 10:00:00",
            "Сумма операции": -112.50,  # Округление до 120 = 7.50
        }
    ]

    result = investment_bank("2021-12", transactions, 10)

    assert result == 7.50


def test_investment_bank_limit_100():
    """Тест расчета инвесткопилки с лимитом 100"""
    transactions = [
        {
            "Дата операции": "15.12.2021 10:00:00",
            "Сумма операции": -112.50,  # Округление до 200 = 87.50
        }
    ]

    result = investment_bank("2021-12", transactions, 100)

    assert result == 87.50


def test_investment_bank_no_transactions():
    """Тест расчета инвесткопилки без транзакций"""
    result = investment_bank("2021-12", [], 50)

    assert result == 0.0


def test_investment_bank_only_income():
    """Тест расчета инвесткопилки только с доходами"""
    transactions = [
        {
            "Дата операции": "15.12.2021 10:00:00",
            "Сумма операции": 1000.0,  # Положительная сумма - доход
        }
    ]

    result = investment_bank("2021-12", transactions, 50)

    assert result == 0.0


def test_cashback_categories_analysis():
    """Тест анализа выгодных категорий кешбэка"""
    transactions = [
        {
            "Дата операции": "15.12.2021 10:00:00",
            "Категория": "Супермаркеты",
            "Сумма операции": -10000.0,  # Кешбэк 400
        },
        {
            "Дата операции": "20.12.2021 14:00:00",
            "Категория": "Различные товары",
            "Сумма операции": -5000.0,  # Кешбэк 200
        },
        {
            "Дата операции": "25.12.2021 18:00:00",
            "Категория": "Супермаркеты",
            "Сумма операции": -5000.0,  # Кешбэк 200
        },
        {
            "Дата операции": "25.01.2022 18:00:00",  # Другой месяц
            "Категория": "Транспорт",
            "Сумма операции": -20000.0,
        },
    ]

    result = cashback_categories_analysis(transactions, 2021, 12)
    parsed = json.loads(result)

    # Супермаркеты: 15000 * 0.04 = 600
    # Различные товары: 5000 * 0.04 = 200
    assert "Супермаркеты" in parsed
    assert parsed["Супермаркеты"] == 600.0
    assert "Различные товары" in parsed
    assert parsed["Различные товары"] == 200.0
    assert "Транспорт" not in parsed  # Другой месяц


def test_cashback_categories_analysis_no_data():
    """Тест анализа кешбэка без данных"""
    result = cashback_categories_analysis([], 2021, 12)
    parsed = json.loads(result)

    assert len(parsed) == 0


def test_cashback_categories_analysis_only_income():
    """Тест анализа кешбэка только с доходами"""
    transactions = [
        {
            "Дата операции": "15.12.2021 10:00:00",
            "Категория": "Пополнение",
            "Сумма операции": 50000.0,
        }
    ]

    result = cashback_categories_analysis(transactions, 2021, 12)
    parsed = json.loads(result)

    assert len(parsed) == 0
