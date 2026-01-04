import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "info_card, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(info_card: str, expected: str) -> None:
    """Тестирование функции корректности распознавания и применения нужного типа маскировки в зависимости
    от типа входных данных (карта или счет)."""
    assert mask_account_card(info_card) == expected


def test_get_date() -> None:
    """Тестирование функции возвращения строки с датой в формате 'ДД.ММ.ГГГГ"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


def test_get_data_day_error() -> None:
    """Тестирование корректности числа даты"""
    with pytest.raises(ValueError) as ex_info:
        get_date("2024-03-32")
        assert str(ex_info.value) == "Число только в диапазоне от 1 до 31"


def test_get_data_month_error() -> None:
    """Тестирование корректности месяца даты"""
    with pytest.raises(ValueError) as ex_info:
        get_date("2024-14-31")
        assert str(ex_info.value) == "Число только в диапазоне от 1 до 12"


def test_get_data_year_error() -> None:
    """Тестирование корректности года даты"""
    with pytest.raises(TypeError) as ex_info:
        get_date("202F-03-31")
        assert str(ex_info.value) == "Год должен состоять только из цифр"
