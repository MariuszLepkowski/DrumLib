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
                return redirect("drummers:drummer_profile", pk=content_object.pk)
        else:
            form = CommentForm()

    elif content_type == "album":
        content_object = get_object_or_404(Album, id=object_id)
        drummer_slug = request.POST.get("drummer_slug")

        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.album = content_object
                comment.drummer = get_object_or_404(Drummer, slug=drummer_slug)
                comment.save()
                return redirect(
                    "discography:album_tracks",
                    album_title=content_object.title,
                    slug=comment.drummer.slug,
                )
        else:
            form = CommentForm()

    return render(request, "comments/add_comment.html", {"form": form})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            if comment.album:
                return redirect(
                    "discography:album_tracks",
                    album_title=comment.album.title,
                    slug=comment.drummer.slug,
                )
            elif comment.drummer:
                return redirect(
                    "drummers:drummer_profile",
                    pk=comment.drummer.pk,
                )
    else:
        form = CommentForm(instance=comment)
    return render(request, "comments/edit_comment.html", {"form": form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user or request.user.is_staff:
        if comment.album:
            redirect_url = redirect(
                "discography:album_tracks",
                album_title=comment.album.title,
                slug=comment.drummer.slug,
            )
        elif comment.drummer:
            redirect_url = redirect(
                "drummers:drummer_profile",
                pk=comment.drummer.pk,
            )
        comment.delete()
        return redirect_url
    return redirect(
        "drummers:drummer_profile",
        pk=comment.drummer.pk,
    )
