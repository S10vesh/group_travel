"""Загрузка и сохранение данных в JSON с преобразованием в объекты."""

import json
from pathlib import Path
from typing import Any

from models import Trip, Participant

DATA_DIR = Path(__file__).parent / "data"


def load_trips(filename: str = "trips.json") -> list[Trip]:
    """Загрузить путешествия из JSON в виде объектов Trip."""
    data = _read_json(filename)
    return [
        Trip(
            trip_id=item["id"],
            name=item["name"],
            start_date=item["start_date"],
            budget=item["budget"],
            min_participants=item["min_participants"],
        )
        for item in data
    ]


def save_trips(trips: list[Trip], filename: str = "trips.json") -> None:
    """Сохранить объекты Trip в JSON."""
    data = [
        {
            "id": t.id,
            "name": t.name,
            "start_date": t.start_date,
            "budget": t.budget,
            "min_participants": t.min_participants,
        }
        for t in trips
    ]
    _write_json(filename, data)


def load_participants(
    trips: list[Trip],
    filename: str = "participants.json",
) -> list[Participant]:
    """Загрузить участников; связать каждого с объектом Trip."""
    data = _read_json(filename)
    result: list[Participant] = []
    for item in data:
        trip = next((t for t in trips if t.id == item["trip_id"]), None)
        if trip is None:
            continue
        result.append(
            Participant(
                participant_id=item["id"],
                name=item["name"],
                trip=trip,
            )
        )
    return result


def save_participants(
    participants: list[Participant],
    filename: str = "participants.json",
) -> None:
    """Сохранить участников в JSON (храним trip_id, а не объект)."""
    data = [
        {"id": p.id, "name": p.name, "trip_id": p.trip.id}
        for p in participants
    ]
    _write_json(filename, data)


def _read_json(filename: str) -> list[dict[str, Any]]:
    """Прочитать список словарей из JSON."""
    path = DATA_DIR / filename
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создан пустой список.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения {filename}. Возвращён пустой список.")
        return []


def _write_json(filename: str, data: list[dict[str, Any]]) -> None:
    """Записать список словарей в JSON."""
    path = DATA_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
