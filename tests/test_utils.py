import tempfile
from unittest import mock
from unittest.mock import patch

import pytest
import requests

from src.utils import (calculate_cashback, filter_by_date, get_currencies, get_data_from_user, get_data_from_xlsx,
                       get_data_via_api_currencies, get_data_via_api_stocks, get_exchange_rates, get_stock_prices,
                       get_stocks, get_top_five_transactions, get_total_expenses, process_cards_info, say_hello,
                       sort_by_amount)


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


def test_filter_by_date(get_df, dec_df):
    """Тестирует нормальную работу функции."""
    current_month_df = filter_by_date("02.12.2021 00:00:00", get_df).iloc[:, :-1]
    assert current_month_df.equals(dec_df)


@pytest.mark.parametrize(
    "date",
    [
        "31.12.2021",
        "08-03-2022 15:45:00",
        "15:45:00",
        "2022-03-08 17:15:00",
    ],
)
def test_filter_by_date_wrong_date(get_df, get_empty_df, date, capsys):
    """Тестирует работу функции при передаче неверного формата даты."""
    assert filter_by_date(date, get_df).equals(get_empty_df)
    captured = capsys.readouterr()
    assert captured.out == "Неправильный формат даты. Введите дату в формате DD.MM.YY HH:MM:SS\n"


def test_sort_by_amount(get_df):
    """Тестирует нормальную работу функции."""
    assert sort_by_amount(get_df)[0] == {
        "Дата операции": "31.01.2018 20:09:33",
        "Дата платежа": "31.01.2018",
        "Номер карты": "*4556",
        "Статус": "OK",
        "Сумма операции": -1212.8,
        "Валюта операции": "RUB",
        "Сумма платежа": -1212.8,
        "Валюта платежа": "RUB",
        "Кэшбэк": 12.0,
        "Категория": "Ж/д билеты",
        "MCC": 4112.0,
        "Описание": "РЖД",
        "Бонусы (включая кэшбэк)": 12.0,
        "Округление на инвесткопилку": 0.0,
        "Сумма операции с округлением": 1212.8,
        "Correct sum": 1212.8,
    }


def test_get_total_expenses(get_df):
    """Тестирует нормальную работу функции."""
    assert get_total_expenses(get_df) == {"4556": 1267.80, "7197": 99.00}


def test_get_total_expenses_empty_df(get_empty_df):
    """Тестирует работу функции при отсутствии данных."""
    assert get_total_expenses(get_empty_df) == {"nan": 0.0}


def test_calculate_cashback(monthly_operations, cashback):
    """Тестирует нормальную работу функции."""
    assert calculate_cashback(monthly_operations) == cashback


def test_calculate_cashback_zero_expenses():
    """Тестирует работу функции, когда отсутствуют данные по операциям."""
    assert calculate_cashback({"nan": 0.0}) == {"nan": [0.0, 0.0]}


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


def test_process_cards_info(cashback):
    """Тестирует нормальную работу функции."""
    assert process_cards_info(cashback)[:3] == [
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


def test_process_cards_info_empty_data():
    """Тестирует работу функции, когда отсутствуют входные данные."""
    assert process_cards_info({"nan": [0.0, 0.0]}) == []


def test_get_top_five_transactions(get_df):
    transactions_list = sort_by_amount(get_df)
    assert get_top_five_transactions(transactions_list)[:2] == [
        {
            "date": "31.01.2018",
            "amount": -1212.80,
            "category": "Ж/д билеты",
            "description": "РЖД",
        },
        {
            "date": "01.12.2021",
            "amount": -99.00,
            "category": "Фастфуд",
            "description": "IP Yakubovskaya M.V.",
        },
    ]


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


@patch("src.utils.json.load")
@patch("src.utils.open")
def test_get_stocks(mock_open, mock_json_load, stocks):
    """Тестирует нормальную работу функции."""
    mock_json_load.return_value = stocks
    assert get_stocks("stocks.json") == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    mock_open.assert_called_once_with("stocks.json", "r", encoding="utf-8")


def test_get_stocks_no_such_file(capsys):
    """Тестирует работу функции, когда файл не найден."""
    file_name = "no_such_file.json"
    assert get_stocks(file_name) == []
    captured = capsys.readouterr()
    assert captured.out == "Файл не найден. Проверьте правильность введенных данных.\n"


def test_get_stocks_json_decode_error():
    """Тестирует работу функции при возникновении ошибки декодирования."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as tmp_file:
        data = "company: Apple Inc, tickerSymbol: AAPL"
        tmp_file.write(data)
        file_path = tmp_file.name
    assert get_stocks(file_path) == []


@pytest.mark.parametrize(
    "input_currencies, input_stocks, user_currencies, user_stocks",
    [
        ("USD,eur CNy, JPY", "aapl,GOOGL tSLA, AMZN", ["USD", "EUR", "CNY", "JPY"], ["AAPL", "GOOGL", "TSLA", "AMZN"]),
        ("KZt", "aapl,GOOGL tSLA, AMZN", ["KZT"], ["AAPL", "GOOGL", "TSLA", "AMZN"]),
        ("eur CNy", "msft ", ["EUR", "CNY"], ["MSFT"]),
    ],
)
@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.utils.json.dump")
@patch("src.utils.open")
@patch("src.utils.get_stocks")
@patch("src.utils.get_currencies")
def test_get_data_from_user(
    mock_get_currencies,
    mock_get_stocks,
    mock_open,
    mock_json_dump,
    mock_join,
    mock_dirname,
    input_currencies,
    input_stocks,
    user_currencies,
    user_stocks,
):
    """Тестирует нормальную работу функции."""
    mock_get_currencies.return_value = ["USD", "EUR", "CNY", "JPY", "KZT"]
    mock_get_stocks.return_value = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    get_data_from_user(input_currencies, input_stocks)
    mock_open.assert_called_once_with("/mock/path/user_settings.json", "w", encoding="utf-8")
    mock_json_dump.assert_called_with(
        {"user_currencies": user_currencies, "user_stocks": user_stocks}, mock_open().__enter__()
    )


@patch("src.utils.get_stocks")
@patch("src.utils.get_currencies")
def test_get_data_from_user_logger_messages(mock_get_currencies, mock_get_stocks, caplog):
    mock_get_currencies.return_value = []
    mock_get_stocks.return_value = []
    get_data_from_user("USD,eur CNy, JPY", "aapl,GOOGL tSLA, AMZN")
    assert "Failed to get data about codes and symbols" in caplog.messages


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


@patch("src.utils.requests.get")
def test_get_data_via_api_currencies(mock_get, api_response_currencies):
    """Тестирует нормальную работу функции."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = api_response_currencies
    result = get_data_via_api_currencies(["USD", "EUR", "CNY", "JPY", "KZT"])
    assert result == (True, [87.99, 95.18, 11.89, 59.64, 18.44])


@patch("src.utils.requests.get")
def test_get_data_via_api_currencies_denied_request(mock_get):
    """Тестирует работу функции, когда запрос был заблокирован."""
    mock_get.return_value.status_code = 403
    mock_get.return_value.reason = "Forbidden"
    result = get_data_via_api_currencies(["USD", "EUR", "CNY", "JPY", "KZT"])
    assert result == (False, "Forbidden")


def test_get_data_via_api_currencies_request_error():
    """Тестирует работу функции при возникновении ошибки."""
    with mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Something went wrong")):
        result = get_data_via_api_currencies(["USD", "EUR", "CNY", "JPY", "KZT"])
    assert result == (False, "Something went wrong")


@patch("src.utils.requests.get")
def test_get_data_via_api_stocks(mock_get, api_response_stocks):
    """Тестирует нормальную работу функции."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = api_response_stocks
    result = get_data_via_api_stocks(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
    assert result == (True, [216.24, 166.94, 163.67, 406.02, 200])


@patch("src.utils.requests.get")
def test_get_data_via_api_stocks_denied_access(mock_get):
    """Тестирует работу функции, когда доступ был запрещен."""
    mock_get.return_value.status_code = 401
    mock_get.return_value.reason = "Unauthorized"
    result = get_data_via_api_stocks(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
    assert result == (False, "Unauthorized")


def test_get_data_via_api_stocks_request_error():
    """Тестирует работу функции при возникновении ошибки."""
    with mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Something went wrong")):
        result = get_data_via_api_stocks(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
    assert result == (False, "Something went wrong")


@patch("src.utils.get_data_via_api_currencies")
def test_get_exchange_rates(mock_get_currencies):
    """Тестирует нормальную работу функции."""
    mock_get_currencies.return_value = (True, [87.99, 95.18, 11.89, 59.64, 18.44])
    assert get_exchange_rates(["USD", "EUR", "CNY", "JPY", "KZT"])[:2] == [
        {"currency": "USD", "rate": 87.99},
        {"currency": "EUR", "rate": 95.18},
    ]


@pytest.mark.parametrize("return_status, return_result", [(False, "Forbidden"), (False, "Something went wrong")])
@patch("src.utils.get_data_via_api_currencies")
def test_get_exchange_rates_unsuccessful_operation(mock_get_currencies, return_status, return_result):
    """Тестирует работу функции при неудачной попытке получить данные через API."""
    mock_get_currencies.return_value = (return_status, return_result)
    assert get_exchange_rates(["USD", "EUR", "CNY", "JPY", "KZT"]) is None


@patch("src.utils.get_data_via_api_stocks")
def test_get_stock_prices(mock_get_stocks):
    """Тестирует нормальную работу функции."""
    mock_get_stocks.return_value = (True, [216.24, 166.94, 163.67, 406.02, 200])
    assert get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])[:2] == [
        {"stock": "AAPL", "price": 216.24},
        {"stock": "AMZN", "price": 166.94},
    ]


@pytest.mark.parametrize("return_status, return_result", [(False, "Unauthorized"), (False, "Something went wrong")])
@patch("src.utils.get_data_via_api_stocks")
def test_get_stock_prices_unsuccessful_operation(mock_get_stocks, return_status, return_result):
    mock_get_stocks.return_value = (return_status, return_result)
    assert get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]) is None
