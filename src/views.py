import json
import os
from datetime import datetime

from src.utils import (calculate_cashback, filter_by_date, get_data_from_xlsx, get_exchange_rates, get_stock_prices,
                       get_top_five_transactions, get_total_expenses, process_cards_info, say_hello, sort_by_amount)


def generate_json_response(date: str) -> str:
    """Основная функция для страницы Главная."""

    file_path = os.path.dirname(os.path.dirname(__file__))

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        hour = date_obj.hour
        formated_date = date_obj.strftime("%d.%m.%Y %H:%M:%S")

    except ValueError:
        print("Неправильный формат даты. Введите дату в формате YYYY-MM-DD HH:MM:SS")

    else:
        with open(os.path.join(file_path, "user_settings.json")) as settings_file:
            user_settings = json.load(settings_file)

        all_operations = get_data_from_xlsx(os.path.join(file_path, "data", "operations.xlsx"))
        current_month_operations = filter_by_date(formated_date, all_operations)
        current_month_expenses = calculate_cashback(get_total_expenses(current_month_operations))

        result = {
            "greeting": say_hello(hour),
            "cards": process_cards_info(current_month_expenses),
            "top_transactions": get_top_five_transactions(sort_by_amount(current_month_operations)),
            "currency_rates": get_exchange_rates(user_settings.get("user_currencies")),
            "stock_prices": get_stock_prices(user_settings.get("user_stocks")),
        }

        return json.dumps(result, ensure_ascii=False, indent=4)
