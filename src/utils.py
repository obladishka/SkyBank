import json
import os

import numpy as np
import pandas as pd


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
