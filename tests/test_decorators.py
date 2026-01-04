import os

from src.decorators import log


@log()
def my_function(x, y):
    return x / y


def test_my_function_success(capsys):
    """Тестирование на успешное выполнение функции"""
    result = my_function(4, 2)
    assert result == 2
    captured = capsys.readouterr()
    assert f"my_function ok. Результат: {round(result, 1)}\n" in captured.out


def test_my_function_division_by_zero(capsys):
    """Тестирование ошибки деления на ноль"""
    result = my_function(4, 0)
    captured = capsys.readouterr()
    assert result is None
    assert captured.out == "my_function error: division by zero. Inputs: (4, 0), {}\n"


@log(filename="test_log.txt")
def my_function_sum(x, y):
    return x + y


def test_my_function_file_output():
    """Тестирование вывода в файл"""
    my_function_sum(2, 3)
    with open("test_log.txt", "r", encoding="utf-8") as file:
        content = file.read()
    assert "Функция my_function_sum ok. Результат: 5" in content
    os.remove("test_log.txt")
