from django.db import models


class Short_url(models.Model):
    original_url = models.URLField(max_length=700)
    short_url = models.CharField(primary_key=True)
    datatime_created = models.DateTimeField()

    def __str__(self):
        return self.short_url
