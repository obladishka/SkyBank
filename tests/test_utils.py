import tempfile
from unittest.mock import patch

import pytest

from src.utils import get_currencies, get_data_from_user, get_data_from_xlsx


@patch("src.utils.pd.read_excel")
def test_get_data_from_xlsx(mock_read_excel, get_df):
    """Тестирует нормальную работу функции."""
    mock_read_excel.return_value = get_df
    assert get_data_from_xlsx("existing.xlsx").equals(get_df)
    mock_read_excel.assert_called_once_with("existing.xlsx")


def test_get_data_from_xlsx_no_such_file(get_empty_df, capsys):
    """Тестирует работу функции, когда Excel-файл не найден."""
    file_name = "no_such_file.xlsx"
    get_data_from_xlsx(file_name)
    captured = capsys.readouterr()
    assert captured.out == "Файл не найден. Проверьте правильность введенных данных.\n"
    assert get_data_from_xlsx(file_name).equals(get_empty_df)


@patch("src.utils.json.load")
@patch("src.utils.open")
def test_get_currencies(mock_open, mock_json_load, currencies):
    """Тестирует нормальную работу функции."""
    mock_json_load.return_value = currencies
    assert get_currencies("currencies.json") == ["USD", "EUR", "CNY", "JPY", "KZT"]
    mock_open.assert_called_once_with("currencies.json", "r", encoding="utf-8")


def test_get_currencies_no_such_file(capsys):
    """Тестирует работу функции, когда файл не найден."""
    file_name = "no_such_file.json"
    assert get_currencies(file_name) == []
    captured = capsys.readouterr()
    assert captured.out == "Файл не найден. Проверьте правильность введенных данных.\n"


def test_get_currencies_json_decode_error():
    """Тестирует работу функции при возникновении ошибки декодирования."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as tmp_file:
        data = """{
            "symbol": "KZT",
            "name": {"Kazakhstani Tenge"},
            "symbol_native": "тңг.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "KZT",
            "name_plural": "Kazakhstani tenges"
        }"""
        tmp_file.write(data)
        file_path = tmp_file.name
    assert get_currencies(file_path) == []


@pytest.mark.parametrize(
    "input_currencies, input_stocks, user_currencies, user_stocks",
    [
        ("USD,eur CNy, JPY", "aapl,GOOGL tSLA, AMZN", ["USD", "EUR", "CNY", "JPY"], ["AAPL", "GOOGL", "TSLA", "AMZN"]),
        ("KZt", "aapl,GOOGL tSLA, AMZN", ["KZT"], ["AAPL", "GOOGL", "TSLA", "AMZN"]),
        ("eur CNy", "msft ", ["EUR", "CNY"], ["MSFT"]),
    ],
)
@patch("src.utils.json.dump")
@patch("src.utils.open")
@patch("src.utils.get_stocks")
@patch("src.utils.get_currencies")
def test_get_data_from_user(
    mock_get_currencies,
    mock_get_stocks,
    mock_open,
    mock_json_dump,
    input_currencies,
    input_stocks,
    user_currencies,
    user_stocks,
):
    """Тестирует нормальную работу функции."""
    mock_get_currencies.return_value = ["USD", "EUR", "CNY", "JPY", "KZT"]
    mock_get_stocks.return_value = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    get_data_from_user(input_currencies, input_stocks)
    mock_open.assert_called_once_with(
        "C:\\Users\\user\\Desktop\\python\\python_work\\Course_3\\SkyBank\\user_settings.json", "w", encoding="utf-8"
    )
    mock_json_dump.assert_called_with(
        {"user_currencies": user_currencies, "user_stocks": user_stocks}, mock_open().__enter__()
    )


@pytest.mark.parametrize(
    "input_currencies, input_stocks",
    [
        ("wrong_currency", "aapl,GOOGL tSLA, AMZN"),
        ("USD,eur CNy, JPY", "wrong_symbol"),
        ("byr", "tmos, MCX"),
    ],
)
@patch("src.utils.get_stocks")
@patch("src.utils.get_currencies")
def test_get_data_from_user_wrong_data(mock_get_currencies, mock_get_stocks, input_currencies, input_stocks):
    """Тестирует работу функции при вводе несуществующих валют или тикеров, не входящих в S&P 500."""
    mock_get_currencies.return_value = ["USD", "EUR", "CNY", "JPY", "KZT"]
    mock_get_stocks.return_value = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    assert get_data_from_user(input_currencies, input_stocks) == "Проверьте правильность введенных данных."
