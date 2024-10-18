from django import forms

from .models import ShortUrl


class CreateNewShortUrl(forms.ModelForm):
    class Meta:
        model = ShortUrl
        fields = {"original_url"}
