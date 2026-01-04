"""
Тесты для модуля views.py
"""

import json
from datetime import datetime
from unittest.mock import mock_open, patch

import pandas as pd

from src.views import (
    get_cards_info,
    get_currency_rates,
    get_greeting,
    get_stock_prices,
    get_top_transactions,
    load_user_settings,
    main_page,
)


def test_get_greeting_morning():
    """Тест приветствия утром"""
    morning_time = datetime(2021, 12, 31, 8, 0, 0)
    assert get_greeting(morning_time) == "Доброе утро"


def test_get_greeting_afternoon():
    """Тест приветствия днем"""
    afternoon_time = datetime(2021, 12, 31, 14, 0, 0)
    assert get_greeting(afternoon_time) == "Добрый день"


def test_get_greeting_evening():
    """Тест приветствия вечером"""
    evening_time = datetime(2021, 12, 31, 20, 0, 0)
    assert get_greeting(evening_time) == "Добрый вечер"


def test_get_greeting_night():
    """Тест приветствия ночью"""
    night_time = datetime(2021, 12, 31, 2, 0, 0)
    assert get_greeting(night_time) == "Доброй ночи"


def test_get_cards_info():
    """Тест получения информации по картам"""
    # Создаем тестовый DataFrame
    data = {
        "Дата операции": [
            datetime(2021, 12, 15),
            datetime(2021, 12, 20),
            datetime(2021, 12, 25),
        ],
        "Дата платежа": ["15.12.2021", "20.12.2021", "25.12.2021"],
        "Номер карты": ["*7197", "*7197", "*5091"],
        "Статус": ["OK", "OK", "OK"],
        "Сумма операции": [-100.0, -200.0, -300.0],
        "Валюта операции": ["RUB", "RUB", "RUB"],
        "Сумма платежа": [-100.0, -200.0, -300.0],
        "Валюта платежа": ["RUB", "RUB", "RUB"],
        "Кешбэк": [None, None, None],
        "Категория": ["Супермаркеты", "Супермаркеты", "Различные товары"],
        "MCC": [5411, 5411, 5399],
        "Описание": ["Лента", "Лента", "Ozon.ru"],
        "Бонусы": [1, 2, 3],
        "Округление": [0, 0, 0],
        "Сумма с округлением": [100.0, 200.0, 300.0],
    }
    df = pd.DataFrame(data)

    start_date = datetime(2021, 12, 1)
    end_date = datetime(2021, 12, 31)

    result = get_cards_info(df, start_date, end_date)

    assert len(result) == 2
    assert any(card["last_digits"] == "7197" for card in result)
    assert any(card["last_digits"] == "5091" for card in result)


def test_get_top_transactions():
    """Тест получения топ-транзакций"""
    data = {
        "Дата операции": [
            datetime(2021, 12, 15),
            datetime(2021, 12, 20),
            datetime(2021, 12, 25),
        ],
        "Дата платежа": ["15.12.2021", "20.12.2021", "25.12.2021"],
        "Номер карты": ["*7197", "*7197", "*5091"],
        "Статус": ["OK", "OK", "OK"],
        "Сумма операции": [-500.0, -200.0, -1000.0],
        "Валюта операции": ["RUB", "RUB", "RUB"],
        "Сумма платежа": [-500.0, -200.0, -1000.0],
        "Валюта платежа": ["RUB", "RUB", "RUB"],
        "Кешбэк": [None, None, None],
        "Категория": ["Супермаркеты", "Супермаркеты", "Различные товары"],
        "MCC": [5411, 5411, 5399],
        "Описание": ["Лента", "Лента", "Ozon.ru"],
        "Бонусы": [1, 2, 3],
        "Округление": [0, 0, 0],
        "Сумма с округлением": [500.0, 200.0, 1000.0],
    }
    df = pd.DataFrame(data)

    start_date = datetime(2021, 12, 1)
    end_date = datetime(2021, 12, 31)

    result = get_top_transactions(df, start_date, end_date, 2)

    assert len(result) == 2
    assert result[0]["amount"] == -1000.0  # Самая большая по модулю
    assert result[1]["amount"] == -500.0


def test_get_currency_rates():
    """Тест получения курсов валют"""
    currencies = ["USD", "EUR"]
    result = get_currency_rates(currencies)

    assert len(result) == 2
    assert all("currency" in item for item in result)
    assert all("rate" in item for item in result)


def test_get_stock_prices():
    """Тест получения цен на акции"""
    stocks = ["AAPL", "MSFT"]
    result = get_stock_prices(stocks)

    assert len(result) == 2
    assert all("stock" in item for item in result)
    assert all("price" in item for item in result)


def test_load_user_settings():
    """Тест загрузки пользовательских настроек"""
    mock_settings = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "MSFT"]}

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_settings))):
        result = load_user_settings()

    assert "user_currencies" in result
    assert "user_stocks" in result
    assert len(result["user_currencies"]) == 2
    assert len(result["user_stocks"]) == 2


def test_load_user_settings_file_not_found():
    """Тест загрузки настроек при отсутствии файла"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_user_settings()

    assert result == {"user_currencies": [], "user_stocks": []}


@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
@patch("src.views.load_user_settings")
def test_main_page(mock_settings, mock_stocks, mock_currencies):
    """Тест главной функции страницы"""
    # Мокируем внешние зависимости
    mock_settings.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mock_currencies.return_value = [{"currency": "USD", "rate": 75.0}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}]

    # Создаем тестовый DataFrame
    data = {
        "Дата операции": [datetime(2021, 12, 15), datetime(2021, 12, 20)],
        "Дата платежа": ["15.12.2021", "20.12.2021"],
        "Номер карты": ["*7197", "*7197"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [-100.0, -200.0],
        "Валюта операции": ["RUB", "RUB"],
        "Сумма платежа": [-100.0, -200.0],
        "Валюта платежа": ["RUB", "RUB"],
        "Кешбэк": [None, None],
        "Категория": ["Супермаркеты", "Супермаркеты"],
        "MCC": [5411, 5411],
        "Описание": ["Лента", "Лента"],
        "Бонусы": [1, 2],
        "Округление": [0, 0],
        "Сумма с округлением": [100.0, 200.0],
    }
    df = pd.DataFrame(data)

    result = main_page("2021-12-31 16:00:00", df)

    # Проверяем, что результат - валидный JSON
    parsed = json.loads(result)
    assert "greeting" in parsed
    assert "cards" in parsed
    assert "top_transactions" in parsed
    assert "currency_rates" in parsed
    assert "stock_prices" in parsed


def test_main_page_invalid_date():
    """Тест главной функции с некорректной датой"""
    result = main_page("invalid-date")

    parsed = json.loads(result)
    assert "error" in parsed
