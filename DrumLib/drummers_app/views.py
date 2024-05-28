from django.shortcuts import render, HttpResponse
from .models import Drummer, DrummerPhoto



def drummers(request):
    # response = ('drummers view. '
    #             'Displays list of drummers in the database with filtering and sorting options. '
    #             'Each drummer has a profile with basic information and an associated discography.')
    # return HttpResponse(response)

    template_name = "drummers_app/drummers.html"

    return render(request, template_name)



def drummer_profile(request, drummer_name):
    # response = f'drummer_profile view. Displays {drummer_name} profile with basic information and an associated discography.'
    # return HttpResponse(response, drummer_name)
    template_name = "drummers_app/drummer-profile.html"

    return render(request, template_name)


def add_drummer(request):
    # response = 'add_drummer view. Allows users to add_new drummer to db through form.'
    # return HttpResponse(response)
    template_name = "drummers_app/add-drummer.html"

    return render(request, template_name)