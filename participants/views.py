from django.shortcuts import render

from storage import load_participants, load_trips


def participant_list(request):
    participants = load_participants(load_trips())
    return render(request, "participants/participant_list.html", {
        "participants": participants,
    })


def participant_detail(request, participant_id):
    participants = load_participants(load_trips())
    participant = next(
        (p for p in participants if p.id == participant_id), None,
    )
    if participant is None:
        return render(request, "404.html", {
            "error_title": "Участник не найден",
        }, status=404)
    return render(request, "participants/participant_detail.html", {
        "participant": participant,
    })
