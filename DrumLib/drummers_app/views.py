from django.shortcuts import render, HttpResponse
from .models import Drummer, DrummerPhoto


def drummers(request):
    response = ('drummers view. '
                'Displays list of drummers in the database with filtering and sorting options. '
                'Each drummer has a profile with basic information and an associated discography.')
    return HttpResponse(response)


def drummer_profile(request, drummer_name):
    response = (f'drummer_profile view. Displays {drummer_name} profile with basic information and an associated discography.')
    return HttpResponse(response, drummer_name)