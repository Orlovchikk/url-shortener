from django.urls import path

from . import views

urlpatterns = [path("", views.ClicksListView.as_view(), name="statistics")]
