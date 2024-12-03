from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, CustomAuthenticationForm,  UserProfileForm
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User






class CustomLoginView(LoginView):
    template_name = 'user_management_app/login.html'
    authentication_form = CustomAuthenticationForm


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile(request):
    return render(request, 'user_management_app/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            # Save the profile
            profile = form.save(commit=False)
            # Update the user fields as well if needed
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()  # Save the user model
            profile.save()  # Save the profile model
            messages.success(request, 'Your profile has been updated!')
            return redirect('user_management_app:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'user_management_app/edit_profile.html', {'form': form})
