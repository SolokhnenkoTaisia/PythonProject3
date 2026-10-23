import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from src.reports import spending_by_category
from src.services import simple_search
from src.utils import load_transactions

from src.external_api import get_currency_rates, get_stock_prices
from src.views import (
    get_card_summary,
    get_greeting,
    get_latest_transactions,
)


def main(
    date_time: str,
    transactions: pd.DataFrame,
) -> dict[str, Any]:
    """Формирует данные для главной страницы приложения."""
    current_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

    month_start = current_time.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    data = transactions.copy()
    data["Дата операции"] = pd.to_datetime(
        data["Дата операции"],
        errors="coerce",
    )

    data = data.loc[
        (data["Дата операции"] >= month_start) & (data["Дата операции"] <= current_time)
    ].copy()

    settings_path = Path("user_settings.json")

    with settings_path.open("r", encoding="utf-8") as file:
        settings = json.load(file)

    currency_rates = get_currency_rates(settings["user_currencies"])
    stock_prices = get_stock_prices(settings["user_stocks"])

    return {
        "greeting": get_greeting(current_time),
        "cards": get_card_summary(data),
        "top_transactions": get_latest_transactions(data, limit=5),
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

if __name__ == "__main__":
    transactions = load_transactions("data/operations.xlsx")

    # Берём дату последней операции из файла.
    latest_date = transactions["Дата операции"].max()
    date_time = latest_date.strftime("%Y-%m-%d %H:%M:%S")

    # Главная страница приложения.
    print("Главная страница:")
    print(main(date_time, transactions))

    # Поиск транзакций.
    print("\nРезультаты поиска:")
    print(simple_search("супермаркеты", transactions))

    # Отчёт по расходам в категории.
    print("\nОтчёт по категории:")
    print(
        spending_by_category(
            transactions,
            "Супермаркеты",
            report_date=latest_date.to_pydatetime(),
        )
    )
