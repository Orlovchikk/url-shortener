from django.urls import path

from . import views

urlpatterns = [
    path("stat/<str:pk>", views.short_url_stat, name="short-url-stat"),
]
