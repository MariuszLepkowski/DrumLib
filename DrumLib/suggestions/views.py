from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import AlbumSuggestionForm, DrummerSuggestionForm
from .models import AlbumSuggestion, DrummerSuggestion


class SuggestContentView(TemplateView):
    template_name = "suggestions/suggest-content.html"


class SuggestDrummerView(LoginRequiredMixin, CreateView):
    model = DrummerSuggestion
    form_class = DrummerSuggestionForm
    template_name = "suggestions/suggest-drummer.html"
    success_url = reverse_lazy("suggestions:suggestions_thank_you")

    def form_valid(self, form):
        form.instance.suggested_by = self.request.user
        return super().form_valid(form)


class SuggestAlbumView(LoginRequiredMixin, CreateView):
    model = AlbumSuggestion
    form_class = AlbumSuggestionForm
    template_name = "suggestions/suggest-album.html"
    success_url = reverse_lazy("suggestions:suggestions_thank_you")

    def form_valid(self, form):
        form.instance.suggested_by = self.request.user
        return super().form_valid(form)


class SuggestionsThankYouView(LoginRequiredMixin, TemplateView):
    template_name = "suggestions/thank-you.html"
