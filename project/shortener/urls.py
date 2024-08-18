from django.urls import path

import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.Create_short_url, name="create"),
    path("<str:url>", views.redirect, name="redirect"),
]
