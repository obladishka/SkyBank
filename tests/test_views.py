import pytest

from src.views import say_hello


@pytest.mark.parametrize(
    "time, expected",
    [
        (0, "Доброй ночи"),
        (4, "Доброй ночи"),
        (5, "Доброе утро"),
        (11, "Доброе утро"),
        (12, "Добрый день"),
        (15, "Добрый день"),
        (18, "Добрый вечер"),
        (23, "Добрый вечер"),
    ],
)
def test_say_hello(time, expected):
    """Тестирует нормальную работу функции с различными входными данными."""
    assert say_hello(time) == expected


def test_say_hello_wrong_time():
    """Тестирует работу функции, когда передано неверное время."""
    assert say_hello(24) == "Неверно указано время. Проверьте правильность введенных данных."
