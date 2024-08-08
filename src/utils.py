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
