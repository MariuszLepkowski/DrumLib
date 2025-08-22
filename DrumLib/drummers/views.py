from comments_app.forms import CommentForm
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .models import Drummer, DrummerPhoto


def sort_by_last_name(drummer):
    """Returns only last name of a drummer."""
    return drummer.name.split()[-1]


def drummers(request):
    template_name = "drummers_app/drummers.html"

    drummers = Drummer.objects.all().order_by("name")
    drummers_sorted = sorted(drummers, key=sort_by_last_name)

    context = {
        "title": "Drummers Explorer",
        "drummers": drummers_sorted,
    }

    return render(request, template_name, context)


def drummer_profile(request, drummer_name):
    template_name = "drummers_app/drummer-profile.html"

    drummer = Drummer.objects.get(name=drummer_name)
    comments = drummer.comment_set.filter(album__isnull=True)
    form = CommentForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to post a comment.")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.drummer = drummer
            comment.save()
            return redirect("drummers_app:drummer_profile", drummer_name=drummer.name)

    context = {
        "title": f"{drummer_name}",
        "drummer": drummer,
        "form": form,
        "comments": comments,
    }

    return render(request, template_name, context)
