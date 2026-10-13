from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("trips/", include("trips.urls")),
    path("participants/", include("participants.urls")),
]
handler404 = "homepage.views.page_not_found"
