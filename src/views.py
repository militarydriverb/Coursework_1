"""
Модуль для генерации JSON-ответов для веб-страниц.
Содержит функции для формирования данных страницы "Главная" и других страниц.
"""

import json
import logging
from datetime import datetime
from typing import Any, Optional

import pandas as pd
import requests

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/views.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_greeting(current_time: datetime) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    Args:
        current_time: Текущее время

    Returns:
        Строка с приветствием
    """
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_info(
    transactions: pd.DataFrame, start_date: datetime, end_date: datetime
) -> list[dict[str, Any]]:
    """
    Получает информацию по каждой карте: последние 4 цифры, сумма расходов и кешбэк.

    Args:
        transactions: DataFrame с транзакциями
        start_date: Начальная дата периода
        end_date: Конечная дата периода

    Returns:
        Список словарей с информацией по картам
    """
    try:
        # Фильтруем транзакции по дате
        mask = (transactions.iloc[:, 0] >= start_date) & (
            transactions.iloc[:, 0] <= end_date
        )
        filtered = transactions[mask]

        # Группируем по номеру карты
        cards_data = []
        card_numbers = filtered.iloc[:, 2].unique()

        for card in card_numbers:
            if pd.isna(card) or card == "" or not isinstance(card, str):
                continue

            # Получаем транзакции по карте (отрицательные суммы - расходы)
            card_transactions = filtered[filtered.iloc[:, 2] == card]
            expenses = (
                card_transactions[card_transactions.iloc[:, 4] < 0].iloc[:, 4].sum()
            )
            total_spent = abs(expenses)
            cashback = total_spent / 100

            # Извлекаем последние 4 цифры карты
            last_digits = card.replace("*", "")

            cards_data.append(
                {
                    "last_digits": last_digits,
                    "total_spent": round(total_spent, 2),
                    "cashback": round(cashback, 2),
                }
            )

        logger.info(f"Получена информация по {len(cards_data)} картам")
        return cards_data
    except Exception as e:
        logger.error(f"Ошибка при получении информации по картам: {e}")
        return []


def get_top_transactions(
    transactions: pd.DataFrame, start_date: datetime, end_date: datetime, top_n: int = 5
) -> list[dict[str, Any]]:
    """
    Получает топ-N транзакций по сумме платежа.

    Args:
        transactions: DataFrame с транзакциями
        start_date: Начальная дата периода
        end_date: Конечная дата периода
        top_n: Количество транзакций в топе

    Returns:
        Список словарей с топ-транзакциями
    """
    try:
        # Фильтруем транзакции по дате
        mask = (transactions.iloc[:, 0] >= start_date) & (
            transactions.iloc[:, 0] <= end_date
        )
        filtered = transactions[mask].copy()

        # Сортируем по абсолютной сумме операции
        filtered["abs_amount"] = filtered.iloc[:, 4].abs()
        top = filtered.nlargest(top_n, "abs_amount")

        top_list = []
        for _, row in top.iterrows():
            # Дата операции (колонка 0) - используем дату платежа (колонка 1)
            date_val = row.iloc[1]
            if isinstance(date_val, str):
                date_str = date_val.split()[0]
            else:
                date_str = date_val.strftime("%d.%m.%Y")

            top_list.append(
                {
                    "date": date_str,
                    "amount": float(row.iloc[4]),
                    "category": str(row.iloc[9])
                    if pd.notna(row.iloc[9])
                    else "Без категории",
                    "description": str(row.iloc[11])
                    if pd.notna(row.iloc[11])
                    else "Без описания",
                }
            )

        logger.info(f"Получен топ-{top_n} транзакций")
        return top_list
    except Exception as e:
        logger.error(f"Ошибка при получении топ-транзакций: {e}")
        return []


def get_currency_rates(currencies: list[str]) -> list[dict[str, Any]]:
    """
    Получает курсы валют через API.

    Args:
        currencies: Список кодов валют

    Returns:
        Список словарей с курсами валют
    """
    try:
        # Используем бесплатный API для получения курсов валют
        # В реальном проекте нужно использовать API-ключ и платный сервис
        rates_list = []

        # Попробуем использовать ЦБ РФ API
        try:
            response = requests.get(
                "https://www.cbr-xml-daily.ru/daily_json.js", timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                valute = data.get("Valute", {})

                for currency in currencies:
                    if currency in valute:
                        rates_list.append(
                            {
                                "currency": currency,
                                "rate": round(valute[currency]["Value"], 2),
                            }
                        )
                    else:
                        # Если валюта не найдена, используем заглушку
                        rates_list.append({"currency": currency, "rate": 0.0})
        except Exception as api_error:
            logger.warning(f"Не удалось получить курсы валют через API: {api_error}")
            # Возвращаем заглушки
            for currency in currencies:
                rates_list.append({"currency": currency, "rate": 0.0})

        logger.info(f"Получены курсы для {len(rates_list)} валют")
        return rates_list
    except Exception as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")
        return []


def get_stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """
    Получает цены акций через API.

    Args:
        stocks: Список тикеров акций

    Returns:
        Список словарей с ценами акций
    """
    try:
        # Для получения реальных цен акций нужен API-ключ
        # В демо-режиме используем заглушки
        stock_list = []

        # Пример цен (в реальном проекте получать через API)
        demo_prices = {
            "AAPL": 150.12,
            "AMZN": 3173.18,
            "GOOGL": 2742.39,
            "MSFT": 296.71,
            "TSLA": 1007.08,
        }

        for stock in stocks:
            stock_list.append({"stock": stock, "price": demo_prices.get(stock, 0.0)})

        logger.info(f"Получены цены для {len(stock_list)} акций")
        return stock_list
    except Exception as e:
        logger.error(f"Ошибка при получении цен акций: {e}")
        return []


def load_user_settings(settings_path: str = "user_settings.json") -> dict[str, Any]:
    """
    Загружает пользовательские настройки из JSON файла.

    Args:
        settings_path: Путь к файлу с настройками

    Returns:
        Словарь с настройками
    """
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
        logger.info("Пользовательские настройки загружены")
        return settings
    except Exception as e:
        logger.error(f"Ошибка при загрузке настроек: {e}")
        return {"user_currencies": [], "user_stocks": []}


def main_page(date_str: str, transactions_df: Optional[pd.DataFrame] = None) -> str:
    """
    Главная функция для генерации JSON-ответа для страницы "Главная".

    Args:
        date_str: Дата и время в формате 'YYYY-MM-DD HH:MM:SS'
        transactions_df: DataFrame с транзакциями (если None, загружается из файла)

    Returns:
        JSON-строка с данными для страницы
    """
    try:
        # Парсим дату
        current_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        logger.info(f"Генерация страницы 'Главная' для {date_str}")

        # Определяем начало месяца
        start_of_month = current_datetime.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

        # Загружаем данные, если не переданы
        if transactions_df is None:
            transactions_df = pd.read_excel("data/operations.xlsx")
            # Преобразуем первую колонку (дата операции) в datetime
            transactions_df.iloc[:, 0] = pd.to_datetime(
                transactions_df.iloc[:, 0], format="%d.%m.%Y %H:%M:%S"
            )

        # Загружаем настройки пользователя
        settings = load_user_settings()

        # Формируем ответ
        response = {
            "greeting": get_greeting(current_datetime),
            "cards": get_cards_info(transactions_df, start_of_month, current_datetime),
            "top_transactions": get_top_transactions(
                transactions_df, start_of_month, current_datetime, 5
            ),
            "currency_rates": get_currency_rates(settings.get("user_currencies", [])),
            "stock_prices": get_stock_prices(settings.get("user_stocks", [])),
        }

        json_response = json.dumps(response, ensure_ascii=False, indent=2)
        logger.info("Страница 'Главная' успешно сгенерирована")
        return json_response

    except Exception as e:
        logger.error(f"Ошибка при генерации страницы 'Главная': {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    # Пример использования
    result = main_page("2021-12-31 16:00:00")
    print(result)
