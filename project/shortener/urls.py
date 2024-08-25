from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_short_url, name="create"),
    path("<str:url>", views.redirect, name="redirect"),
]
