from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """Фильтрует транзакции по заданной валюте и возвращает итератор."""
    return filter(
        lambda x: x.get("operationAmount", {}).get("currency", {}).get("code")
        == currency,
        transactions,
    )


def transaction_descriptions(transactions: list) -> Iterator[dict]:
    """Принимает список словарей с транзакциями и возвращает
    описание каждой операции по очереди."""
    for i in transactions:
        yield i["description"]


def card_number_generator(start: int, stop: int):
    """Выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты.
    Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999.
    Генератор должен принимать начальное и конечное значения для генерации диапазона номеров.
    """
    if start < 1 or stop > 9999999999999999:
        raise ValueError("Число не может быть меньше 1 и больше 9999999999999999")
    for i in range(start, stop + 1):
        card_number = str(i).zfill(16)
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"


if __name__ == "__main__":
    transactions = [  # pragma: no cover type: ignore # noqa
        {  # pragma: no cover type: ignore # noqa
            "id": 939719570,  # pragma: no cover type: ignore # noqa
            "state": "EXECUTED",  # pragma: no cover type: ignore # noqa
            "date": "2018-06-30T02:08:58.425572",  # pragma: no cover type: ignore # noqa
            "operationAmount": {  # pragma: no cover type: ignore # noqa
                "amount": "9824.07",  # pragma: no cover type: ignore # noqa
                "currency": {  # pragma: no cover type: ignore # noqa
                    "name": "USD",  # pragma: no cover type: ignore # noqa
                    "code": "USD",  # pragma: no cover type: ignore # noqa
                },  # pragma: no cover type: ignore # noqa
            },  # pragma: no cover type: ignore # noqa
            "description": "Перевод организации",  # pragma: no cover type: ignore # noqa
            "from": "Счет 75106830613657916952",  # pragma: no cover type: ignore # noqa
            "to": "Счет 11776614605963066702",  # pragma: no cover type: ignore # noqa
        },  # pragma: no cover type: ignore # noqa
        {  # pragma: no cover type: ignore # noqa
            "id": 142264268,  # pragma: no cover type: ignore # noqa
            "state": "EXECUTED",  # pragma: no cover type: ignore # noqa
            "date": "2019-04-04T23:20:05.206878",  # pragma: no cover type: ignore # noqa
            "operationAmount": {  # pragma: no cover type: ignore # noqa
                "amount": "79114.93",  # pragma: no cover type: ignore # noqa
                "currency": {  # pragma: no cover type: ignore # noqa
                    "name": "USD",  # pragma: no cover type: ignore # noqa
                    "code": "USD",  # pragma: no cover type: ignore # noqa
                },  # pragma: no cover type: ignore # noqa
            },  # pragma: no cover type: ignore # noqa
            "description": "Перевод со счета на счет",  # pragma: no cover type: ignore # noqa
            "from": "Счет 19708645243227258542",  # pragma: no cover type: ignore # noqa
            "to": "Счет 75651667383060284188",  # pragma: no cover type: ignore # noqa
        },  # pragma: no cover type: ignore # noqa
        {  # pragma: no cover type: ignore # noqa
            "id": 873106923,  # pragma: no cover type: ignore # noqa
            "state": "EXECUTED",  # pragma: no cover type: ignore # noqa
            "date": "2019-03-23T01:09:46.296404",  # pragma: no cover type: ignore # noqa
            "operationAmount": {  # pragma: no cover type: ignore # noqa
                "amount": "43318.34",  # pragma: no cover type: ignore # noqa
                "currency": {  # pragma: no cover type: ignore # noqa
                    "name": "руб.",  # pragma: no cover type: ignore # noqa
                    "code": "RUB",  # pragma: no cover type: ignore # noqa
                },  # pragma: no cover type: ignore # noqa
            },  # pragma: no cover type: ignore # noqa
            "description": "Перевод со счета на счет",  # pragma: no cover type: ignore # noqa
            "from": "Счет 44812258784861134719",  # pragma: no cover type: ignore # noqa
            "to": "Счет 74489636417521191160",  # pragma: no cover type: ignore # noqa
        },  # pragma: no cover type: ignore # noqa
        {  # pragma: no cover type: ignore # noqa
            "id": 895315941,  # pragma: no cover type: ignore # noqa
            "state": "EXECUTED",  # pragma: no cover type: ignore # noqa
            "date": "2018-08-19T04:27:37.904916",  # pragma: no cover type: ignore # noqa
            "operationAmount": {  # pragma: no cover type: ignore # noqa
                "amount": "56883.54",  # pragma: no cover type: ignore # noqa
                "currency": {  # pragma: no cover type: ignore # noqa
                    "name": "USD",  # pragma: no cover type: ignore # noqa
                    "code": "USD",  # pragma: no cover type: ignore # noqa
                },  # pragma: no cover type: ignore # noqa
            },  # pragma: no cover type: ignore # noqa
            "description": "Перевод с карты на карту",  # pragma: no cover type: ignore # noqa
            "from": "Visa Classic 6831982476737658",  # pragma: no cover type: ignore # noqa
            "to": "Visa Platinum 8990922113665229",  # pragma: no cover type: ignore # noqa
        },  # pragma: no cover type: ignore # noqa
        {  # pragma: no cover type: ignore # noqa
            "id": 594226727,  # pragma: no cover type: ignore # noqa
            "state": "CANCELED",  # pragma: no cover type: ignore # noqa
            "date": "2018-09-12T21:27:25.241689",  # pragma: no cover type: ignore # noqa
            "operationAmount": {  # pragma: no cover type: ignore # noqa
                "amount": "67314.70",  # pragma: no cover type: ignore # noqa
                "currency": {  # pragma: no cover type: ignore # noqa
                    "name": "руб.",  # pragma: no cover type: ignore # noqa
                    "code": "RUB",  # pragma: no cover type: ignore # noqa
                },  # pragma: no cover type: ignore # noqa
            },  # pragma: no cover type: ignore # noqa
            "description": "Перевод организации",  # pragma: no cover type: ignore # noqa
            "from": "Visa Platinum 1246377376343588",  # pragma: no cover type: ignore # noqa
            "to": "Счет 14211924144426031657",  # pragma: no cover type: ignore # noqa
        },  # pragma: no cover type: ignore # noqa
    ]  # pragma: no cover type: ignore # noqa
    # Фильтрация транзакций с валютой USD               # pragma: no cover type: ignore # noqa
    usd_transactions = filter_by_currency(
        transactions, "USD"
    )  # pragma: no cover type: ignore # noqa
    for _ in range(2):  # pragma: no cover type: ignore # noqa
        print(next(usd_transactions))  # pragma: no cover type: ignore # noqa
        # pragma: no cover type: ignore # noqa
    descriptions = transaction_descriptions(
        transactions
    )  # pragma: no cover type: ignore # noqa
    for _ in range(5):  # pragma: no cover type: ignore # noqa
        print(next(descriptions))  # pragma: no cover type: ignore # noqa
        # pragma: no cover type: ignore # noqa
    for card_number in card_number_generator(
        1, 5
    ):  # pragma: no cover type: ignore # noqa
        print(card_number)  # pragma: no cover type: ignore # noqa
