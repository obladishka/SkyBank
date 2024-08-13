import json
from unittest.mock import patch

import pytest

from src.reports import spending_by_category


def test_spending_by_category(get_df, dec_df):
    """Тестирует нормальную работу функции."""
    assert spending_by_category(get_df, "Фастфуд", "01.12.2021 12:35:05") == json.dumps(
        dec_df.to_dict(orient="records"), ensure_ascii=False, indent=4
    )


@pytest.mark.parametrize("date", ["01.12.2021", "01-12-2021 12:35:05", "2021-12-01 12:35:05", "2021-12-01"])
def test_spending_by_category_wrong_date(get_df, date, capsys):
    """Тестирует работу функции при передаче неверного формата даты."""
    assert spending_by_category(get_df, "Фастфуд", date) is None
    captured = capsys.readouterr()
    assert captured.out == "Неправильный формат даты. Введите дату в формате DD.MM.YY HH:MM:SS\n"


@patch("src.reports.pd.DataFrame.to_dict")
def test_spending_by_category_json_dumps_error(mock_df_to_dict, get_df, caplog):
    """Тестирует работу функции при ошибке сериализации данных."""
    mock_df_to_dict.return_value = {
        "symbol": "KZT",
        "name": {"Kazakhstani Tenge"},
        "symbol_native": "тңг.",
        "decimal_digits": 2,
        "rounding": 0,
        "code": "KZT",
        "name_plural": "Kazakhstani tenges",
    }
    assert spending_by_category(get_df, "Фастфуд", "01.12.2021 12:35:05") is None
    assert "Object of type set is not JSON serializable" in caplog.messages


def test_spending_by_category_no_transactions(get_df):
    """Тестирует работу функции, когда транзакций по заданной категории не найдено."""
    assert spending_by_category(get_df, "Not existing category", "01.12.2021 12:35:05") == "[]"
