from unittest.mock import patch

import pytest

from src.views import process_cards_info, say_hello


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


@patch("src.views.calculate_cashback")
@patch("src.views.get_total_expenses")
@patch("src.views.filter_by_date")
@patch("src.views.get_data_from_xlsx")
def test_process_cards_info(
    mock_get_df, mock_filter_df, mock_total_expenses, mock_cashback, get_df, monthly_operations, cashback
):
    """Тестирует нормальную работу функции."""
    mock_get_df.return_value = get_df
    mock_filter_df.return_value = get_df
    mock_total_expenses.return_value = monthly_operations
    mock_cashback.return_value = cashback
    assert process_cards_info("30.11.2021 18:19:28", "existing.xlsx")[:3] == [
        {
            "last_digits": "1112",
            "total_spent": 46207.08,
            "cashback": 462.07,
        },
        {
            "last_digits": "4556",
            "total_spent": 533948.75,
            "cashback": 5339.49,
        },
        {
            "last_digits": "5091",
            "total_spent": 14918.16,
            "cashback": 149.18,
        },
    ]
    mock_get_df.assert_called_once_with("existing.xlsx")
    mock_filter_df.assert_called_once_with("30.11.2021 18:19:28", get_df)


@pytest.mark.parametrize(
    "date, file",
    [
        ("30.11.2021 18:19:28", "no_such_file.xlsx"),
        ("30.11.2021", "existing.xlsx"),
        ("08-03-2022 15:45:00", "existing.xlsx"),
        ("08-03-2022 15:45:00", "no_such_file.xlsx"),
    ],
)
@patch("src.views.calculate_cashback")
@patch("src.views.get_total_expenses")
@patch("src.views.filter_by_date")
@patch("src.views.get_data_from_xlsx")
def test_process_cards_info_empty_data(
    mock_get_df, mock_filter_df, mock_total_expenses, mock_cashback, get_empty_df, date, file
):
    """Тестирует работу функции, когда переданы неверные входные данные."""
    mock_get_df.return_value = get_empty_df
    mock_filter_df.return_value = get_empty_df
    mock_total_expenses.return_value = {"nan": 0.0}
    mock_cashback.return_value = {"nan": [0.0, 0.0]}
    assert process_cards_info(date, file) == []
    mock_get_df.assert_called_once_with(file)
    mock_filter_df.assert_called_once_with(date, get_empty_df)
