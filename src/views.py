from datetime import datetime
from typing import Any

import pandas as pd


def get_greeting(current_time: datetime | None = None) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    now = current_time or datetime.now()
    hour = now.hour

    if 6 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 18:
        return "Добрый день"
    if 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_latest_transactions(
    transactions: pd.DataFrame,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Возвращает транзакции с наибольшими суммами платежей."""
    if limit < 0:
        raise ValueError("Количество операций не может быть отрицательным")

    if transactions.empty or limit == 0:
        return []

    required_columns = [
        "Дата операции",
        "Сумма платежа",
        "Категория",
        "Описание",
    ]

    missing_columns = [
        column for column in required_columns if column not in transactions.columns
    ]
    if missing_columns:
        missing_names = ", ".join(missing_columns)
        raise ValueError(f"В таблице отсутствуют столбцы: {missing_names}")

    result = transactions[required_columns].copy()
    result["Сумма платежа"] = pd.to_numeric(
        result["Сумма платежа"],
        errors="coerce",
    )
    result = result.dropna(subset=["Сумма платежа"])
    result = result.sort_values(
        "Сумма платежа",
        ascending=False,
    ).head(limit)

    result["Дата операции"] = pd.to_datetime(
        result["Дата операции"],
        errors="coerce",
        dayfirst=False,
    ).dt.strftime("%d.%m.%Y")

    result = result.rename(
        columns={
            "Дата операции": "date",
            "Сумма платежа": "amount",
            "Категория": "category",
            "Описание": "description",
        }
    )

    result = result.astype(object).where(pd.notna(result), None)
    records = result.to_dict(orient="records")
    return [{str(key): value for key, value in record.items()} for record in records]


def get_card_summary(
    transactions: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Возвращает расходы и кешбэк по каждой банковской карте."""
    required_columns = ["Номер карты", "Сумма платежа"]

    missing_columns = [
        column for column in required_columns if column not in transactions.columns
    ]
    if missing_columns:
        missing_names = ", ".join(missing_columns)
        raise ValueError(f"В таблице отсутствуют столбцы: {missing_names}")

    if transactions.empty:
        return []

    result = transactions[required_columns].copy()
    result["Номер карты"] = (
        result["Номер карты"]
        .astype("string")
        .str.extract(
            r"(\d{4})$",
            expand=False,
        )
    )
    result["Сумма платежа"] = pd.to_numeric(
        result["Сумма платежа"],
        errors="coerce",
    )

    # В исходной таблице расходы обозначены отрицательными суммами.
    result["Расходы"] = (-result["Сумма платежа"]).where(
        result["Сумма платежа"] < 0,
        0,
    )

    result = result.dropna(subset=["Номер карты", "Сумма платежа"])
    grouped = result.groupby("Номер карты", sort=False)["Расходы"].sum()

    cards = []
    for last_digits, total_spent in grouped.items():
        total_spent = round(float(total_spent), 2)
        cards.append(
            {
                "last_digits": str(last_digits),
                "total_spent": total_spent,
                "cashback": round(total_spent / 100, 2),
            }
        )

    return cards
