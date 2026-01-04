import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7000792289606361", "7000 79** **** 6361"),
        ("1596837868705199", "1596 83** **** 5199"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("6831982476737658", "6831 98** **** 7658"),
        ("8990922113665229", "8990 92** **** 5229"),
        ("5999414228426353", "5999 41** **** 6353"),
        ("9999999999999999", "9999 99** **** 9999"),
        ("0000000000000000", "0000 00** **** 0000"),
    ],
)
def test_get_mask_card_number(card_number: int, expected: str) -> None:
    """Тестирование правильности маскирования номера карты."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("card_number", ["", None])
def test_get_mask_card_number_none(card_number: int) -> None:
    """Тестирование правильности маскирования номера карты, если данные не переданы."""
    with pytest.raises(TypeError) as ex_info:
        get_mask_card_number(card_number)
        assert str(ex_info.value) == "Данные не переданы"


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("700079ffffffff", "Неверный тип данных"),
        (["lala", "lalal", "lalal"], "Неверный тип данных"),
        ({"[f[f[", "[f[f[f"}, "Неверный тип данных"),
    ],
)
def test_get_mask_card_number_error_type(card_number: int, expected: str) -> None:
    """Тестирование правильности маскирования номера карты, если не верныЙ тип данных"""
    with pytest.raises(TypeError) as ex_info:
        get_mask_card_number(card_number)
        assert str(ex_info.value) == expected


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("70007922896061", "Неверный номер карты"),
        ("12345667765433345566776543345677", "Неверный номер карты"),
        (1234, "Неверный номер карты"),
    ],
)
def test_get_mask_card_number_wrong_number(card_number: int, expected: str) -> None:
    """Тестирование правильности маскирования номера карты, если номер карты не верен"""
    with pytest.raises(ValueError) as ex_info:
        get_mask_card_number(card_number)
        assert str(ex_info.value) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("64686473678894779589", "**9589"),
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305"),
        ("7365410843013587lala", "Неверный тип данных"),
        ("7365410843013587", "**3587"),
        ("", "Неверный тип данных"),
        (None, "Неверный тип данных"),
        ("edyatlikoshimoshek", "Неверный тип данных"),
        ("не ну а вдруг", "Неверный тип данных"),
        ("12345667765433345566776543345677", "Неверный номер счета"),
        (1234, "**1234"),
        (["lala", "lalal", "lalal"], "Неверный тип данных"),
        ({"[f[f[", "[f[f[f"}, "Неверный тип данных"),
        ("64686473678894779589", "**9589"),
        ("35383033474447895560", "**5560"),
        ("73654108430135874305", "**4305"),
    ],
)
def test_get_mask_account(account_number: int, expected: str) -> None:
    """Тестирование правильности маскирования номера счета."""
    assert get_mask_account(account_number) == expected
