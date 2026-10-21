from datetime import datetime

import pandas as pd

from src.views import (
    get_card_summary,
    get_greeting,
    get_latest_transactions,
)


def test_get_greeting_morning():
    assert get_greeting(datetime(2025, 1, 1, 9, 0)) == "Доброе утро"


def test_get_greeting_day():
    assert get_greeting(datetime(2025, 1, 1, 14, 0)) == "Добрый день"


def test_get_greeting_evening():
    assert get_greeting(datetime(2025, 1, 1, 20, 0)) == "Добрый вечер"


def test_get_greeting_night():
    assert get_greeting(datetime(2025, 1, 1, 2, 0)) == "Доброй ночи"


def test_get_latest_transactions_sorts_by_amount():
    transactions = pd.DataFrame(
        {
            "Дата операции": [
                "2025-01-01",
                "2025-01-03",
                "2025-01-02",
            ],
            "Сумма платежа": [-100.0, 500.0, 250.0],
            "Категория": ["Продукты", "Техника", "Кафе"],
            "Описание": ["Покупка 1", "Покупка 2", "Покупка 3"],
        }
    )

    result = get_latest_transactions(transactions, limit=2)

    assert len(result) == 2
    assert result[0]["amount"] == 500.0
    assert result[1]["amount"] == 250.0
    assert result[0]["date"] == "03.01.2025"
    assert result[0]["category"] == "Техника"
    assert result[0]["description"] == "Покупка 2"
    assert set(result[0]) == {
        "date",
        "amount",
        "category",
        "description",
    }


def test_get_latest_transactions_empty_dataframe():
    result = get_latest_transactions(pd.DataFrame())

    assert result == []


def test_get_latest_transactions_zero_limit():
    transactions = pd.DataFrame({"Описание": ["Покупка"]})

    assert get_latest_transactions(transactions, limit=0) == []


def test_get_latest_transactions_negative_limit():
    transactions = pd.DataFrame({"Описание": ["Покупка"]})

    try:
        get_latest_transactions(transactions, limit=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалась ошибка ValueError")


def test_get_greeting_at_six_am():
    assert get_greeting(datetime(2025, 1, 1, 6, 0)) == "Доброе утро"


def test_get_greeting_at_five_am():
    assert get_greeting(datetime(2025, 1, 1, 5, 0)) == "Доброй ночи"


def test_get_card_summary():
    transactions = pd.DataFrame(
        {
            "Номер карты": ["*7197", "*7197", "*1234", "*1234"],
            "Сумма платежа": [-1000.0, -500.0, -250.0, 100.0],
        }
    )

    result = get_card_summary(transactions)

    assert result == [
        {
            "last_digits": "7197",
            "total_spent": 1500.0,
            "cashback": 15.0,
        },
        {
            "last_digits": "1234",
            "total_spent": 250.0,
            "cashback": 2.5,
        },
    ]


def test_get_card_summary_empty_dataframe():
    transactions = pd.DataFrame(
        {
            "Номер карты": [],
            "Сумма платежа": [],
        }
    )

    assert get_card_summary(transactions) == []
