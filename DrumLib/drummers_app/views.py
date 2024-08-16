from django.shortcuts import render, HttpResponse
from .models import Drummer, DrummerPhoto
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from comments_app.forms import CommentForm


def sort_by_last_name(drummer):
    """Returns only last name of a drummer."""
    return drummer.name.split()[-1]


def drummers(request):
    template_name = "drummers_app/drummers.html"

    drummers = Drummer.objects.all().order_by('name')
    drummers_sorted = sorted(drummers, key=sort_by_last_name)

    context = {
        'title': 'Drummers Explorer',
        'drummers': drummers_sorted,
    }

    return render(request, template_name, context)


def drummer_profile(request, drummer_name):
    template_name = "drummers_app/drummer-profile.html"

    drummer = Drummer.objects.get(name=drummer_name)

    comments = drummer.comment_set.filter(album__isnull=True)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.drummer = drummer
            comment.save()

            return redirect('drummers_app:drummer_profile', drummer_name=drummer.name)

    context = {
        'title': f'{drummer_name}',
        'drummer': drummer,
        'form': form,
        'comments': comments,
    }

    return render(request, template_name, context)


def add_drummer(request):
    # response = 'add_drummer view. Allows users to add_new drummer to db through form.'
    # return HttpResponse(response)
    template_name = "drummers_app/add-drummer.html"
    context = {
        'title': 'Add Drummer'
    }

    return render(request, template_name, context)