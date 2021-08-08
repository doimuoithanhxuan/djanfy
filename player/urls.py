from django.urls import path

from . import views

app_name = "player"

urlpatterns = [
    path("new/", views.SongCreationView.as_view(), name="song-new"),
    path("", views.ListSongView.as_view(), name="index"),
]
