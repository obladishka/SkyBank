import json
import logging
import os
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "utils.log")

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_data_from_xlsx(file_path: str) -> pd.DataFrame | None:
    """Функция для считывания инфы из excel-файла."""
    try:
        logger.info(f"Trying to read info form {file_path}")
        df = pd.read_excel(file_path)
        logger.info("Successful operation")
        return df
    except FileNotFoundError as ex:
        logger.error(ex)
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


def filter_by_date(current_date: str, df: pd.DataFrame) -> pd.DataFrame:
    """Функция для фильтрации операций с начала месяца по текущую дату."""
    try:
        logger.info("Getting start and end date")
        end_date = datetime.strptime(current_date, "%d.%m.%Y %H:%M:%S")
        start_time = datetime.strptime(f"01.{end_date.month}.{end_date.year} 00:00:00", "%d.%m.%Y %H:%M:%S")

        logger.info("Formatting dates in df")
        df["date"] = df["Дата операции"].map(lambda x: datetime.strptime(str(x), "%d.%m.%Y %H:%M:%S"))
        logger.info(f"Getting operations from {start_time} to {end_date}")
        return df[(df["date"] >= start_time) & (df["date"] <= end_date)]

    except ValueError as ex:
        logger.error(ex)
        print("Неправильный формат даты. Введите дату в формате DD.MM.YY HH:MM:SS")
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


def sort_by_amount(df: pd.DataFrame) -> list[dict]:
    """Функция для сортировки транзакций по сумме платежа."""
    df_copy = df.loc[::]
    logger.info("Formating transactions sum to abs number")
    df_copy["Correct sum"] = df_copy["Сумма операции"].map(lambda x: -x if x < 0 else x)
    logger.info("Sorting by abs transactions sum in descending order")
    sorted_by_expenses_desc = df_copy.sort_values(by="Correct sum", ascending=False)
    logger.info("Returning result in a form of dict")
    return sorted_by_expenses_desc.to_dict(orient="records")


def get_total_expenses(df: pd.DataFrame) -> dict[str, float]:
    """Функция для получения общей суммы расходов по каждой карте."""
    df_copy = df.loc[::]
    logger.info("Formating card numbers")
    df_copy["Formated card numbers"] = df_copy["Номер карты"].map(lambda x: str(x).replace("*", ""))
    logger.info("Grouping operations by card numbers")
    grouped_data = df_copy.groupby("Formated card numbers")["Сумма платежа"].sum().map(lambda x: -x if x < 0 else x)
    logger.info("Returning result in a form of dict")
    return grouped_data.to_dict()


def calculate_cashback(operations_dict: dict) -> dict:
    """Функция, считающая кэшбэк (1 рубль на каждые 100 рублей)."""
    logger.info("Calculating cashback for each card and adding this info to the dict")
    for key, value in operations_dict.items():
        cash_back = round(value / 100, 2)
        operations_dict[key] = [value]
        operations_dict[key].append(cash_back)
    logger.info("Returning updated dict")
    return operations_dict


def say_hello(time: int) -> str:
    """Функция для вывода приветствия в зависимости от текущего времени."""
    if 0 <= time <= 23:
        return (
            "Доброй ночи"
            if 0 <= time < 5
            else "Доброе утро" if 5 <= time < 12 else "Добрый день" if 12 <= time < 18 else "Добрый вечер"
        )
    return "Неверно указано время. Проверьте правильность введенных данных."


def process_cards_info(operations_dict: dict) -> list[dict]:
    """Функция для вывода информации по каждой карте."""

    cards = [key for key in operations_dict.keys() if key != "nan"]
    return [
        {
            "last_digits": card,
            "total_spent": round(operations_dict.get(card)[0], 2),
            "cashback": operations_dict.get(card)[1],
        }
        for card in cards
    ]


def get_currencies(currencies_file: str) -> list:
    """Функция для получения списка существующих валют."""
    try:
        logger.info(f"Trying to open a file {currencies_file}")
        with open(currencies_file, "r", encoding="utf-8") as cf:
            try:
                logger.info("Trying to deserialize file data")
                currencies = json.load(cf)
                logger.info("Data deserialized successfully")
                return [currency.get("code") for currency in currencies]
            except json.JSONDecodeError as ex:
                logger.error(ex)
                return []
    except FileNotFoundError as ex:
        logger.error(ex)
        print("Файл не найден. Проверьте правильность введенных данных.")
        return []


def get_stocks(stocks_file: str) -> list:
    """Функция для получения списка тикеров компаний S&P 500."""
    try:
        logger.info(f"Trying to open a file {stocks_file}")
        with open(stocks_file, "r", encoding="utf-8") as sf:
            try:
                logger.info("Trying to deserialize file data")
                companies = json.load(sf)
                logger.info("Data deserialized successfully")
                return [company.get("tickerSymbol") for company in companies]
            except json.JSONDecodeError as ex:
                logger.error(ex)
                return []
    except FileNotFoundError as ex:
        logger.error(ex)
        print("Файл не найден. Проверьте правильность введенных данных.")
        return []


def get_data_from_user(user_currencies: str, user_stocks: str) -> None | str:
    """Функция для записи пользовательских настроек в файл."""

    file_path = os.path.dirname(os.path.dirname(__file__))

    logger.info("Getting codes and symbols lists")
    codes = get_currencies(os.path.join(file_path, "data", "currencies.json"))
    symbols = get_stocks(os.path.join(file_path, "data", "sandp500.json"))

    if not codes or not symbols:
        logger.warning(
            f"Failed to get data about {'codes and symbols' if not codes and not symbols else 'codes ' if not codes
                                        else 'symbols'}"
        )

    logger.info("Getting user preferences")
    user_currencies = user_currencies.upper().replace(",", " ").replace("  ", " ").split()
    user_stocks = user_stocks.upper().replace(",", " ").replace("  ", " ").split()

    logger.info("Checking if user preferences are valid")
    if any(currency not in codes for currency in user_currencies) or any(
        stock not in symbols for stock in user_stocks
    ):
        logger.warning(
            f"{'Currencies and stocks' if any(currency not in codes for currency in user_currencies) and
                any(stock not in symbols for stock in user_stocks) else 'Currencies'
                if any(currency not in codes for currency in user_currencies) else 'Stocks'} are invalid"
        )
        return "Проверьте правильность введенных данных."

    logger.info("Writing user settings into file.")
    with open(os.path.join(file_path, "user_settings.json"), "w", encoding="utf-8") as of:
        user_settings = {"user_currencies": user_currencies, "user_stocks": user_stocks}
        json.dump(user_settings, of)


def get_data_via_api_currencies(currencies: list[str]) -> tuple:
    """Функция для получения текущего курса валют."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    logger.info("Trying to get current currencies rates.")
    try:
        response = requests.get(url)
        status_code = response.status_code

        if status_code == 200:
            logger.info("Current currencies rates got successfully.")
            currencies_data = response.json()["Valute"]
            currencies_rates = [currencies_data.get(currency, {}).get("Value") for currency in currencies]
            logger.info(f"Returning rates for user's currencies: {currencies}.")
            return True, list(map(lambda x: round(x, 2), currencies_rates))

        logger.warning(f"Operation failed. Reason: {response.reason}")
        return False, str(response.reason)

    except requests.exceptions.RequestException as ex:
        logger.error(ex)
        return False, str(ex)


def get_data_via_api_stocks(stocks: list[str]) -> tuple:
    """Функция для получения текущего курса валют."""
    load_dotenv()

    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={os.getenv("API_KEY")}"

    logger.info("Trying to get stocks list.")
    try:
        response = requests.get(url)
        status_code = response.status_code

        if status_code == 200:
            logger.info("Stocks list got successfully.")
            stocks_data = response.json()
            stocks_prices = [i.get("price") for i in stocks_data for stock in stocks if i.get("symbol") == stock]
            logger.info(f"Returning prices of user's stocks: {stocks}.")
            return True, stocks_prices

        logger.warning(f"Operation failed. Reason: {response.reason}")
        return False, str(response.reason)

    except requests.exceptions.RequestException as ex:
        logger.error(ex)
        return False, str(ex)
