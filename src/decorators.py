import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: Имя файла для записи логов. Если None - вывод в консоль.

    Returns:
        Декорированную функцию с логированием.
    """

    # Сначала определяем внутренний декоратор
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем успешное сообщение
                log_message = f"{func_name} ok\n"

                # Логируем результат
                _write_log(log_message, filename)

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = f"{func_name} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}\n"

                # Логируем ошибку
                _write_log(error_message, filename)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    # Теперь обрабатываем случай @log без скобок
    if callable(filename):
        # @log без скобок: filename - это функция
        func = filename
        # Используем None как значение по умолчанию для filename
        return decorator(func)
    else:
        # @log() или @log(filename="...")
        return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """
    Записывает сообщение в файл или выводит в консоль.

    Args:
        message: Сообщение для логирования.
        filename: Имя файла. Если None - вывод в консоль.
    """
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message)
    else:
        print(message, end="")
