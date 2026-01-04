import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


def test_filter_by_currency(transactions, input_by_currency):
    """Тестирование корректности фильтра транзакций по заданной валюте"""
    currency, expected = input_by_currency
    assert list(filter_by_currency(transactions, currency)) == expected


def test_filter_by_currency_no_currency(transactions):
    """Тестирование корректности работы функции при отсутствии транзакций в заданной валюте
    или пустого списка валютны операций"""
    assert list(filter_by_currency(transactions, "EUR")) == []


def test_transaction_descriptions(transactions):
    """Тестирование корректности возврата описания для каждой транзакции"""
    result = list(transaction_descriptions(transactions))
    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


def test_transaction_description_no_transactions():
    """Тестирование работы функции в различным количеством транзакций включая пустой список"""
    result = list(transaction_descriptions([]))
    assert result == []


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (
            10001,
            10003,
            ["0000 0000 0001 0001", "0000 0000 0001 0002", "0000 0000 0001 0003"],
        ),
        (
            9999999999999998,
            9999999999999999,
            ["9999 9999 9999 9998", "9999 9999 9999 9999"],
        ),
    ],
)
def test_card_number_generator(start, stop, expected):
    """Тестирование корректности возврата номеров карт в заданном диапазоне и их форматирования"""
    assert list(card_number_generator(start, stop)) == expected


def test_card_number_generator_digits_number():
    """Тестирование корректности обработки крайних значений"""
    with pytest.raises(ValueError) as ex_info:
        list(card_number_generator(0, 5))
    assert (
        str(ex_info.value) == "Число не может быть меньше 1 и больше 9999999999999999"
    )
