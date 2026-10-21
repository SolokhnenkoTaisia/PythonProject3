# PythonProject3 — Анализ банковских транзакций

Учебный проект курсовой работы на Python 3.12 для обработки и анализа банковских транзакций.

## Возможности

- **Главная страница:** приветствие в зависимости от времени суток, сводка расходов по картам, расчёт кешбэка и отображение пяти крупнейших транзакций.
- **Курсы валют:** получение курсов валют с помощью внешнего API.
- **Цены акций:** получение котировок акций через Alpha Vantage.
- **Поиск транзакций:** поиск по категории и описанию без учёта регистра.
- **Отчёт по категории:** формирование отчёта о расходах по выбранной категории за последние три месяца с сохранением результата в JSON.

## Используемые технологии

- Python 3.12
- Poetry
- pandas
- openpyxl
- requests
- python-dotenv
- pytest
- mypy, black, isort, flake8

## Структура проекта

- `src/main.py` — формирование данных главной страницы.
- `src/views.py` — приветствие, сводка по картам и последние транзакции.
- `src/external_api.py` — получение курсов валют и цен акций.
- `src/services.py` — поиск транзакций.
- `src/reports.py` — отчёт по расходам на выбранную категорию.
- `src/decorators.py` — декоратор сохранения отчётов.
- `src/utils.py` — загрузка данных из Excel.
- `tests/` — автоматические тесты.
- `data/` — исходные данные.
- `user_settings.json` — настройки валют и акций.
- `.env_template` — шаблон конфигурации для API-ключа.

## Установка и настройка

1. Установите Python 3.12 и Poetry.
2. Установите зависимости:

   ```bash
   poetry install
   ```

3. Создайте файл `.env` на основе `.env_template` и укажите API-ключ Alpha Vantage:

   ```text
   ALPHA_VANTAGE_API_KEY=ваш_ключ
   ```

4. Проверьте, что файл `data/operations.xlsx` существует и содержит данные транзакций.

## Использование функций проекта

Функции проекта можно вызывать из Python-кода.

### Загрузка транзакций и формирование главной страницы

```python
from datetime import datetime

from src.main import main
from src.utils import load_transactions

transactions = load_transactions("data/operations.xlsx")

result = main(
    "2021-12-31 23:59:59",
    transactions,
)

print(result)
```

Для получения курсов валют и котировок акций необходим действующий API-ключ и доступ к внешним сервисам.

### Поиск транзакций

```python
from src.services import simple_search
from src.utils import load_transactions

transactions = load_transactions("data/operations.xlsx")

result = simple_search("супермаркеты", transactions)
print(result)
```

### Формирование отчёта по категории

```python
from src.reports import spending_by_category
from src.utils import load_transactions

transactions = load_transactions("data/operations.xlsx")

result = spending_by_category(
    transactions,
    "Супермаркеты",
)

print(result)
```

Результат отчёта сохраняется в JSON с помощью декоратора.

## Запуск тестов

```bash
poetry run pytest
```

## Проверки качества кода

```bash
poetry run mypy src
poetry run black --check src tests
poetry run isort --check-only src tests
poetry run flake8 src tests
```

## Конфигурация и ограничения API

В `user_settings.json` указываются валюты и тикеры акций, которые необходимо получать через API.

Внешние API могут ограничивать частоту запросов или временно не предоставлять данные. В таких случаях отдельные курсы или котировки могут быть недоступны.

**Важно:** файл `.env` с личным API-ключом не следует добавлять в Git или публиковать на GitHub.
