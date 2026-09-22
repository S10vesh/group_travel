from models import Trip
from models.participants import add_participant
from models.groups import TravelGroup


def test_group_is_not_ready():
    trip = Trip(1, "Крым", "2026-07-15", 40000, 3)
    group = TravelGroup(trip)
    assert not group.is_ready()
    assert group.count() == 0


def test_group_becomes_ready():
    trip = Trip(1, "Крым", "2026-07-15", 40000, 3)
    group = TravelGroup(trip)
    participants = []
    for name in ("Иван", "Мария", "Алексей"):
        p = add_participant(participants, name, trip)
        group.add_participant(p)
    assert group.count() == 3
    assert group.is_ready()
