import os
from unittest.mock import MagicMock, patch

import pytest

from src.external_api import currency_rates, transactions_by_currency


@patch("requests.request")
def test_currency_rates(mock_request: MagicMock) -> None:
    """Тестирование работы функции извлечения и конвертации валюты в рубли через API apilayer"""
    code_to = "RUB"
    code_from = "USD"
    amount = "1"
    mock_request.return_value.json.return_value = {"result": 1.12}
    mock_request.return_value.status_code = 200
    assert currency_rates(code_to, code_from, amount) == 1.12

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={code_to}&from={code_from}&amount={amount}"

    api_key = os.getenv("APILAYER_API_KEY")
    headers = {"apikey": f"{api_key}"}

    mock_request.assert_called_once_with("GET", url, headers=headers, params={})


@patch("requests.request")
def test_currency_rates_status_error(mock_request: MagicMock) -> None:
    """Тестирование работы функции извлечения и конвертации валюты при коде состояния 400"""
    code_to = "RUB"
    code_from = "USD"
    amount = "1"

    mock_request.return_value.status_code = 400
    mock_request.return_value.text = "Error"
    with pytest.raises(Exception) as ex_info:
        currency_rates(code_to, code_from, amount)

    assert "Что-то пошло не так. Ошибка API: 400, Error" in str(ex_info.value)

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={code_to}&from={code_from}&amount={amount}"

    api_key = os.getenv("APILAYER_API_KEY")
    headers = {"apikey": f"{api_key}"}

    mock_request.assert_called_once_with("GET", url, headers=headers, params={})


def test_transactions_by_currency_code_rub(transactions) -> None:
    """Тестирование работы функции при коде валюты в транзакции RUB"""
    transaction = transactions[2]
    assert transactions_by_currency(transaction) == 43318.34


@patch("src.external_api.currency_rates")
def test_transactions_by_currency_code_not_rub(mock_get, transactions) -> None:
    """Тестирование работы функции при коде валюты в транзакции неравном RUB"""
    transaction = transactions[0]
    mock_get.return_value = 784283.3
    assert transactions_by_currency(transaction) == 784283.3
    mock_get.assert_called_once_with(code_to="RUB", code_from="USD", amount="9824.07")


def test_transactions_by_currency_empty_list() -> None:
    """Тестирование работы функции при пустом списке"""
    assert transactions_by_currency({}) == 0


def test_transaction_by_currency_except_exception() -> None:
    """Тестирование функции, если файл не найден"""
    assert (
        transactions_by_currency(
            {"invalid_key": "invalid_value", "number": 123, "boolean": "true"}
        )
        is None
    )
