from django.shortcuts import render


def home_page(request):
    template_name = "home_app/home_page.html"
    return render(request, template_name)
