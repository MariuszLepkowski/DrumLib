from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST': #if the form has been submitted
        form = UserRegistrationForm(request.POST) #form bound with post data
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account for {username} created successfully!')
            return render(request,'user_management_app/registration-success.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_management_app/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')