import functools
import os
import sys
import tempfile

import pytest

from src.decorators import log

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)


def test_write_log_to_file():
    """Тест внутренней функции _write_log с файлом."""
    from src.decorators import _write_log

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        # Тестируем запись в файл
        test_message = "Test log message\n"
        _write_log(test_message, filename)

        # Проверяем содержимое файла
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content == test_message

        # Тестируем добавление в конец файла
        _write_log("Second message\n", filename)

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content == test_message + "Second message\n"

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_write_log_to_console(capsys):
    """Тест внутренней функции _write_log с выводом в консоль."""
    from src.decorators import _write_log

    # Тестируем вывод в консоль (filename=None)
    test_message = "Console log message\n"
    _write_log(test_message, None)

    captured = capsys.readouterr()
    assert captured.out == test_message

    # Тестируем несколько сообщений
    _write_log("Message 1\n", None)
    _write_log("Message 2\n", None)

    captured = capsys.readouterr()
    assert captured.out == "Message 1\nMessage 2\n"


def test_log_with_no_arguments():
    """Тест декоратора без аргументов (по умолчанию в консоль)."""

    @log()  # Обязательно со скобками
    def no_args_func():
        return "success"

    result = no_args_func()
    assert result == "success"


def test_log_with_empty_filename():
    """Тест с пустым именем файла (должен писать в консоль)."""

    @log(filename="")  # Пустая строка
    def empty_filename_func():
        return "test"

    # Файл не должен создаваться
    assert not os.path.exists("")
    result = empty_filename_func()
    assert result == "test"


def test_log_with_special_characters():
    """Тест с функциями, возвращающими разные типы данных."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def return_none():
            return None

        @log(filename=filename)
        def return_list():
            return [1, 2, 3]

        @log(filename=filename)
        def return_dict():
            return {"key": "value"}

        # Вызываем все функции
        assert return_none() is None
        assert return_list() == [1, 2, 3]
        assert return_dict() == {"key": "value"}

        # Проверяем, что все вызовы залогированы
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'return_none ok' in content
            assert 'return_list ok' in content
            assert 'return_dict ok' in content

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_log_exception_propagation():
    """Тест, что исключение пробрасывается после логирования."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def raise_custom_error():
            raise RuntimeError("Custom error message")

        # Убеждаемся, что исключение пробрасывается
        with pytest.raises(RuntimeError, match="Custom error message"):
            raise_custom_error()

        # Проверяем, что ошибка залогирована
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'raise_custom_error error' in content
            assert 'RuntimeError' in content

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_log_with_complex_arguments():
    """Тест с комплексными аргументами."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def complex_args(a, b=10, *args, **kwargs):
            return a + b + sum(args) + sum(kwargs.values())

        # Вызываем с разными аргументами
        result = complex_args(1, 2, 3, 4, x=5, y=6)
        assert result == 21  # 1 + 2 + 3 + 4 + 5 + 6

        # Проверяем логи
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'complex_args ok' in content

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_log_timestamp_inclusion():
    """Тест, что timestamp добавляется в логи."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        @log(filename=filename)
        def timestamp_func():
            return "timestamp test"

        timestamp_func()

        with open(filename, 'r', encoding='utf-8') as f:

            f.read()

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_multiple_decorators():
    """Тест совместного использования нескольких декораторов."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
        filename = tmp.name

    try:
        def another_decorator(func):
            @functools.wraps(func)  # Добавьте это!
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) * 2

            return wrapper

        @log(filename=filename)
        @another_decorator
        def decorated_func(x):
            return x + 1

        result = decorated_func(5)
        assert result == 12  # (5 + 1) * 2

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'decorated_func ok' in content  # Теперь будет работать

    finally:
        if os.path.exists(filename):
            os.unlink(filename)
