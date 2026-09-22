"""Функции работы с путешествиями."""

from typing import Any
from datetime import date


def add_trip(
    trips: list[dict[str, Any]],
    name: str,
    start_date: date,
    budget: float,
    min_participants: int,
) -> dict[str, Any]:
    """Добавить новое путешествие."""
    new_id = max((t["id"] for t in trips), default=0) + 1
    trip = {
        "id": new_id,
        "name": name,
        "start_date": start_date.isoformat(),
        "budget": budget,
        "min_participants": min_participants,
    }
    trips.append(trip)
    return trip


def find_trip_by_name(
    trips: list[dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    """Найти путешествия по подстроке названия."""
    query_lower = query.lower()
    return [t for t in trips if query_lower in t["name"].lower()]


def get_trip_by_id(
    trips: list[dict[str, Any]],
    trip_id: int,
) -> dict[str, Any] | None:
    """Найти путешествие по id."""
    for trip in trips:
        if trip["id"] == trip_id:
            return trip
    return None


def check_budget(trip: dict[str, Any], min_budget: float) -> bool:
    """Проверить, достаточен ли бюджет путешествия."""
    return trip["budget"] >= min_budget


def sort_trips_by_budget(
    trips: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Отсортировать путешествия по бюджету (по возрастанию)."""
    return sorted(trips, key=lambda t: t["budget"])
