from django.shortcuts import render

from storage import load_participants, load_trips


def index(request):
    trips = load_trips()
    participants = load_participants(trips)
    return render(request, "homepage/index.html", {
        "trip_count": len(trips),
        "participant_count": len(participants),
    })


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
