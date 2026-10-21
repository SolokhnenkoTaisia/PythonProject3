import pandas as pd
import pytest

from src.services import simple_search


@pytest.fixture
def transactions():
    return pd.DataFrame(
        {
            "Категория": ["Продукты", "Кафе", "Переводы", None],
            "Описание": [
                "Магазин у дома",
                "Кофейня",
                "Перевод Ивану",
                "Не указано",
            ],
        }
    )


def test_search_by_category_case_insensitive(transactions):
    result = simple_search("КАФЕ", transactions)

    assert len(result) == 1
    assert result[0]["Категория"] == "Кафе"


def test_search_by_description(transactions):
    result = simple_search("магазин", transactions)

    assert len(result) == 1
    assert result[0]["Описание"] == "Магазин у дома"


def test_search_returns_all_matches(transactions):
    result = simple_search("перевод", transactions)

    assert len(result) == 1
    assert result[0]["Категория"] == "Переводы"


def test_search_empty_query(transactions):
    assert simple_search("", transactions) == []
    assert simple_search("   ", transactions) == []


def test_search_without_matches(transactions):
    assert simple_search("самолёт", transactions) == []


def test_search_empty_dataframe():
    empty = pd.DataFrame(columns=["Категория", "Описание"])

    assert simple_search("кафе", empty) == []


def test_search_missing_columns():
    invalid = pd.DataFrame({"Название": ["Кафе"]})

    with pytest.raises(ValueError, match="отсутствуют столбцы"):
        simple_search("кафе", invalid)
