import json
import os

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv


def get_data_from_xlsx(file_path: str) -> pd.DataFrame | None:
    """Функция для считывания инфы из excel-файла."""
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        print("Файл не найден. Проверьте правильность введенных данных.")
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


def get_currencies(currencies_file: str) -> list:
    """Функция для получения списка существующих валют."""
    try:
        with open(currencies_file, "r", encoding="utf-8") as cf:
            try:
                currencies = json.load(cf)
                return [currency.get("code") for currency in currencies]
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        print("Файл не найден. Проверьте правильность введенных данных.")
        return []


def get_stocks(stocks_file: str) -> list:
    """Функция для получения списка тикеров компаний S&P 500."""
    try:
        with open(stocks_file, "r", encoding="utf-8") as sf:
            try:
                companies = json.load(sf)
                return [company.get("tickerSymbol") for company in companies]
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        print("Файл не найден. Проверьте правильность введенных данных.")
        return []


def get_data_from_user(user_currencies: str, user_stocks: str) -> None | str:
    """Функция для записи пользовательских настроек в файл."""

    file_path = os.path.dirname(os.path.dirname(__file__))

    codes = get_currencies(os.path.join(file_path, "data", "currencies.json"))
    symbols = get_stocks(os.path.join(file_path, "data", "sandp500.json"))

    user_currencies = user_currencies.upper().replace(",", " ").replace("  ", " ").split()
    user_stocks = user_stocks.upper().replace(",", " ").replace("  ", " ").split()

    if any(currency not in codes for currency in user_currencies) or any(
        stock not in symbols for stock in user_stocks
    ):
        return "Проверьте правильность введенных данных."

    # Вносим пользовательские данные в файл
    with open(os.path.join(file_path, "user_settings.json"), "w", encoding="utf-8") as of:
        user_settings = {"user_currencies": user_currencies, "user_stocks": user_stocks}
        json.dump(user_settings, of)


def get_data_via_api_currencies(currencies: list[str]) -> tuple:
    """Функция для получения текущего курса валют."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    try:
        response = requests.get(url)
        status_code = response.status_code

        if status_code == 200:
            currencies_data = response.json()["Valute"]
            currencies_rates = [currencies_data.get(currency, {}).get("Value") for currency in currencies]
            return True, list(map(lambda x: round(x, 2), currencies_rates))

        return False, str(response.reason)

    except requests.exceptions.RequestException as ex:
        return False, str(ex)


def get_data_via_api_stocks(stocks: list[str]) -> tuple:
    """Функция для получения текущего курса валют."""
    load_dotenv()

    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={os.getenv("API_KEY")}"

    try:
        response = requests.get(url)
        status_code = response.status_code

        if status_code == 200:
            stocks_data = response.json()
            stocks_prices = [i.get("price") for i in stocks_data for stock in stocks if i.get("symbol") == stock]
            return True, stocks_prices

        return False, str(response.reason)

    except requests.exceptions.RequestException as ex:
        return False, str(ex)
