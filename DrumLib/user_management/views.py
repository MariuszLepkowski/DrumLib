from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import CustomAuthenticationForm, UserProfileForm, UserRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return render(
            request, "user_management_app/registration-error-302.html", status=302
        )

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account for {username} created successfully!")
            login(request, user)
            return redirect("user_management_app:profile")
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = UserRegistrationForm()
    return render(request, "user_management_app/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "user_management_app/login.html"
    authentication_form = CustomAuthenticationForm


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def profile(request):
    return render(request, "user_management_app/profile.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            # Save the profile
            profile = form.save(commit=False)
            # Update the user fields as well if needed
            user = request.user
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()  # Save the user model
            profile.save()  # Save the profile model
            messages.success(request, "Your profile has been updated!")
            return redirect("user_management_app:profile")
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, "user_management_app/edit_profile.html", {"form": form})
