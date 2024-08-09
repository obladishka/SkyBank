import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def get_df() -> pd.DataFrame:
    data = {
        "Дата операции": ["01.12.2021 12:35:05", "30.11.2021 18:19:28", "31.01.2018 20:09:33"],
        "Дата платежа": ["01.12.2021", "30.11.2021", "02.02.2018"],
        "Номер карты": ["*7197", "*4556", "	*4556"],
        "Статус": ["OK", "FAILED", "OK"],
        "Сумма операции": [-99.00, -55.00, -1212.80],
        "Валюта операции": ["RUB", "RUB", "RUB"],
        "Сумма платежа": [-99.00, -55.00, -1212.80],
        "Валюта платежа": ["RUB	", "RUB", "RUB"],
        "Кэшбэк": [np.nan, np.nan, 12],
        "Категория": ["Фастфуд", np.nan, "Ж/д билеты"],
        "MCC": [5814, np.nan, 4112],
        "Описание": ["IP Yakubovskaya M.V.", "Перевод на карту", "РЖД"],
        "Бонусы (включая кэшбэк)": [1.00, 0.00, 12.00],
        "Округление на инвесткопилку": [0.00, 0.00, 0.00],
        "Сумма операции с округлением": [99.00, 55.00, 1212.80],
    }

    return pd.DataFrame(data)


@pytest.fixture
def get_empty_df() -> pd.DataFrame:
    data = {
        "Дата операции": [np.nan],
        "Дата платежа": [np.nan],
        "Номер карты": [np.nan],
        "Статус": [np.nan],
        "Сумма операции": [np.nan],
        "Валюта операции": [np.nan],
        "Сумма платежа": [np.nan],
        "Валюта платежа": [np.nan],
        "Кэшбэк": [np.nan],
        "Категория": [np.nan],
        "MCC": [np.nan],
        "Описание": [np.nan],
        "Бонусы (включая кэшбэк)": [np.nan],
        "Округление на инвесткопилку": [np.nan],
        "Сумма операции с округлением": [np.nan],
    }
    return pd.DataFrame(data)


@pytest.fixture
def currencies() -> list[dict[str, str | int]]:
    return [
        {
            "symbol": "$",
            "name": "US Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "USD",
            "name_plural": "US dollars",
        },
        {
            "symbol": "€",
            "name": "Euro",
            "symbol_native": "€",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "EUR",
            "name_plural": "euros",
        },
        {
            "symbol": "CN¥",
            "name": "Chinese Yuan",
            "symbol_native": "CN¥",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "CNY",
            "name_plural": "Chinese yuan",
        },
        {
            "symbol": "¥",
            "name": "Japanese Yen",
            "symbol_native": "￥",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "JPY",
            "name_plural": "Japanese yen",
        },
        {
            "symbol": "KZT",
            "name": "Kazakhstani Tenge",
            "symbol_native": "тңг.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "KZT",
            "name_plural": "Kazakhstani tenges",
        },
    ]


@pytest.fixture
def stocks() -> list[dict[str, str]]:
    return [
        {"company": "Apple Inc", "tickerSymbol": "AAPL"},
        {"company": "Amazon.com Inc", "tickerSymbol": "AMZN"},
        {"company": "Alphabet Inc Cl A", "tickerSymbol": "GOOGL"},
        {"company": "Microsoft Corp", "tickerSymbol": "MSFT"},
        {"company": "Tesla Inc", "tickerSymbol": "TSLA"},
    ]
