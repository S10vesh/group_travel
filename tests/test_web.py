"""Проверки веб-интерфейса без базы данных и записи в рабочие JSON."""
import os
import json
from pathlib import Path
from unittest.mock import patch

import django
import pytest
from django.contrib.staticfiles import finders
from django.test import Client, override_settings
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "group_travel.settings")
django.setup()

from models import Participant, Trip  # noqa: E402
from storage import load_participants, load_trips  # noqa: E402


@pytest.fixture
def client():
    with override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"]):
        yield Client()


@pytest.mark.parametrize("url", ["/", "/trips/", "/participants/"])
def test_main_pages(client, url):
    response = client.get(url)
    assert response.status_code == 200
    assert "Group Travel" in response.content.decode()


def test_actual_json_records(client):
    trips = load_trips()
    participants = load_participants(trips)
    for trip in trips:
        response = client.get(reverse("trips:detail", args=[trip.id]))
        assert response.status_code == 200
    for participant in participants:
        response = client.get(
            reverse("participants:detail", args=[participant.id]),
        )
        assert response.status_code == 200
        assert reverse("trips:detail", args=[participant.trip.id]) in (
            response.content.decode()
        )


@pytest.mark.parametrize("url", [
    "/trips/999999/", "/participants/999999/", "/nonexistent/",
    "/trips/abc/", "/participants/-1/",
])
def test_custom_404(client, url):
    response = client.get(url)
    assert response.status_code == 404
    assert "ОШИБКА 404" in response.content.decode()
    assert 'href="/"' in response.content.decode()


@pytest.mark.parametrize("module,url,message", [
    ("trips", "/trips/", "Путешествий пока нет"),
    ("participants", "/participants/", "Участников пока нет"),
])
def test_empty_lists(client, module, url, message):
    with patch(f"{module}.views.load_trips", return_value=[]):
        response = client.get(url)
    assert response.status_code == 200
    assert message in response.content.decode()


@pytest.mark.parametrize("count,expected", [
    (0, "Набираем участников"),
    (2, "Группа готова к планированию"),
])
def test_group_status_and_links(client, count, expected):
    trip = Trip(42, "Алтай", "2026-12-01", 50000, 2)
    people = [Participant(i, f"Участник {i}", trip) for i in range(count)]
    with patch("trips.views.load_trips", return_value=[trip]), patch(
        "trips.views.load_participants", return_value=people,
    ):
        response = client.get("/trips/42/")
    html = response.content.decode()
    assert response.status_code == 200
    assert expected in html
    assert "01.12.2026" in html
    for person in people:
        assert reverse("participants:detail", args=[person.id]) in html
    if not count:
        assert "В этой поездке пока нет участников" in html


def test_names_are_escaped(client):
    trip = Trip(42, '<script>alert("x")</script>', "2026-12-01", 50, 2)
    with patch("trips.views.load_trips", return_value=[trip]), patch(
        "trips.views.load_participants", return_value=[],
    ):
        html = client.get("/trips/42/").content.decode()
    assert '<script>alert(' not in html
    assert "&lt;script&gt;" in html


@pytest.mark.parametrize("asset", [
    "homepage/css/style.css", "homepage/js/main.js", "homepage/img/logo.svg",
])
def test_static_assets(client, asset):
    assert finders.find(asset)
    assert f"/static/{asset}" in client.get("/").content.decode()


@pytest.mark.parametrize("url", [
    "/", "/trips/", "/trips/1/", "/participants/", "/participants/1/",
])
def test_russian_text_encoding(client, url):
    html = client.get(url).content.decode("utf-8")
    # Unicode escapes keep the expected text independent of shell encoding.
    expected = (
        "\u041f\u0443\u0442\u0435\u0448"
        "\u0435\u0441\u0442\u0432\u0438\u044f"
    )
    assert expected in html
    assert "???" not in html
    assert "\ufffd" not in html


def test_readme_encoding():
    readme = Path(__file__).resolve().parents[1] / "README.md"
    text = readme.read_text(encoding="utf-8")
    assert "???" not in text
    assert "\ufffd" not in text


@pytest.mark.parametrize("debug", [True, False])
@pytest.mark.parametrize("url,message", [
    ("/trips/999999/", "Путешествие не найдено"),
    ("/participants/999999/", "Участник не найден"),
])
def test_missing_record_message(client, debug, url, message):
    with override_settings(DEBUG=debug):
        response = client.get(url)
    assert response.status_code == 404
    assert message in response.content.decode("utf-8")


def test_json_is_reloaded_without_changing_project_data(client, tmp_path):
    trip = {
        "id": 123, "name": "Проверка JSON", "start_date": "2026-12-10",
        "budget": 12345, "min_participants": 1,
    }
    person = {"id": 456, "name": "Тестовый участник", "trip_id": 123}
    trip_file = tmp_path / "trips.json"
    people_file = tmp_path / "participants.json"
    trip_file.write_text(json.dumps([trip]), encoding="utf-8")
    people_file.write_text(json.dumps([person]), encoding="utf-8")
    with patch("storage.DATA_DIR", tmp_path):
        html = client.get("/trips/123/").content.decode("utf-8")
        assert trip["name"] in html
        assert person["name"] in html
        assert "Группа готова к планированию" in html
        html = client.get("/participants/456/").content.decode("utf-8")
        assert trip["name"] in html
        assert person["name"] in html
        trip["name"] = "Новое название из файла"
        trip_file.write_text(json.dumps([trip]), encoding="utf-8")
        people_file.write_text("[]", encoding="utf-8")
        html = client.get("/trips/123/").content.decode("utf-8")
        assert trip["name"] in html
        assert person["name"] not in html
        assert "Набираем участников" in html
