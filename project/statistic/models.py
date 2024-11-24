from django.db import models
from shortener.models import ShortUrl


class ClickData(models.Model):
    short_url = models.ForeignKey(ShortUrl, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    country = models.CharField(null=True)
    browser = models.CharField(null=True)
    language = models.CharField(null=True)
    device_type = models.CharField(null=True)
    operating_system = models.CharField(null=True)
    is_bot = models.BooleanField(null=True)

    class Meta:
        ordering = ("created_at",)
