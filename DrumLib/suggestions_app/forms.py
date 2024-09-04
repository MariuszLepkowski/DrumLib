from django import forms
from .models import DrummerSuggestion, AlbumSuggestion


class DrummerSuggestionForm(forms.ModelForm):
    class Meta:
        model = DrummerSuggestion
        fields = ['name', 'bio']

class AlbumSuggestionForm(forms.ModelForm):
    class Meta:
        model = AlbumSuggestion
        fields = ['title', 'drummer', 'drummer_suggestion']
