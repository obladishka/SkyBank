import io
import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Optional

import pandas as pd

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "reports.log")

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def write_to_file(my_file: str = None) -> Any:
    """Декоратор для записи в файл результата, возвращаемого функцией для формирования отчета."""

    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            result = func(*args, **kwargs)

            if not my_file or my_file[-4:] == "json":
                file_name = os.path.join(file_path, "report.json")
                with open(file_name, "w", encoding="utf-8") as output_file:
                    new_result = json.loads(result)
                    json.dump(new_result, output_file, ensure_ascii=False, indent=4)

            elif my_file[-4:] == ".csv":
                file_name = os.path.join(file_path, my_file)
                pd.read_json(io.StringIO(result)).to_csv(file_name, index=False)

            else:
                file_name = os.path.join(file_path, my_file)
                pd.read_json(io.StringIO(result)).to_excel(file_name, index=False)

        return wrapper

    return my_decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция для формирования отчета."""

    try:
        logger.info("Getting time diapason")
        end_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S") if date else datetime.now()
        start_date = end_date - timedelta(days=90)

        logger.info(f"Filtering transactions between {start_date} & {end_date}")
        transactions["date"] = transactions["Дата операции"].map(
            lambda x: datetime.strptime(str(x), "%d.%m.%Y %H:%M:%S")
        )
        filtered_transactions = transactions[(transactions["date"] >= start_date) & (transactions["date"] <= end_date)]

        logger.info("Transforming result into dict")
        result = (
            filtered_transactions.loc[transactions["Категория"] == category].iloc[:, :-1].to_dict(orient="records")
        )
        try:
            logger.info("Trying to serialize results")
            return json.dumps(result, ensure_ascii=False, indent=4)

        except Exception as ex:
            logger.error(ex)

    except ValueError as ex:
        logger.error(ex)
        print("Неправильный формат даты. Введите дату в формате DD.MM.YY HH:MM:SS")
