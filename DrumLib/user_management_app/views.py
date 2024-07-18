from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST': #if the form has been submitted
        form = UserRegistrationForm(request.POST) #form bound with post data
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account for {username} created successfully!')
            return render(request,'user_management_app/registration-success.html')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_management_app/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'user_management_app/login.html'
    authentication_form = CustomAuthenticationForm


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile(request):
    return render(request, 'user_management_app/profile.html')