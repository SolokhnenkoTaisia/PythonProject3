import json
from functools import wraps
from pathlib import Path
from typing import Any, Callable


def save_report(
    default_filename: str = "report.json",
) -> Callable[..., Any]:
    """Сохраняет результат функции-отчёта в JSON-файл."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(
            *args: Any,
            filename: str | Path | None = None,
            **kwargs: Any,
        ) -> Any:
            result = func(*args, **kwargs)

            output_path = Path(filename or default_filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if hasattr(result, "to_dict"):
                data = result.to_dict(orient="records")
            else:
                data = result

            with output_path.open("w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    default=str,
                )

            return result

        return wrapper

    return decorator
