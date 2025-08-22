from django import forms
from .models import DrummerSuggestion, AlbumSuggestion


class DrummerSuggestionForm(forms.ModelForm):
    class Meta:
        model = DrummerSuggestion
        fields = ['name']

class AlbumSuggestionForm(forms.ModelForm):
    class Meta:
        model = AlbumSuggestion
        fields = ['album_author', 'album_title', 'drummers_on_album']
