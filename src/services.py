import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "services.log")

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions_list(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Функция для формирования списка транзакций."""
    logger.info("Transforming df to dict")
    transactions = df.to_dict(orient="records")
    logger.info("Trying to convert data to the format needed")
    try:
        return [
            {
                "Дата операции": datetime.strftime(
                    datetime.strptime(transaction.get("Дата операции"), "%d.%m.%Y %H:%M:%S"), "%Y-%m-%d"
                ),
                "Сумма операции": transaction.get("Сумма операции"),
            }
            for transaction in transactions
        ]
    except Exception as ex:
        logger.error(ex)
        return []


def filter_by_month(month: str, transactions_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Функция для фильтрации транзакций по месяцу."""
    try:
        logger.info("Checking if input data is correct")
        datetime.strptime(month, "%Y-%m")
    except ValueError as ex:
        logger.error(ex)
        print("Неправильный формат даты. Введите дату в формате YYYY-MM")
        return []
    else:
        logger.info("Successful operation. Returning filtered list.")
        return [transaction for transaction in transactions_list if transaction.get("Дата операции")[:7] == month]


def round_to_limit(amount: float, limit: int) -> float:
    """Функция для округления суммы до заданного лимита."""
    logger.info(f"Checking if input data {amount}, {limit} is correct")
    if limit not in [10, 50, 100]:
        logger.warning(f"Incorrect limit: {limit}")
        print("Указан неверный лимит. Выберите лимит из возможных вариантов: 10, 50, 100")
        return 0.0
    logger.info("Returning result")
    return limit - amount % limit
