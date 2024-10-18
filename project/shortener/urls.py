from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_short_url, name="create"),
    path("<str:url>/", views.redirect, name="redirect"),
    path("lk/links/", views.UrlListView.as_view(), name="links_list"),
    path(
        "lk/links/<str:pk>/delete/", views.UrlDeleteView.as_view(), name="link_delete"
    ),
    path(
        "lk/links/<str:pk>/update/", views.UrlUpdateView.as_view(), name="link_update"
    ),
]
