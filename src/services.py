from datetime import datetime
from typing import Any

import pandas as pd


def get_transactions_list(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Функция для формирования списка транзакций."""
    transactions = df.to_dict(orient="records")
    return [
        {
            "Дата операции": datetime.strftime(
                datetime.strptime(transaction.get("Дата операции"), "%d.%m.%Y %H:%M:%S"), "%Y-%m-%d"
            ),
            "Сумма операции": transaction.get("Сумма операции"),
        }
        for transaction in transactions
    ]
