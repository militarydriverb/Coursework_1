"""
Модуль для сервисов обработки транзакций.
Содержит функции для поиска транзакций и анализа данных.
"""

import json
import logging
from typing import Any

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def simple_search(transactions: list[dict[str, Any]], search_string: str) -> str:
    """
    Простой поиск транзакций по строке запроса.
    Ищет совпадения в описании или категории транзакции.

    Args:
        transactions: Список словарей с транзакциями
        search_string: Строка для поиска

    Returns:
        JSON-строка со списком найденных транзакций
    """
    try:
        logger.info(f"Поиск транзакций по запросу: '{search_string}'")

        if not search_string:
            logger.warning("Пустая строка поиска")
            return json.dumps([], ensure_ascii=False)

        # Приводим строку поиска к нижнему регистру для поиска без учета регистра
        search_lower = search_string.lower()

        # Используем функциональное программирование - filter
        def matches_search(transaction: dict[str, Any]) -> bool:
            """
            Проверяет, содержит ли транзакция искомую строку в описании или категории.

            Args:
                transaction: Словарь с данными транзакции

            Returns:
                True, если найдено совпадение
            """
            description = str(transaction.get("Описание", "")).lower()
            category = str(transaction.get("Категория", "")).lower()

            return search_lower in description or search_lower in category

        # Фильтруем транзакции
        found_transactions = list(filter(matches_search, transactions))

        logger.info(f"Найдено транзакций: {len(found_transactions)}")

        # Возвращаем результат в JSON
        return json.dumps(found_transactions, ensure_ascii=False, indent=2, default=str)

    except Exception as e:
        logger.error(f"Ошибка при поиске транзакций: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def search_by_phone_numbers(transactions: list[dict[str, Any]]) -> str:
    """
    Поиск транзакций, содержащих телефонные номера в описании.
    Использует функциональное программирование.

    Args:
        transactions: Список словарей с транзакциями

    Returns:
        JSON-строка со списком транзакций с телефонными номерами
    """
    import re

    try:
        logger.info("Поиск транзакций с телефонными номерами")

        # Регулярное выражение для поиска телефонных номеров
        # Формат: +7 XXX XXX-XX-XX или +7 (XXX) XXX-XX-XX и т.д.
        phone_pattern = re.compile(r"\+7\s*\(?\d{3}\)?\s*\d{3}[-\s]?\d{2}[-\s]?\d{2}")

        # Используем функциональное программирование - filter
        def has_phone_number(transaction: dict[str, Any]) -> bool:
            """
            Проверяет, содержит ли описание транзакции телефонный номер.

            Args:
                transaction: Словарь с данными транзакции

            Returns:
                True, если найден телефонный номер
            """
            description = str(transaction.get("Описание", ""))
            return bool(phone_pattern.search(description))

        # Фильтруем транзакции
        found_transactions = list(filter(has_phone_number, transactions))

        logger.info(
            f"Найдено транзакций с телефонными номерами: {len(found_transactions)}"
        )

        return json.dumps(found_transactions, ensure_ascii=False, indent=2, default=str)

    except Exception as e:
        logger.error(f"Ошибка при поиске транзакций с телефонными номерами: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def search_transfers_to_individuals(transactions: list[dict[str, Any]]) -> str:
    """
    Поиск переводов физическим лицам.
    Ищет транзакции категории "Переводы" с именем и первой буквой фамилии.
    Использует функциональное программирование.

    Args:
        transactions: Список словарей с транзакциями

    Returns:
        JSON-строка со списком переводов физлицам
    """
    import re

    try:
        logger.info("Поиск переводов физическим лицам")

        # Регулярное выражение для поиска имени и первой буквы фамилии
        # Формат: Имя Б. или Имя Б (с точкой или без)
        name_pattern = re.compile(r"[А-ЯЁA-Z][а-яёa-z]+\s+[А-ЯЁA-Z]\.?(?:\s|$)")

        # Используем функциональное программирование - filter
        def is_transfer_to_individual(transaction: dict[str, Any]) -> bool:
            """
            Проверяет, является ли транзакция переводом физлицу.

            Args:
                transaction: Словарь с данными транзакции

            Returns:
                True, если это перевод физлицу
            """
            category = str(transaction.get("Категория", ""))
            description = str(transaction.get("Описание", ""))

            # Проверяем категорию и наличие имени в описании
            is_transfer = "перевод" in category.lower()
            has_name = bool(name_pattern.search(description))

            return is_transfer and has_name

        # Фильтруем транзакции
        found_transactions = list(filter(is_transfer_to_individual, transactions))

        logger.info(f"Найдено переводов физлицам: {len(found_transactions)}")

        return json.dumps(found_transactions, ensure_ascii=False, indent=2, default=str)

    except Exception as e:
        logger.error(f"Ошибка при поиске переводов физлицам: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def investment_bank(
    month: str, transactions: list[dict[str, Any]], limit: int
) -> float:
    """
    Рассчитывает сумму, которую можно отложить в "Инвесткопилку"
    при округлении трат до заданного порога.

    Args:
        month: Месяц для расчета (формат 'YYYY-MM')
        transactions: Список словарей с транзакциями
        limit: Порог округления (10, 50 или 100)

    Returns:
        Сумма для откладывания в копилку
    """
    try:
        logger.info(f"Расчет инвесткопилки за {month} с порогом {limit}")

        # Используем функциональное программирование - map и filter
        # Фильтруем транзакции по месяцу
        def is_in_month(transaction: dict[str, Any]) -> bool:
            """Проверяет, относится ли транзакция к указанному месяцу."""
            date_str = str(transaction.get("Дата операции", ""))
            if not date_str:
                return False

            # Извлекаем месяц из даты
            try:
                # Формат даты может быть разным, пробуем несколько вариантов
                if "-" in date_str:
                    transaction_month = date_str[:7]  # YYYY-MM
                else:
                    # Формат DD.MM.YYYY
                    parts = date_str.split()[0].split(".")
                    if len(parts) >= 3:
                        transaction_month = f"{parts[2]}-{parts[1]}"
                    else:
                        return False

                return transaction_month == month
            except Exception:
                return False

        # Функция для расчета округления
        def calculate_rounding(transaction: dict[str, Any]) -> float:
            """Рассчитывает сумму округления для одной транзакции."""
            amount = transaction.get("Сумма операции", 0)

            # Учитываем только расходы (отрицательные суммы)
            if amount >= 0:
                return 0.0

            # Берем абсолютное значение
            abs_amount = abs(amount)

            # Округляем до ближайшего большего числа, кратного limit
            rounded_amount = ((int(abs_amount) // limit) + 1) * limit

            # Разница - это сумма для копилки
            return rounded_amount - abs_amount

        # Фильтруем и вычисляем
        month_transactions = filter(is_in_month, transactions)
        rounding_amounts = map(calculate_rounding, month_transactions)
        total = sum(rounding_amounts)

        logger.info(f"Сумма для инвесткопилки: {total:.2f}")
        return round(total, 2)

    except Exception as e:
        logger.error(f"Ошибка при расчете инвесткопилки: {e}")
        return 0.0


def cashback_categories_analysis(
    data: list[dict[str, Any]], year: int, month: int
) -> str:
    """
    Анализирует, какие категории были бы наиболее выгодными для повышенного кешбэка.
    Рассчитывает потенциальный кешбэк по каждой категории (5% вместо стандартного 1%).

    Args:
        data: Список словарей с транзакциями
        year: Год для анализа
        month: Месяц для анализа

    Returns:
        JSON-строка с анализом кешбэка по категориям
    """
    try:
        logger.info(f"Анализ выгодности категорий за {year}-{month:02d}")

        # Используем функциональное программирование
        # Фильтруем транзакции по году и месяцу
        def is_in_period(transaction: dict[str, Any]) -> bool:
            """Проверяет, относится ли транзакция к указанному периоду."""
            date_str = str(transaction.get("Дата операции", ""))
            if not date_str:
                return False

            try:
                # Формат DD.MM.YYYY или YYYY-MM-DD
                if "-" in date_str:
                    parts = date_str.split()[0].split("-")
                    trans_year = int(parts[0])
                    trans_month = int(parts[1])
                else:
                    parts = date_str.split()[0].split(".")
                    if len(parts) >= 3:
                        trans_year = int(parts[2])
                        trans_month = int(parts[1])
                    else:
                        return False

                return trans_year == year and trans_month == month
            except Exception:
                return False

        # Фильтруем транзакции
        period_transactions = list(filter(is_in_period, data))

        # Группируем по категориям и считаем расходы
        categories_spending: dict[str, float] = {}

        for transaction in period_transactions:
            category = transaction.get("Категория", "Без категории")
            amount = transaction.get("Сумма операции", 0)

            # Учитываем только расходы (отрицательные суммы)
            if amount < 0:
                if category not in categories_spending:
                    categories_spending[category] = 0.0
                categories_spending[category] += abs(amount)

        # Рассчитываем потенциальный кешбэк (5% - 1% = 4% дополнительно)
        # Используем map для преобразования
        def calculate_cashback(item: tuple[str, float]) -> tuple[str, float]:
            """Рассчитывает дополнительный кешбэк для категории."""
            category, spending = item
            additional_cashback = spending * 0.04  # 4% дополнительного кешбэка
            return (category, round(additional_cashback, 2))

        cashback_data = dict(map(calculate_cashback, categories_spending.items()))

        # Сортируем по убыванию кешбэка
        sorted_cashback = dict(
            sorted(cashback_data.items(), key=lambda x: x[1], reverse=True)
        )

        logger.info(f"Проанализировано категорий: {len(sorted_cashback)}")

        return json.dumps(sorted_cashback, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка при анализе категорий кешбэка: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    # Пример использования
    import pandas as pd

    # Загружаем данные
    df = pd.read_excel("data/operations.xlsx")
    transactions_list = df.to_dict("records")

    # Простой поиск
    print("=== Простой поиск ===")
    result = simple_search(transactions_list, "Лента")
    print(result[:500])  # Выводим первые 500 символов
