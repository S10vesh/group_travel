"""Модель участника и функции работы с коллекцией участников."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .trips import Trip


class Participant:
    """Участник путешествия."""

    def __init__(self, participant_id: int, name: str, trip: "Trip") -> None:
        """Создать участника, связанного с объектом Trip."""
        self.id = participant_id
        self.name = name
        self.trip = trip

    def __str__(self) -> str:
        """Строковое представление участника."""
        return f"#{self.id} {self.name} (путешествие: {self.trip.name})"


def add_participant(
    participants: list[Participant],
    name: str,
    trip: "Trip",
) -> Participant:
    """Создать участника и добавить его в коллекцию."""
    new_id = max((p.id for p in participants), default=0) + 1
    participant = Participant(new_id, name, trip)
    participants.append(participant)
    return participant


def get_participants_by_trip(
    participants: list[Participant],
    trip: "Trip",
) -> list[Participant]:
    """Получить всех участников конкретного путешествия."""
    return [p for p in participants if p.trip.id == trip.id]


def count_participants(
    participants: list[Participant],
    trip: "Trip",
) -> int:
    """Посчитать количество участников путешествия."""
    return len(get_participants_by_trip(participants, trip))
