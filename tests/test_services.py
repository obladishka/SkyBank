from src.services import get_transactions_list


def test_get_transactions_list(get_df):
    """Тестирует нормальную работу функции."""
    assert get_transactions_list(get_df)[:2] == [
        {"Дата операции": "2021-12-01", "Сумма операции": -99.00},
        {"Дата операции": "2021-11-30", "Сумма операции": -55.00},
    ]


def test_get_transactions_list_empty_df(get_empty_df):
    """Тестирует работу функции при пустом датафрейме."""
    assert get_transactions_list(get_empty_df) == []
