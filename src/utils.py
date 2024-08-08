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


def get_data_from_user() -> None:
    """Функция для задания пользовательских настроек."""

    file_path = os.path.dirname(os.path.dirname(__file__))

    # Получаем список кодов существующих валют
    try:
        with open(os.path.join(file_path, "data", "currencies.json"), "r", encoding="utf-8") as cf:
            try:
                currencies = json.load(cf)
                codes = [currency.get("code") for currency in currencies]
            except json.JSONDecodeError:
                codes = []
    except FileNotFoundError:
        print("Файл не найден. Проверьте правильность введенных данных.")
        codes = []

    # Получаем список тикеров компаний S&P 500
    try:
        with open(os.path.join(file_path, "data", "sandp500.json"), "r", encoding="utf-8") as sf:
            try:
                companies = json.load(sf)
                symbols = [company.get("tickerSymbol") for company in companies]
            except json.JSONDecodeError:
                symbols = []
    except FileNotFoundError:
        print("Файл не найден. Проверьте правильность введенных данных.")
        symbols = []

    # Получаем данные от пользователя и проверяем их корректность
    user_currencies = (
        input("Введите ISO-коды валют, для отображения на главной странице (через запятую или пробел): ")
        .upper()
        .replace(",", " ")
        .replace("  ", " ")
        .split()
    )

    while any(currency not in codes for currency in user_currencies):
        print("Введенные валюты не найдены. Проверьте правильность введенных данных.")
        user_currencies = (
            input("Введите ISO-коды валют, для отображения на главной странице (через запятую или пробел): ")
            .upper()
            .replace(",", " ")
            .replace("  ", " ")
            .split()
        )

    user_stocks = (
        input(
            "Введите тикеры акций компаний S&P 500, для отображения на главной странице (через запятую или пробел): "
        )
        .upper()
        .replace(",", " ")
        .replace("  ", " ")
        .split()
    )

    while any(stock not in symbols for stock in user_stocks):
        print("Введенные тикеры не найдены. Проверьте правильность введенных данных.")
        user_stocks = (
            input(
                "Введите тикеры акций компаний S&P 500, для отображения на главной странице\
                 (через запятую или пробел): "
            )
            .upper()
            .replace(",", " ")
            .replace("  ", " ")
            .split()
        )

    # Вносим пользовательские данные в файл
    with open(os.path.join(file_path, "user_settings.json"), "w", encoding="utf-8") as of:
        user_settings = {"user_currencies": user_currencies, "user_stocks": user_stocks}
        json.dump(user_settings, of)
