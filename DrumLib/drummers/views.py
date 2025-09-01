from comments.forms import CommentForm
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .models import Drummer


class DrummerListView(ListView):
    model = Drummer
    template_name = "drummers/drummers.html"
    context_object_name = "drummers"

    def get_queryset(self):
        return Drummer.objects.all().order_by("last_name", "first_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Drummers Explorer"
        return context


class DrummerDetailView(FormMixin, DetailView):
    model = Drummer
    template_name = "drummers/drummer-profile.html"
    context_object_name = "drummer"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("drummers:drummer_profile", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drummer = self.get_object()
        context["title"] = str(drummer)
        context["comments"] = drummer.comment_set.filter(album__isnull=True)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to post a comment.")
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.drummer = self.object
            comment.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)
