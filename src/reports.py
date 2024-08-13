import json
import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "reports.log")

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


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

        except json.JSONDecodeError as ex:
            logger.error(ex)

    except ValueError as ex:
        logger.error(ex)
        print("Неправильный формат даты. Введите дату в формате DD.MM.YY HH:MM:SS")
