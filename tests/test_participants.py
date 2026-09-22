from datetime import date
from trips import add_trip
from participants import add_participant, can_start_planning


def test_add_participant():
    participants = []
    p = add_participant(participants, "Иван", 1)
    assert len(participants) == 1
    assert p["name"] == "Иван"


def test_can_start_planning():
    trips = []
    trip = add_trip(trips, "Крым", date(2026, 7, 15), 40000, 3)
    participants = []
    add_participant(participants, "Иван", trip["id"])
    add_participant(participants, "Мария", trip["id"])
    assert not can_start_planning(trip, participants)
    add_participant(participants, "Алексей", trip["id"])
    assert can_start_planning(trip, participants)
