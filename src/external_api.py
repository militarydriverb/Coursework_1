import os
from typing import Optional

import requests
from dotenv import load_dotenv

try:
    from src.csv_excel_data import get_excel_data_reading
except ModuleNotFoundError:
    from csv_excel_data import get_excel_data_reading

load_dotenv()

API_KEY = os.getenv("APILAYER_API_KEY")


def currency_rates(code_to: str, code_from: str, amount: str) -> float:
    """
    Получает актуальный курс валюты через API exchangerates_data.

    Args:
        code_to: Код валюты, в которую конвертируем (например, 'RUB')
        code_from: Код валюты, из которой конвертируем (например, 'USD')
        amount: Сумма для конвертации

    Returns:
        float: Конвертированная сумма, округленная до 2 знаков

    Raises:
        Exception: При ошибке запроса к API или неверном статус-коде
    """
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={code_to}&from={code_from}&amount={amount}"

    payload: dict = {}
    headers = {"apikey": f"{API_KEY}"}
    try:
        response = requests.request("GET", url, headers=headers, params=payload)
        status_code = response.status_code
        result = response.text

        if response.status_code != 200:
            raise Exception(f"Ошибка API: {status_code}, {result}")

    except Exception as ex_info:
        raise Exception(f"Что-то пошло не так. {str(ex_info)}")
    else:
        output_data = response.json()
        return round(float(output_data.get("result", 0)), 2)


def transactions_by_currency(operation: Optional[dict]) -> None | int | float:
    """Функция конвертация транзакции в рубли по актуальному курсу"""

    try:
        if not operation:
            print("Словарь пуст")
            return 0
        currency_code = operation["operationAmount"]["currency"]["code"]
        amount_value = operation["operationAmount"]["amount"]

        if currency_code == "RUB":
            result = round(float(amount_value), 2)
        else:
            result = currency_rates(
                code_to="RUB", code_from=currency_code, amount=amount_value
            )
        return result
    except Exception as e:
        print(str(e))
    return None


if __name__ == "__main__":
    data_str = get_excel_data_reading("data/operations.xlsx")  # pragma: no cover
    if data_str:  # pragma: no cover
        print(transactions_by_currency(data_str[1]))  # pragma: no cover
