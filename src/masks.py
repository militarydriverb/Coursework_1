import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/masks.log", encoding="utf-8", mode="w+")
file_formater = logging.Formatter(
    "%(asctime)s %(filename)s %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: int) -> str:
    """
    Маскирует номер банковской карты.

    Принимает на вход номер карты в виде числа и возвращает
    маску номера по правилу XXXX XX** **** XXXX.

    Args:
        card_number: 16-значный номер карты

    Returns:
        str: Замаскированный номер карты в формате XXXX XX** **** XXXX

    Raises:
        TypeError: Если данные не переданы или имеют неверный тип
        ValueError: Если длина номера карты не равна 16 символам

    Example:
        >>> get_mask_card_number(1234567890123456)
        '1234 56** **** 3456'
    """
    logger.info("function get_mask_card_number is started")
    if not card_number:
        logger.error("no data")
        raise TypeError("Данные не переданы")
    else:
        logger.info("data successfully received and reformated")
        card_number_str = str(card_number)
        if not card_number_str.isnumeric():
            logger.error("wrong data type")
            raise TypeError("Неверный тип данных")
        if len(card_number_str) == 16:
            mask_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[12:]}"
            logger.info("card number successfully masked")
            return mask_number
        logger.error("wrong card number")
        raise ValueError("Неверный номер карты")


if __name__ == "__main__":
    print(
        get_mask_card_number(1234567890123456)
    )  # pragma: no cover type: ignore # noqa
    print(get_mask_card_number(123456789012345))  # pragma: no cover type: ignore # noqa
    print(
        get_mask_card_number("700079ffffffff")
    )  # pragma: no cover type: ignore # noqa
    print(get_mask_card_number(""))  # pragma: no cover type: ignore # noqa
    print(get_mask_card_number(None))  # pragma: no cover type: ignore # noqa


def get_mask_account(account_number: int) -> str:
    """
    Маскирует номер банковского счета.

    Принимает на вход номер счета в виде числа и
    возвращает маску номера по правилу **XXXX.

    Args:
        account_number: Номер счета (от 4 до 20 символов)

    Returns:
        str: Замаскированный номер счета в формате **XXXX или сообщение об ошибке

    Example:
        >>> get_mask_account(73654108430135874305)
        '**4305'
    """
    logger.info("function get_mask_account is started")
    if account_number is None:
        logger.info("no data")
        return "Неверный тип данных"
    else:
        logger.info("data successfully received and reformated")
        account_number_str = str(account_number)
        if not account_number_str.isnumeric():
            logger.error("wrong data type")
            return "Неверный тип данных"
    if 20 >= len(account_number_str) >= 4:
        mask_account = f"**{account_number_str[-4:]}"
        logger.info("account successfully masked")
        return mask_account
    logger.error("wrong account number")
    return "Неверный номер счета"


if __name__ == "__main__":
    print(get_mask_account(1234567890123456))  # pragma: no cover type: ignore # noqa
    print(
        get_mask_account(1234567890123456990987)
    )  # pragma: no cover type: ignore # noqa
    print(get_mask_account(""))  # pragma: no cover type: ignore # noqa
    print(get_mask_account("12345678901234asd"))  # pragma: no cover type: ignore # noqa
    print(get_mask_account(None))  # pragma: no cover type: ignore # noq
