from datetime import date
from trips import add_trip, find_trip_by_name, sort_trips_by_budget


def test_add_trip():
    trips = []
    trip = add_trip(trips, "Крым", date(2026, 7, 15), 40000, 3)
    assert len(trips) == 1
    assert trip["name"] == "Крым"
    assert trip["id"] == 1


def test_find_trip_by_name():
    trips = []
    add_trip(trips, "Крым 2026", date(2026, 7, 15), 40000, 3)
    add_trip(trips, "Сочи", date(2026, 8, 1), 25000, 4)
    found = find_trip_by_name(trips, "крым")
    assert len(found) == 1
    assert found[0]["name"] == "Крым 2026"


def test_sort_trips_by_budget():
    trips = []
    add_trip(trips, "A", date(2026, 1, 1), 50000, 3)
    add_trip(trips, "B", date(2026, 1, 1), 20000, 3)
    sorted_trips = sort_trips_by_budget(trips)
    assert sorted_trips[0]["budget"] == 20000
