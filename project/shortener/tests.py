from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import ShortUrl


class ShortenerTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = ShortUrl.objects.create(
            original_url="https://0.0.0.0/",
            short_url="sdf93c9",
            datatime_created=timezone.now(),
        )

        cls.user = get_user_model().objects.create_user(
            username="test_creating",
            email="test_creating@email.com",
            password="QweQwe123!@#",
        )

    def test_redirect(self):
        request = self.client.get(reverse("redirect", args=[self.url.short_url]))

        self.assertEqual(request.status_code, 200)
        self.assertContains(request, "https://0.0.0.0/")

    def test_create_url_for_logged_in_user(self):
        self.client.login(email="test_creating@email.com", password="QweQwe123!@#")

        data = {
            "original_url": "https://0.0.0.0/aaa",
            "short_url": "sdf93c9",
            "datatime_created": timezone.now(),
            "user": self.user,
        }

        response = self.client.post(reverse("create"), data=data)
        self.assertEqual(response.status_code, 200)

        short_url = ShortUrl.objects.get(original_url="https://0.0.0.0/aaa")
        request = self.client.get(reverse("redirect", args=[short_url.short_url]))

        self.assertEqual(request.status_code, 200)
        self.assertContains(request, "https://0.0.0.0/aaa")
        self.assertEqual(short_url.user, self.user)
