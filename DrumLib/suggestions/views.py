from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AlbumSuggestionForm, DrummerSuggestionForm


def suggest_content(request):
    return render(request, "suggestions_app/suggest-content.html")


@login_required
def suggest_drummer(request):
    if request.method == "POST":
        form = DrummerSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.suggested_by = request.user
            suggestion.save()
            return redirect("suggestions_app:suggestions_thank_you")
    else:
        form = DrummerSuggestionForm()
    return render(request, "suggestions_app/suggest-drummer.html", {"form": form})


@login_required
def suggest_album(request):
    if request.method == "POST":
        form = AlbumSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.suggested_by = request.user
            suggestion.save()
            return redirect("suggestions_app:suggestions_thank_you")
    else:
        form = AlbumSuggestionForm()
    return render(request, "suggestions_app/suggest-album.html", {"form": form})


@login_required
def suggestions_thank_you(request):
    return render(request, "suggestions_app/thank-you.html")
