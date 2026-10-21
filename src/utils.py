from pathlib import Path

import pandas as pd


def load_transactions(file_path: str | Path) -> pd.DataFrame:
    """Загружает банковские операции из Excel-файла."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    transactions = pd.read_excel(path)

    # Убираем переносы строк и лишние пробелы в названиях столбцов.
    transactions.columns = [
        " ".join(str(column).split()) for column in transactions.columns
    ]

    # Преобразуем дату операции в формат даты и времени.
    if "Дата операции" in transactions.columns:
        transactions["Дата операции"] = pd.to_datetime(
            transactions["Дата операции"],
            dayfirst=True,
            errors="coerce",
        )

    return transactions
