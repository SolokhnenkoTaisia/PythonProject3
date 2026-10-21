import json
from datetime import datetime

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category():
    transactions = pd.DataFrame(
        {
            "Дата операции": [
                "2026-08-10",
                "2026-09-15",
                "2026-10-20",
                "2026-10-21",
                "2026-05-01",
            ],
            "Сумма платежа": [
                -500,
                -300,
                2000,
                -100,
                -700,
            ],
            "Категория": [
                "Кафе",
                "Кафе",
                "Кафе",
                "Продукты",
                "Кафе",
            ],
        }
    )

    report = spending_by_category(
        transactions,
        "Кафе",
        datetime(2026, 10, 21),
    )

    assert len(report) == 2
    assert report["Сумма платежа"].tolist() == [500, 300]


def test_report_saves_to_default_file(tmp_path, monkeypatch):
    transactions = pd.DataFrame(
        {
            "Дата операции": ["2026-10-10"],
            "Сумма платежа": [-500],
            "Категория": ["Кафе"],
        }
    )

    monkeypatch.chdir(tmp_path)

    spending_by_category(
        transactions,
        "Кафе",
        datetime(2026, 10, 21),
    )

    report_path = tmp_path / "report.json"

    assert report_path.exists()

    with report_path.open(encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]["Категория"] == "Кафе"


def test_report_saves_to_custom_file(tmp_path):
    transactions = pd.DataFrame(
        {
            "Дата операции": ["2026-10-10"],
            "Сумма платежа": [-500],
            "Категория": ["Кафе"],
        }
    )

    report_path = tmp_path / "cafe_report.json"

    spending_by_category(
        transactions,
        "Кафе",
        datetime(2026, 10, 21),
        filename=report_path,
    )

    assert report_path.exists()
