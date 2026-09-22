"""Загрузка и сохранение данных в JSON."""

import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).parent / "data"


def load_json(filename: str) -> list[dict[str, Any]]:
    """Загрузить список словарей из JSON-файла."""
    path = DATA_DIR / filename
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создаётся пустой список.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения {filename}. Возвращается пустой список.")
        return []


def save_json(filename: str, data: list[dict[str, Any]]) -> None:
    """Сохранить список словарей в JSON-файл."""
    path = DATA_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
