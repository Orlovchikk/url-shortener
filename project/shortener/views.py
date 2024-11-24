import os
import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, ListView, UpdateView
from django_user_agents.utils import get_user_agent
from dotenv import load_dotenv
from statistic.models import ClickData

from . import models
from .forms import CreateNewShortUrl
from .utils import *


def home(request):
    return render(request, "home.html")


def create_short_url(request):
    if request.method == "POST":
        form = CreateNewShortUrl(request.POST)

        if form.is_valid():
            original_website = form.cleaned_data["original_url"]

            unique_key = "".join(
                random.choices(string.ascii_letters + string.digits, k=6)
            )

            user = request.user if request.user.is_authenticated else None
            s = models.ShortUrl(
                original_url=original_website,
                short_url=unique_key,
                datatime_created=timezone.now(),
                user=user,
                clicks=0,
            )
            s.save()

            load_dotenv()
            domain = "https://f5dc-94-25-229-185.ngrok-free.app"
            qrcode_png = create_qrcode(domain + "/" + str(unique_key))

            context = {
                "chars": unique_key,
                "qrcode": qrcode_png,
            }

            return render(request, "shortener/urlcreated.html", context)
    else:
        form = CreateNewShortUrl()
        return render(request, "shortener/create.html", {"form": form})


def redirect(request, url):
    try:
        obj = get_object_or_404(models.ShortUrl, short_url=url)

        if obj:
            country = get_country(request)
            user_agent_info = get_user_agent_info(get_user_agent(request))
            language = get_language(request.META.get("HTTP_ACCEPT_LANGUAGE", ""))

            click_data = ClickData.objects.create(
                short_url=obj,
                created_at=timezone.now(),
                country=country,
                language=language,
                **user_agent_info
            )
            click_data.save()

            obj.clicks += 1
            obj.save()

            qrcode = create_qrcode(obj.original_url)
            context = {
                "original_url": obj.original_url,
                "qrcode": qrcode,
            }
            return render(request, "shortener/redirect.html", context=context)
        else:
            return render(request, "shortener/pagenotfound.html")

    except Exception as e:
        print(e)


class UrlListView(LoginRequiredMixin, ListView):
    model = models.ShortUrl
    template_name = "shortener/link_list.html"
    context_object_name = "links"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["links"] = context["links"].filter(user=self.request.user)
        return context


class UrlDeleteView(LoginRequiredMixin, DeleteView):
    model = models.ShortUrl
    template_name = "shortener/link_confirm_delete.html"
    context_object_name = "link"
    login_url = "account_login"
    success_url = reverse_lazy("links_list")


class UrlUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ShortUrl
    template_name = "shortener/link_update_form.html"
    context_object_name = "link"
    login_url = "account_login"
    fields = ["original_url"]
    success_url = reverse_lazy("links_list")
