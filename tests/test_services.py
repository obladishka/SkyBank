import json

import pytest

from src.services import filter_by_month, get_transactions_list, investment_bank, round_to_limit


def test_get_transactions_list(get_df):
    """Тестирует нормальную работу функции."""
    assert get_transactions_list(get_df)[:2] == [
        {"Дата операции": "2021-12-01", "Сумма операции": -99.00},
        {"Дата операции": "2021-11-30", "Сумма операции": -55.00},
    ]


def test_get_transactions_list_empty_df(get_empty_df):
    """Тестирует работу функции при пустом датафрейме."""
    assert get_transactions_list(get_empty_df) == []


def test_filter_by_month(transactions_list):
    """Тестирует нормальную работу функции."""
    assert filter_by_month("2021-12", transactions_list) == transactions_list[:2]
    assert filter_by_month("2021-11", transactions_list) == transactions_list[2:]


@pytest.mark.parametrize("date", ["2021-12-11", "11-12-2021", "2021.12", "12-2021"])
def test_filter_by_month_wrong_date(date, transactions_list, capsys):
    """Тестирует работу функции при неправильных входных данных."""
    assert filter_by_month(date, transactions_list) == []
    captured = capsys.readouterr()
    assert captured.out == "Неправильный формат даты. Введите дату в формате YYYY-MM\n"


def test_filter_by_month_empty_list():
    """Тестирует работу функции при пустом списке транзакций."""
    assert filter_by_month("2021-12", []) == []


@pytest.mark.parametrize(
    "amount, limit, expected",
    [
        (-160.89, 10, 9.11),
        (-160.89, 50, 39.11),
        (-64.0, 10, 6.0),
        (-64.0, 100, 36.0),
        (-103.0, 10, 7.0),
        (-103.0, 50, 47.0),
        (-103.0, 100, 97.0),
        (500.0, 10, 0.0),
        (500.0, 50, 0.0),
        (500.0, 100, 0.0),
    ],
)
def test_round_to_limit(amount, limit, expected):
    """Тестирует нормальную работу функции с различными входными данными."""
    assert round_to_limit(amount, limit) == expected


def test_round_to_limit_incorrect_limit(capsys):
    """Тестирует работу функции, когда неверно указан лимит."""
    assert round_to_limit(500.0, 45) == 0.0
    captured = capsys.readouterr()
    assert captured.out == "Указан неверный лимит. Выберите лимит из возможных вариантов: 10, 50, 100\n"


@pytest.mark.parametrize(
    "month, limit, expected",
    [
        ("2021-12", 10, 15.11),
        ("2021-12", 50, 75.11),
        ("2021-12", 100, 75.11),
        ("2021-11", 10, 24.5),
        ("2021-11", 50, 104.5),
        ("2021-11", 100, 204.5),
    ],
)
def test_investment_bank(month, limit, expected, transactions_list):
    """Тестирует нормальную работу функции с различными входными данными."""
    assert investment_bank(month, transactions_list, limit) == json.dumps(
        {"month": month, "investment_amount": expected}
    )


@pytest.mark.parametrize(
    "limit, expected",
    [
        (10, None),
        (50, None),
        (100, None),
    ],
)
def test_investment_bank_no_transactions(transactions_list, limit, expected):
    """Тестирует работу функции, когда транзакции не найдены."""
    assert investment_bank("2021-10", transactions_list, limit) is expected


def test_investment_bank_wrong_limit(transactions_list, capsys):
    """Тестирует работу функции, когда транзакции не найдены."""
    assert investment_bank("2021-11", transactions_list, 25) == json.dumps(
        {"month": "2021-11", "investment_amount": 0.0}
    )
    captured = capsys.readouterr()
    assert "Указан неверный лимит. Выберите лимит из возможных вариантов: 10, 50, 100\n" in captured.out
