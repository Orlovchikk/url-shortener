import base64
import io
import os
import random
import string

import qrcode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from dotenv import load_dotenv

from . import models
from .forms import CreateNewShortUrl
from .models import ShortUrl


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
            s = ShortUrl(
                original_url=original_website,
                short_url=unique_key,
                datatime_created=timezone.now(),
                user=user,
            )
            s.save()

            load_dotenv()
            domain = os.getenv("domain")
            qrcode_png = create_qrcode(domain + str(unique_key))

            context = {
                "chars": unique_key,
                "qrcode": qrcode_png,
            }

            return render(request, "urlcreated.html", context)
    else:
        form = CreateNewShortUrl()
        return render(request, "create.html", {"form": form})


def redirect(request, url):
    try:
        obj = models.ShortUrl.objects.get(short_url=str(url))
        qrcode = create_qrcode(obj.original_url)
        context = {
            "original_url": obj.original_url,
            "qrcode": qrcode,
        }
        return render(request, "redirect.html", context=context)
    except Exception as e:
        print(e)
        return render(request, "pagenotfound.html")


def create_qrcode(link):
    qr = qrcode.QRCode(version=1, box_size=9, border=1)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qrcode_png_data = base64.b64encode(buffer.read()).decode("utf-8")

    return qrcode_png_data


class UrlListView(LoginRequiredMixin, ListView):
    model = ShortUrl
    template_name = "shortener/url_list.html"
    context_object_name = "url"
    login_url = "account_login"
