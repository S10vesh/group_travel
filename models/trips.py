"""Модель путешествия и функции работы с коллекцией путешествий."""

from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .groups import TravelGroup


class Trip:
    """Путешествие группы."""

    def __init__(
        self,
        trip_id: int,
        name: str,
        start_date: str,
        budget: float,
        min_participants: int,
    ) -> None:
        """Создать объект путешествия."""
        self.id = trip_id
        self.name = name
        self.start_date = start_date
        self.budget = budget
        self.min_participants = min_participants
        # Обратная связь: к какому TravelGroup относится путешествие.
        # Устанавливается в TravelGroup.__init__.
        self.group: "TravelGroup | None" = None

    def is_budget_enough(self, min_budget: float) -> bool:
        """Проверить, достаточен ли бюджет."""
        return self.budget >= min_budget

    def can_start(self, current_count: int) -> bool:
        """Хватает ли участников для старта планирования."""
        return current_count >= self.min_participants

    def __str__(self) -> str:
        """Строковое представление путешествия."""
        return (
            f"#{self.id} {self.name} | "
            f"дата: {self.start_date} | "
            f"бюджет: {self.budget} руб. | "
            f"мин. участников: {self.min_participants}"
        )


def add_trip(
    trips: list[Trip],
    name: str,
    start_date: date,
    budget: float,
    min_participants: int,
) -> Trip:
    """Создать объект Trip и добавить его в коллекцию."""
    new_id = max((t.id for t in trips), default=0) + 1
    trip = Trip(
        trip_id=new_id,
        name=name,
        start_date=start_date.isoformat(),
        budget=budget,
        min_participants=min_participants,
    )
    trips.append(trip)
    return trip


def find_trip_by_name(trips: list[Trip], query: str) -> list[Trip]:
    """Найти путешествия по подстроке названия."""
    q = query.lower()
    return [t for t in trips if q in t.name.lower()]


def get_trip_by_id(trips: list[Trip], trip_id: int) -> Trip | None:
    """Найти путешествие по id."""
    for t in trips:
        if t.id == trip_id:
            return t
    return None


def sort_trips_by_budget(trips: list[Trip]) -> list[Trip]:
    """Отсортировать путешествия по бюджету (по возрастанию)."""
    return sorted(trips, key=lambda t: t.budget)
