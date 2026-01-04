from datetime import datetime


def filter_by_state(list_of_dict: list, state: str = "EXECUTED") -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению.

    Args:
        list_of_dict: Список словарей для фильтрации
        state: Значение состояния для фильтрации (по умолчанию "EXECUTED")

    Returns:
        list: Новый список отфильтрованных словарей

    Example:
        >>> data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]
        >>> filter_by_state(data, "EXECUTED")
        [{"id": 1, "state": "EXECUTED"}]
    """
    filtered_list = []
    for dict_item in list_of_dict:
        if dict_item.get("state") == state:
            filtered_list.append(dict_item)

    return filtered_list


# Проверка работы кода
if __name__ == "__main__":
    print(
        filter_by_state(
            [
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                },  # pragma: no cover
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                },  # pragma: no cover
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                },  # pragma: no cover
                {
                    "id": 615064591,
                    "state": "CANCELED",
                    "date": "2018-10-14T08:21:33.419441",
                },
            ]
        )
    )  # pragma: no cover


def sort_by_date(data_list: list, descending: bool = True) -> list:
    """
    Сортирует список словарей по ключу 'date'.

    Принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).

    Args:
        data_list: Список словарей с ключом 'date' в формате ISO 8601
        descending: Порядок сортировки (True - убывание, False - возрастание)

    Returns:
        list: Новый список, отсортированный по дате

    Example:
        >>> data = [
        ...     {"id": 1, "date": "2019-07-03T18:35:29.512364"},
        ...     {"id": 2, "date": "2018-06-30T02:08:58.425572"}
        ... ]
        >>> sort_by_date(data)
        [{"id": 1, "date": "2019-07-03T18:35:29.512364"}, ...]
    """
    data_key = "date"
    return sorted(
        data_list,
        key=lambda x: datetime.strptime(x[data_key], "%Y-%m-%dT%H:%M:%S.%f"),
        reverse=descending,
    )
    # return sorted(data_list, key=lambda x: x.get('date'), reverse=descending)

    # Проверка работы кода


if __name__ == "__main__":
    print(
        sort_by_date(
            [
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                },  # pragma: no cover
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                },  # pragma: no cover
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                },  # pragma: no cover
                {
                    "id": 615064591,
                    "state": "CANCELED",
                    "date": "2018-10-14T08:21:33.419441",
                },  # pragma: no cover
            ]
        )
    )

    print(
        sort_by_date(
            [
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                },  # pragma: no cover
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                },  # pragma: no cover
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                },  # pragma: no cover
                {
                    "id": 615064591,
                    "state": "CANCELED",
                    "date": "2018-10-14T08:21:33.419441",
                },  # pragma: no cover
            ]
        )
    )
