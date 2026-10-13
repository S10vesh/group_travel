from django.urls import path
from . import views

app_name = "participants"
urlpatterns = [
    path("", views.participant_list, name="list"),
    path("<int:participant_id>/", views.participant_detail, name="detail"),
]
