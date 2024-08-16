import json
from unittest.mock import mock_open, patch

import pytest

from src.reports import spending_by_category, write_to_file


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


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.reports.json.dump")
def test_write_to_file_json(mock_json, mock_join, mock_dirname, mock_opened):
    """Тестирует запись данных в JSON-файл."""

    @write_to_file("report.json")
    def sample_function():
        return json.dumps({"key": "value"})

    sample_function()

    mock_json.assert_called_once_with(
        {"key": "value"},
        mock_opened("/mock/path/data/report.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )
    mock_opened.assert_called_with("/mock/path/data/report.json", "w", encoding="utf-8")


@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("pandas.DataFrame.to_csv")
def test_write_to_file_csv(mock_to_csv, mock_join, mock_dirname):
    """Тестирует запись данных в CSV-файл."""

    @write_to_file("report.csv")
    def sample_function():
        return json.dumps({"key1": ["value1", "value2"], "key2": ["value3", "value4"]})

    sample_function()

    mock_to_csv.assert_called_once_with("/mock/path/data/report.csv", index=False)


@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("pandas.DataFrame.to_excel")
def test_write_to_file_excel(mock_to_excel, mock_join, mock_dirname):
    """Тестирует запись данных в XLSX-файл."""

    @write_to_file("report.xlsx")
    def sample_function():
        return json.dumps({"key1": ["value1", "value2"], "key2": ["value3", "value4"]})

    sample_function()

    mock_to_excel.assert_called_once_with("/mock/path/data/report.xlsx", index=False)
