import pytest

from src.services import filter_by_month, get_transactions_list


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
