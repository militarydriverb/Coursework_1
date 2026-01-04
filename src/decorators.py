from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функции.

    Автоматически логирует начало и конец выполнения функции,
    а также результаты или возникшие ошибки.

    Args:
        filename: Путь к файлу для записи логов. Если None, логи выводятся в консоль.

    Returns:
        Callable: Декорированная функция с логированием

    Example:
        @log(filename="mylog.txt")
        def my_function(x, y):
            return x / y
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                name_func = func.__name__
                if filename:
                    file = open(filename, "a", encoding="utf-8")
                    file.write(f"Функция {name_func} ok. Результат: {result}" + "\n")
                    file.close()
                else:
                    print(f"{name_func} ok. Результат: {func(*args, **kwargs)}")
            except Exception as e:
                result = None
                print(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
            return result

        return wrapper

    return decorator
