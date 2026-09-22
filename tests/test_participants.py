from models import Trip, Participant
from models.participants import (
    add_participant, count_participants,
)


def test_participant_links_to_trip():
    trip = Trip(1, "Крым", "2026-07-15", 40000, 3)
    p = Participant(1, "Иван", trip)
    assert p.trip is trip
    assert p.trip.name == "Крым"


def test_add_participant():
    trip = Trip(1, "Крым", "2026-07-15", 40000, 3)
    participants = []
    p = add_participant(participants, "Иван", trip)
    assert len(participants) == 1
    assert p.name == "Иван"


def test_count_participants():
    trip = Trip(1, "Крым", "2026-07-15", 40000, 3)
    participants = []
    add_participant(participants, "Иван", trip)
    add_participant(participants, "Мария", trip)
    assert count_participants(participants, trip) == 2
