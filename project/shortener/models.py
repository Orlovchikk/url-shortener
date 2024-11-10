from accounts.models import CustomUser
from django.db import models
from django.urls import reverse


class ShortUrl(models.Model):
    original_url = models.URLField(max_length=300)
    short_url = models.CharField(primary_key=True)
    datatime_created = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    clicks = models.IntegerField()

    def get_absolute_url(self):
        return reverse("redirect", kwargs={"url": self.short_url})

    def __str__(self):
        return self.short_url
