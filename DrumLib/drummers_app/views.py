from django.shortcuts import render, HttpResponse
from .models import Drummer, DrummerPhoto


def sort_by_last_name(drummer):
    """Returns only last name of a drummer."""
    return drummer.name.split()[-1]


def drummers(request):
    template_name = "drummers_app/drummers.html"

    drummers = Drummer.objects.all().order_by('name')
    drummers_sorted = sorted(drummers, key=sort_by_last_name)

    context = {
        'title': 'Drummers Explorer',
        'drummers': drummers_sorted,
    }

    return render(request, template_name, context)



def drummer_profile(request, drummer_name):
    # response = f'drummer_profile view. Displays {drummer_name} profile with basic information and an associated discography.'
    # return HttpResponse(response, drummer_name)
    template_name = "drummers_app/drummer-profile.html"

    drummer =  Drummer.objects.get(name=drummer_name)
    context = {
        'title': f'{drummer_name}',
        'drummer': drummer,
    }

    return render(request, template_name, context)


def add_drummer(request):
    # response = 'add_drummer view. Allows users to add_new drummer to db through form.'
    # return HttpResponse(response)
    template_name = "drummers_app/add-drummer.html"
    context = {
        'title': 'Add Drummer'
    }

    return render(request, template_name, context)