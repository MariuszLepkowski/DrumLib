# comments_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from drummers_app.models import Drummer
from discography_app.models import Album
from .forms import CommentForm


@login_required
def add_comment(request, content_type, object_id):
    if content_type == 'drummer':
        content_object = get_object_or_404(Drummer, id=object_id)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.drummer = content_object
                comment.save()
                return redirect('drummers_app:drummer_profile', drummer_name=content_object.name)
        else:
            form = CommentForm()

    elif content_type == 'album':
        content_object = get_object_or_404(Album, id=object_id)
        drummer_name = request.POST.get('drummer_name')

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.album = content_object
                comment.save()
                return redirect('discography_app:album_tracks', album_title=content_object.title, drummer_name=drummer_name)
        else:
            form = CommentForm()

    return render(request, 'comments_app/add_comment.html', {'form': form})

