from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info_card: str) -> str:
    """
    Обрабатывает информацию о картах и счетах.

    Возвращает тип (карта или счет) и замаскированный номер.

    Args:
        info_card: Строка с типом и номером (например, "Visa Platinum 7000792289606361"
                   или "Счет 73654108430135874305")

    Returns:
        str: Строка с типом и замаскированным номером

    Example:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'
        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
    """
    info_card_split = info_card.split()
    number_card = info_card_split[-1]
    if info_card_split[0] == "Счет":
        result = f"{info_card_split[0]} {get_mask_account(int(number_card))}"
    elif info_card_split[1].isdigit():
        result = f"{info_card_split[0]} {get_mask_card_number(int(number_card))}"
    else:
        result = f"{info_card_split[0] + ' ' + info_card_split[1]} {get_mask_card_number(int(number_card))}"
    return result


if __name__ == "__main__":
    print(mask_account_card("Счет 73654108430135874305"))  # pragma: no cover
    print(mask_account_card("Visa Platinum 7000792289606361"))  # pragma: no cover
    print(mask_account_card("Maestro 1596837868705199"))  # pragma: no cover


def get_date(date_str: str) -> str:
    """
    Преобразует дату из формата ISO 8601 в формат ДД.ММ.ГГГГ.

    Args:
        date_str: Строка с датой в формате ISO 8601 (например, "2024-03-11T02:26:18.671407")

    Returns:
        str: Строка с датой в формате 'ДД.ММ.ГГГГ'

    Raises:
        ValueError: Если день не в диапазоне 1-31 или месяц не в диапазоне 1-12
        TypeError: Если год содержит не только цифры

    Example:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    day = date_str[8:10]
    if not 31 >= int(day) >= 1:
        raise ValueError("Число только в диапазоне от 1 до 31")
    month = date_str[5:7]
    if not 12 >= int(month) >= 1:
        raise ValueError("Число только в диапазоне от 1 до 12")
    year = date_str[:4]
    if not year.isdigit():
        raise TypeError("Год должен состоять только из цифр")
    new_date_str = f"{day}.{month}.{year}"
    return new_date_str


if __name__ == "__main__":
    print(get_date("2024-03-11T02:26:18.671407"))  # pragma: no cover
