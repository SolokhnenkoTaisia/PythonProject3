import json
from typing import Any

import pandas as pd


def simple_search(
    query: str,
    transactions: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Ищет транзакции по категории или описанию."""
    query = query.strip().casefold()

    if not query or transactions.empty:
        return []

    required_columns = {"Категория", "Описание"}
    missing_columns = required_columns - set(transactions.columns)

    if missing_columns:
        missing_names = ", ".join(sorted(missing_columns))
        raise ValueError(f"В таблице отсутствуют столбцы: {missing_names}")

    category_matches = (
        transactions["Категория"]
        .fillna("")
        .astype(str)
        .str.casefold()
        .str.contains(query, regex=False)
    )

    description_matches = (
        transactions["Описание"]
        .fillna("")
        .astype(str)
        .str.casefold()
        .str.contains(query, regex=False)
    )

    matches = transactions.loc[category_matches | description_matches]

    result: list[dict[str, Any]] = json.loads(
        matches.to_json(
            orient="records",
            date_format="iso",
            force_ascii=False,
        )
    )
    return result
