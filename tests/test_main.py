from unittest.mock import patch

import pandas as pd

from src.main import main


def test_main_filters_transactions_by_month_and_date():
    transactions = pd.DataFrame(
        {
            "Дата операции": [
                "2025-01-15",
                "2025-02-10",
                "2025-02-20",
                "2025-03-01",
            ],
            "Номер карты": ["*1111", "*1111", "*2222", "*3333"],
            "Сумма платежа": [-100.0, -200.0, -300.0, -400.0],
            "Категория": [
                "Кафе",
                "Продукты",
                "Техника",
                "Магазины",
            ],
            "Описание": [
                "Покупка в январе",
                "Покупка в феврале",
                "Покупка после даты",
                "Покупка в марте",
            ],
        }
    )

    with (
        patch(
            "src.main.get_currency_rates",
            return_value=[
                {"currency": "USD", "rate": 1.1},
                {"currency": "EUR", "rate": 1.0},
            ],
        ),
        patch("src.main.get_stock_prices", return_value=[]),
    ):
        result = main("2025-02-15 14:30:00", transactions)

    assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) == 1
    assert result["cards"][0]["last_digits"] == "1111"
    assert result["cards"][0]["total_spent"] == 200.0
    assert result["cards"][0]["cashback"] == 2.0
    assert len(result["top_transactions"]) == 1
    assert result["top_transactions"][0]["description"] == "Покупка в феврале"
    assert len(result["currency_rates"]) == 2
    assert {item["currency"] for item in result["currency_rates"]} == {
        "USD",
        "EUR",
    }
    assert all(item["rate"] > 0 for item in result["currency_rates"])
    assert result["stock_prices"] == []
