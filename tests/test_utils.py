import pandas as pd
import pytest

from src.utils import load_transactions


def test_load_transactions_reads_excel(tmp_path):
    """Проверяет загрузку Excel-файла."""
    file_path = tmp_path / "operations.xlsx"

    data = pd.DataFrame(
        {
            "Дата операции": ["15.01.2025 12:30:00"],
            "Сумма операции\n": [-150.0],
            "Категория": ["Супермаркеты"],
        }
    )
    data.to_excel(file_path, index=False)

    result = load_transactions(file_path)

    assert len(result) == 1
    assert "Сумма операции" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["Дата операции"])


def test_load_transactions_file_not_found():
    """Проверяет ошибку при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        load_transactions("data/nonexistent.xlsx")
