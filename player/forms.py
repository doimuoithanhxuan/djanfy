from django import forms
from django.db.models import Q

from .models import Song
from .youtube_dl import CustomYoutubeDL, DownloadInThread


class SongCreationForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["url"]

    def clean(self):
        self.ytdl = CustomYoutubeDL()
        url = self.cleaned_data["url"]
        try:
            self.ie_result = self.ytdl.get_ie_result(url)
        except Exception:
            raise forms.ValidationError({"Youtube-dl Error": "Cannot get IE_RESULT"})
        else:
            if not self.ie_result:
                raise forms.ValidationError({"url": "Not supported"})
            if self.ie_result.get("is_live", False):
                raise forms.ValidationError({"url": "Can not download live video"})

            if Song.objects.filter(
                Q(song_id=self.ie_result["id"]), Q(status="success") | Q(status="downloading")
            ).count():
                raise forms.ValidationError({"url": "This song existed"})
        return {"url": url, "song_id": self.ie_result["id"], "title": self.ie_result["title"]}

    def save(self, commit: bool = False):
        song = super().save(commit=commit)
        song.title = self.cleaned_data["title"]
        song.song_id = self.cleaned_data["song_id"]
        song.status = "downloading"
        DownloadInThread(ytdl=self.ytdl, ie_result=self.ie_result, song=song).start()
        return song.save()
