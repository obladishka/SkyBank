from unittest.mock import patch

from src.views import generate_json_response


@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.views.get_stock_prices")
@patch("src.views.get_exchange_rates")
@patch("src.views.get_top_five_transactions")
@patch("src.views.process_cards_info")
@patch("src.views.json.load")
@patch("src.views.open")
def test_generate_json_response(
    mock_open,
    mock_json,
    mock_process_cards_info,
    mock_get_top_five_transactions,
    mock_get_get_exchange_rates,
    mock_get_stock_prices,
    mock_join,
    mock_dirname,
    json_response,
    get_df,
):
    """Тестирует нормальную работу функции."""
    mock_json.return_value = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}
    mock_process_cards_info.return_value = [
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
    mock_get_top_five_transactions.return_value = [
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
    mock_get_get_exchange_rates.return_value = [
        {"currency": "USD", "rate": 87.99},
        {"currency": "EUR", "rate": 95.18},
    ]
    mock_get_stock_prices.return_value = [
        {"stock": "AAPL", "price": 216.24},
        {"stock": "AMZN", "price": 166.94},
    ]
    assert generate_json_response("2022-03-08 15:45:00", get_df) == json_response
    mock_open.assert_called_once_with("/mock/path/user_settings.json")


def test_generate_json_response_wrong_date(get_df, capsys):
    """Тестирует работу функции при передаче неверной даты."""
    assert generate_json_response("31.12.2021 16:44:00", get_df) is None
    captured = capsys.readouterr()
    assert captured.out == "Неправильный формат даты. Введите дату в формате YYYY-MM-DD HH:MM:SS\n"
