from datetime import date

from django.shortcuts import render

from models import TravelGroup
from models.participants import get_participants_by_trip
from models.trips import get_trip_by_id
from storage import load_participants, load_trips


def trip_list(request):
    return render(request, "trips/trip_list.html", {"trips": load_trips()})


def trip_detail(request, trip_id):
    trips = load_trips()
    trip = get_trip_by_id(trips, trip_id)
    if trip is None:
        return render(request, "404.html", {
            "error_title": "Путешествие не найдено",
        }, status=404)
    group = TravelGroup(trip)
    participants = get_participants_by_trip(load_participants(trips), trip)
    for participant in participants:
        group.add_participant(participant)
    try:
        start_date = date.fromisoformat(trip.start_date)
    except (ValueError, TypeError):
        start_date = None
    return render(request, "trips/trip_detail.html", {
        "trip": trip, "group": group, "start_date": start_date,
    })
