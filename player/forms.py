from django import forms

from .models import Song


class SongCreationForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["url"]
