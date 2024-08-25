from django.shortcuts import render
from . import models
from .forms import CreateNewShortUrl
from datetime import datetime
import random
import string
from .models import ShortUrl


def home(request):
    return render(request, "home.html")


def create_short_url(request):
    if request.method == "POST":
        form = CreateNewShortUrl(request.POST)
        if form.is_valid():
            original_website = form.cleaned_data["original_url"]
            if ShortUrl.objects.filter(original_url=original_website).exists():
                unique_key = ShortUrl.objects.get(original_url=original_website)
                return render(request, "urlcreated.html", {"chars": unique_key})
            else:
                unique_key = "".join(
                    random.choices(string.ascii_letters + string.digits, k=6)
                )
                s = ShortUrl(
                    original_url=original_website,
                    short_url=unique_key,
                    datatime_created=datetime.now(),
                )
                s.save()
                return render(request, "urlcreated.html", {"chars": unique_key})
    else:
        form = CreateNewShortUrl()
        return render(request, "create.html", {"form": form})


def redirect(request, url):
    try:
        obj = models.ShortUrl.objects.get(short_url=str(url))
        print(obj)
        context = {"obj": obj}
        return render(request, "redirect.html", context=context)
    except Exception as e:
        print(e)
        return render(request, "pagenotfound.html")
