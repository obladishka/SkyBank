import pandas as pd


def get_data_from_xlsx(file_path: str) -> pd.DataFrame | None:
    """Функция для считывания инфы из excel-файла."""
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        print("Файл не найден. Проверьте правильность введенных данных.")
