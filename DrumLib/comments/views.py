from discography.models import Album
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from drummers.models import Drummer

from .forms import CommentForm
from .models import Comment


@login_required
def add_comment(request, content_type, object_id):
    if content_type == "drummer":
        content_object = get_object_or_404(Drummer, id=object_id)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.drummer = content_object
                comment.save()
                return redirect(
                    "drummers_app:drummer_profile", drummer_name=content_object.name
                )
        else:
            form = CommentForm()

    elif content_type == "album":
        content_object = get_object_or_404(Album, id=object_id)
        drummer_name = request.POST.get("drummer_name")

        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.album = content_object
                comment.save()
                return redirect(
                    "discography_app:album_tracks",
                    album_title=content_object.title,
                    drummer_name=drummer_name,
                )
        else:
            form = CommentForm()

    return render(request, "comments_app/add_comment.html", {"form": form})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            if comment.album:
                return redirect(
                    "discography_app:album_tracks",
                    album_title=comment.album.title,
                    drummer_name=comment.drummer.name,
                )
            elif comment.drummer:
                return redirect(
                    "drummers_app:drummer_profile", drummer_name=comment.drummer.name
                )
    else:
        form = CommentForm(instance=comment)
    return render(request, "comments_app/edit_comment.html", {"form": form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user or request.user.is_staff:
        if comment.album:
            redirect_url = redirect(
                "discography_app:album_tracks",
                album_title=comment.album.title,
                drummer_name=comment.drummer.name,
            )
        elif comment.drummer:
            redirect_url = redirect(
                "drummers_app:drummer_profile", drummer_name=comment.drummer.name
            )
        comment.delete()
        return redirect_url
    return redirect(
        "drummers_app:drummer_profile", drummer_name=comment.drummer.name
    )  # Fallback in case of failure
