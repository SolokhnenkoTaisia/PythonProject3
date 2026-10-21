import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

CURRENCY_API_URL = "https://api.frankfurter.dev/v2/rate/eur"


def get_currency_rates(
    currencies: list[str],
) -> list[dict[str, Any]]:
    """Получает курсы валют относительно евро."""
    rates = []

    for currency in currencies:
        if currency.upper() == "EUR":
            rates.append({"currency": "EUR", "rate": 1.0})
            continue

        try:
            response = requests.get(
                f"{CURRENCY_API_URL}/{currency.lower()}",
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            rate = float(data["rate"])
            if rate > 0:
                rates.append({"currency": currency.upper(), "rate": rate})
        except (requests.RequestException, ValueError, KeyError) as error:
            logger.warning(
                "Не удалось получить курс %s: %s",
                currency,
                error,
            )

    return rates


def get_stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """Получает цены акций через Alpha Vantage."""
    load_dotenv()
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        logger.warning("Не задан API-ключ Alpha Vantage")
        return []

    prices: list[dict[str, Any]] = []

    for stock in stocks:
        try:
            response = requests.get(
                "https://www.alphavantage.co/query",
                params={
                    "function": "GLOBAL_QUOTE",
                    "symbol": stock,
                    "apikey": api_key,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            quote = data.get("Global Quote", {})
            price = float(quote.get("05. price", 0))

            if price > 0:
                prices.append({"stock": stock, "price": price})
            else:
                logger.warning(
                    "Цена для %s недоступна: %s",
                    stock,
                    data.get("Note")
                    or data.get("Information")
                    or data.get("Error Message", "нет данных"),
                )

        except (
            requests.RequestException,
            ValueError,
            TypeError,
        ) as error:
            logger.warning(
                "Не удалось получить цену %s: %s",
                stock,
                error,
            )

    return prices
