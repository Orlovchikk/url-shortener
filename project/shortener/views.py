from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def Create_short_url(request):
    return render(request, "create.html")


def redirect(request):
    pass
