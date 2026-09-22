"""Функции работы с участниками."""

from typing import Any


def add_participant(
    participants: list[dict[str, Any]],
    name: str,
    trip_id: int,
) -> dict[str, Any]:
    """Добавить участника к путешествию."""
    new_id = max((p["id"] for p in participants), default=0) + 1
    participant = {
        "id": new_id,
        "name": name,
        "trip_id": trip_id,
    }
    participants.append(participant)
    return participant


def get_participants_by_trip(
    participants: list[dict[str, Any]],
    trip_id: int,
) -> list[dict[str, Any]]:
    """Получить всех участников конкретного путешествия."""
    return [p for p in participants if p["trip_id"] == trip_id]


def count_participants(
    participants: list[dict[str, Any]],
    trip_id: int,
) -> int:
    """Посчитать количество участников путешествия."""
    return len(get_participants_by_trip(participants, trip_id))


def can_start_planning(
    trip: dict[str, Any],
    participants: list[dict[str, Any]],
) -> bool:
    """Проверить, можно ли начинать планирование."""
    current = count_participants(participants, trip["id"])
    return current >= trip["min_participants"]
