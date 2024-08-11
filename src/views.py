from src.utils import calculate_cashback, filter_by_date, get_data_from_xlsx, get_total_expenses


def say_hello(time: int) -> str:
    """Функция для вывода приветствия в зависимости от текущего времени."""
    if 0 <= time <= 23:
        return (
            "Доброй ночи"
            if 0 <= time < 5
            else "Доброе утро" if 5 <= time < 12 else "Добрый день" if 12 <= time < 18 else "Добрый вечер"
        )
    return "Неверно указано время. Проверьте правильность введенных данных."


def process_cards_info(date: str, file_path: str) -> list[dict]:
    """Функция для вывода информации по каждой карте."""

    all_operations = get_data_from_xlsx(file_path)
    current_month_operations = filter_by_date(date, all_operations)
    current_month_expenses = get_total_expenses(current_month_operations)
    operations_dict = calculate_cashback(current_month_expenses)

    cards = [key for key in operations_dict.keys() if key != "nan"]
    return [
        {
            "last_digits": card,
            "total_spent": round(operations_dict.get(card)[0], 2),
            "cashback": operations_dict.get(card)[1],
        }
        for card in cards
    ]
