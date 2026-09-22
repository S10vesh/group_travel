"""Класс TravelGroup: путешествие + его участники."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .trips import Trip
    from .participants import Participant


class TravelGroup:
    """Группа: путешествие и его участники."""

    def __init__(self, trip: "Trip") -> None:
        """Создать группу для заданного путешествия."""
        self.trip = trip
        self.participants: list["Participant"] = []

    def add_participant(self, participant: "Participant") -> None:
        """Добавить участника в группу."""
        self.participants.append(participant)

    def count(self) -> int:
        """Количество участников в группе."""
        return len(self.participants)

    def is_ready(self) -> bool:
        """Готова ли группа к планированию."""
        return self.trip.can_start(self.count())

    def __str__(self) -> str:
        """Строковое представление группы."""
        status = "готова" if self.is_ready() else "не готова"
        return (
            f"Группа «{self.trip.name}»: "
            f"{self.count()} из {self.trip.min_participants} — {status}"
        )
