from django.db.models import Q
from django.views import generic

from .forms import SongCreationForm
from .models import Song


class SongCreationView(generic.CreateView):
    form_class = SongCreationForm
    template_name = "player/song_new.html"

    def get_success_url(self) -> str:
        return "/new/"


class ListSongView(generic.ListView):
    context_object_name = "songs"
    template_name = "player/index.html"

    def get_queryset(self):
        return Song.objects.filter(~Q(status="NA") & ~Q(status="fail"))
