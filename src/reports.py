"""
Модуль для генерации отчетов по транзакциям.
Содержит функции для анализа трат по категориям, дням недели и т.д.
"""

import functools
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/reports.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report_to_file(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для записи результата функции-отчета в файл.

    Args:
        filename: Имя файла для записи (если None, используется имя по умолчанию)

    Returns:
        Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Вызываем функцию
            result = func(*args, **kwargs)

            # Определяем имя файла
            if filename is None:
                # Формат по умолчанию: report_<имя_функции>_<timestamp>.txt
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"report_{func.__name__}_{timestamp}.txt"
            else:
                output_filename = filename

            # Создаем директорию reports, если её нет
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)

            # Формируем полный путь
            output_path = reports_dir / output_filename

            # Записываем результат в файл
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    if isinstance(result, pd.DataFrame):
                        f.write(result.to_string())
                    elif isinstance(result, (dict, list)):
                        f.write(json.dumps(result, ensure_ascii=False, indent=2))
                    else:
                        f.write(str(result))

                logger.info(f"Отчет сохранен в файл: {output_path}")
            except Exception as e:
                logger.error(f"Ошибка при записи отчета в файл: {e}")

            return result

        return wrapper

    return decorator


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями
        category: Название категории
        date: Дата в формате 'DD.MM.YYYY' (если None, берется текущая дата)

    Returns:
        DataFrame с тратами по категории за последние 3 месяца
    """
    try:
        logger.info(f"Формирование отчета по категории '{category}'")

        # Определяем конечную дату
        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%d.%m.%Y")

        # Начальная дата - 3 месяца назад
        start_date = end_date - timedelta(days=90)

        logger.info(
            f"Период отчета: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"
        )

        # Копируем DataFrame, чтобы не изменять оригинал
        df = transactions.copy()

        # Преобразуем колонку с датой, если это строка
        date_col = df.columns[0]  # Первая колонка - дата операции
        if df[date_col].dtype == "object":
            df[date_col] = pd.to_datetime(
                df[date_col], format="%d.%m.%Y %H:%M:%S", errors="coerce"
            )

        # Фильтруем по дате
        mask = (df[date_col] >= start_date) & (df[date_col] <= end_date)
        filtered = df[mask]

        # Фильтруем по категории (колонка 9)
        category_col = df.columns[9]
        category_mask = filtered[category_col] == category
        category_filtered = filtered[category_mask]

        # Берем только расходы (отрицательные суммы)
        amount_col = df.columns[4]  # Сумма операции
        expenses = category_filtered[category_filtered[amount_col] < 0].copy()

        # Создаем отчет
        if len(expenses) > 0:
            # Добавляем абсолютные значения
            expenses["Сумма трат"] = expenses[amount_col].abs()

            # Группируем по месяцам
            expenses["Месяц"] = expenses[date_col].dt.to_period("M")

            # Формируем итоговый DataFrame
            report = (
                expenses.groupby("Месяц")
                .agg({"Сумма трат": "sum", amount_col: "count"})
                .reset_index()
            )

            report.columns = ["Месяц", "Общая сумма", "Количество операций"]
            report["Месяц"] = report["Месяц"].astype(str)

            logger.info(f"Отчет сформирован: {len(report)} месяцев")
            return report
        else:
            logger.warning(f"Нет данных по категории '{category}' за указанный период")
            return pd.DataFrame(columns=["Месяц", "Общая сумма", "Количество операций"])

    except Exception as e:
        logger.error(f"Ошибка при формировании отчета по категории: {e}")
        return pd.DataFrame(columns=["Месяц", "Общая сумма", "Количество операций"])


def spending_by_weekday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает средние траты в каждый из дней недели за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями
        date: Дата в формате 'DD.MM.YYYY' (если None, берется текущая дата)

    Returns:
        DataFrame со средними тратами по дням недели
    """
    try:
        logger.info("Формирование отчета по дням недели")

        # Определяем конечную дату
        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%d.%m.%Y")

        # Начальная дата - 3 месяца назад
        start_date = end_date - timedelta(days=90)

        # Копируем DataFrame
        df = transactions.copy()

        # Преобразуем колонку с датой
        date_col = df.columns[0]
        if df[date_col].dtype == "object":
            df[date_col] = pd.to_datetime(
                df[date_col], format="%d.%m.%Y %H:%M:%S", errors="coerce"
            )

        # Фильтруем по дате
        mask = (df[date_col] >= start_date) & (df[date_col] <= end_date)
        filtered = df[mask]

        # Берем только расходы
        amount_col = df.columns[4]
        expenses = filtered[filtered[amount_col] < 0].copy()

        if len(expenses) > 0:
            # Добавляем день недели
            expenses["День недели"] = expenses[date_col].dt.day_name()
            expenses["Сумма трат"] = expenses[amount_col].abs()

            # Группируем по дням недели и считаем среднее
            weekday_stats = (
                expenses.groupby("День недели")
                .agg({"Сумма трат": "mean", amount_col: "count"})
                .reset_index()
            )

            weekday_stats.columns = [
                "День недели",
                "Средняя сумма",
                "Количество операций",
            ]

            # Сортируем по дням недели
            weekday_order = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            weekday_stats["order"] = weekday_stats["День недели"].map(
                {day: i for i, day in enumerate(weekday_order)}
            )
            weekday_stats = weekday_stats.sort_values("order").drop("order", axis=1)

            # Переводим названия дней на русский
            weekday_translation = {
                "Monday": "Понедельник",
                "Tuesday": "Вторник",
                "Wednesday": "Среда",
                "Thursday": "Четверг",
                "Friday": "Пятница",
                "Saturday": "Суббота",
                "Sunday": "Воскресенье",
            }
            weekday_stats["День недели"] = weekday_stats["День недели"].map(
                weekday_translation
            )

            logger.info(f"Отчет сформирован: {len(weekday_stats)} дней")
            return weekday_stats
        else:
            logger.warning("Нет данных за указанный период")
            return pd.DataFrame(
                columns=["День недели", "Средняя сумма", "Количество операций"]
            )

    except Exception as e:
        logger.error(f"Ошибка при формировании отчета по дням недели: {e}")
        return pd.DataFrame(
            columns=["День недели", "Средняя сумма", "Количество операций"]
        )


def spending_by_workday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает средние траты в рабочий и выходной день за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями
        date: Дата в формате 'DD.MM.YYYY' (если None, берется текущая дата)

    Returns:
        DataFrame со средними тратами по типу дня
    """
    try:
        logger.info("Формирование отчета по рабочим/выходным дням")

        # Определяем конечную дату
        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%d.%m.%Y")

        # Начальная дата - 3 месяца назад
        start_date = end_date - timedelta(days=90)

        # Копируем DataFrame
        df = transactions.copy()

        # Преобразуем колонку с датой
        date_col = df.columns[0]
        if df[date_col].dtype == "object":
            df[date_col] = pd.to_datetime(
                df[date_col], format="%d.%m.%Y %H:%M:%S", errors="coerce"
            )

        # Фильтруем по дате
        mask = (df[date_col] >= start_date) & (df[date_col] <= end_date)
        filtered = df[mask]

        # Берем только расходы
        amount_col = df.columns[4]
        expenses = filtered[filtered[amount_col] < 0].copy()

        if len(expenses) > 0:
            # Определяем тип дня (0-4 = рабочие, 5-6 = выходные)
            expenses["Тип дня"] = expenses[date_col].dt.dayofweek.apply(
                lambda x: "Рабочий день" if x < 5 else "Выходной день"
            )
            expenses["Сумма трат"] = expenses[amount_col].abs()

            # Группируем по типу дня
            workday_stats = (
                expenses.groupby("Тип дня")
                .agg({"Сумма трат": "mean", amount_col: "count"})
                .reset_index()
            )

            workday_stats.columns = ["Тип дня", "Средняя сумма", "Количество операций"]

            logger.info("Отчет по рабочим/выходным дням сформирован")
            return workday_stats
        else:
            logger.warning("Нет данных за указанный период")
            return pd.DataFrame(
                columns=["Тип дня", "Средняя сумма", "Количество операций"]
            )

    except Exception as e:
        logger.error(f"Ошибка при формировании отчета по типу дня: {e}")
        return pd.DataFrame(columns=["Тип дня", "Средняя сумма", "Количество операций"])


# Применяем декоратор к функциям-отчетам
spending_by_category = report_to_file()(spending_by_category)
spending_by_weekday = report_to_file()(spending_by_weekday)
spending_by_workday = report_to_file()(spending_by_workday)


if __name__ == "__main__":
    # Пример использования
    df = pd.read_excel("data/operations.xlsx")

    print("=== Отчет по категории ===")
    result1 = spending_by_category(df, "Супермаркеты", "31.12.2021")
    print(result1)

    print("\n=== Отчет по дням недели ===")
    result2 = spending_by_weekday(df, "31.12.2021")
    print(result2)

    print("\n=== Отчет по рабочим/выходным дням ===")
    result3 = spending_by_workday(df, "31.12.2021")
    print(result3)
