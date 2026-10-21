from datetime import datetime

import pandas as pd

from src.decorators import save_report


@save_report()
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    report_date: datetime | None = None,
) -> pd.DataFrame:
    """Формирует отчёт о расходах по категории за последние три месяца."""
    if not category.strip():
        raise ValueError("Название категории не может быть пустым")

    required_columns = {"Дата операции", "Сумма платежа", "Категория"}
    missing_columns = required_columns - set(transactions.columns)

    if missing_columns:
        missing_names = ", ".join(sorted(missing_columns))
        raise ValueError(f"Отсутствуют столбцы: {missing_names}")

    if report_date is None:
        end_date = pd.Timestamp.now()
    else:
        end_date = pd.Timestamp(report_date)

    start_date = end_date - pd.DateOffset(months=3)

    result = transactions.copy()
    result["Дата операции"] = pd.to_datetime(
        result["Дата операции"],
        errors="coerce",
    )
    result["Сумма платежа"] = pd.to_numeric(
        result["Сумма платежа"],
        errors="coerce",
    )

    category_matches = (
        result["Категория"].fillna("").astype(str).str.strip().str.casefold()
        == category.strip().casefold()
    )

    date_matches = (result["Дата операции"] >= start_date) & (
        result["Дата операции"] <= end_date
    )

    expense_matches = result["Сумма платежа"] < 0

    report = result.loc[category_matches & date_matches & expense_matches].copy()

    report["Сумма платежа"] = report["Сумма платежа"].abs()

    return report.reset_index(drop=True)
