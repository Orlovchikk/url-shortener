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

        cls.users_url = ShortUrl.objects.create(
            original_url="https://0.0.0.0/qqq",
            short_url="sdf93c10",
            datatime_created=timezone.now(),
            user=cls.user,
        )

    def test_about_page_template(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Create New URL")

    def test_redirect_page_template(self):
        request = self.client.get(reverse("redirect", args=[self.url.short_url]))
        self.assertEqual(request.status_code, 200)
        self.assertContains(request, "https://0.0.0.0/")
        self.assertTemplateUsed(request, "shortener/redirect.html")
        self.assertContains(request, "You'll be redirected in")

    def test_links_list_view(self):
        self.client.login(email="test_creating@email.com", password="QweQwe123!@#")

        response = self.client.get(reverse("links_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/link_list.html")
        self.assertContains(response, "https://0.0.0.0/qqq")

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
        self.assertTemplateUsed(response, "shortener/urlcreated.html")

        short_url = ShortUrl.objects.get(original_url="https://0.0.0.0/aaa")
        request = self.client.get(reverse("redirect", args=[short_url.short_url]))

        self.assertEqual(request.status_code, 200)
        self.assertContains(request, "https://0.0.0.0/aaa")
        self.assertEqual(short_url.user, self.user)

    def test_create_url_for_logged_out_user(self):
        data = {
            "original_url": "https://0.0.0.0/fff",
            "short_url": "sdf93c3",
            "datatime_created": timezone.now(),
        }
        response = self.client.post(reverse("create"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/urlcreated.html")

        short_url = ShortUrl.objects.get(original_url="https://0.0.0.0/fff")
        request = self.client.get(reverse("redirect", args=[short_url.short_url]))

        self.assertEqual(request.status_code, 200)
        self.assertContains(request, "https://0.0.0.0/fff")
        self.assertIsNone(short_url.user)

    def test_create_incorrect_url(self):
        data = {
            "original_url": "incorrect_url",
            "short_url": "sdf93c1",
            "datatime_created": timezone.now(),
        }

        with self.assertRaises(ValueError):
            response = self.client.post(reverse("create"), data=data)
            self.assertIsNone(response)

        self.assertFalse(ShortUrl.objects.filter(original_url="incorrect_url").exists())

    def test_redirect_logged_out_user(self):
        links_list = self.client.get(reverse("links_list"), follow=True)
        self.assertEqual(links_list.status_code, 200)
        self.assertTemplateUsed(links_list, "account/login.html")

        link_delete = self.client.get(
            reverse("link_delete", args=[self.url.short_url]), follow=True
        )
        self.assertEqual(link_delete.status_code, 200)
        self.assertTemplateUsed(link_delete, "account/login.html")

        link_update = self.client.get(
            reverse("link_update", args=[self.url.short_url]), follow=True
        )
        self.assertEqual(link_update.status_code, 200)
        self.assertTemplateUsed(link_update, "account/login.html")

    # ....ShortUrl matching query does not exist. goes from here
    def test_invalid_short_url(self):
        response = self.client.get(reverse("redirect", args=["invalid_short_url"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/pagenotfound.html")

    def test_url_update_view(self):
        response = self.client.post(
            reverse("link_update", args=[self.users_url.short_url]),
            data={"original_url": "https://0.0.0.0/www"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

        self.client.login(email="test_creating@email.com", password="QweQwe123!@#")

        response = self.client.get(
            reverse("link_update", args=[self.users_url.short_url])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/link_update_form.html")
        self.assertTrue(
            ShortUrl.objects.filter(original_url="https://0.0.0.0/qqq").exists()
        )

        response = self.client.post(
            reverse("link_update", args=[self.users_url.short_url]),
            data={"original_url": "https://0.0.0.0/www"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ShortUrl.objects.filter(original_url="https://0.0.0.0/www").exists()
        )

    #  не работает почему-то :((
    # def test_update_view_incorrect_url(self):
    #     self.client.login(email="test_creating@email.com", password="QweQwe123!@#")

    #     self.assertTrue(
    #         ShortUrl.objects.filter(original_url="https://0.0.0.0/qqq").exists()
    #     )

    #     with self.assertRaises(ValueError):
    #         response = self.client.post(
    #             reverse("link_update", args=[self.users_url.short_url]),
    #             data={"original_url": "invalid_url"},
    #         )
    #         self.assertIsNone(response)

    #     self.assertFalse(ShortUrl.objects.filter(original_url="invalid_url").exists())

    def test_url_delete_view(self):
        response = self.client.post(
            reverse("link_delete", args=[self.users_url.short_url]),
            data={"pk": "sdf93c10"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

        self.client.login(email="test_creating@email.com", password="QweQwe123!@#")
        response = self.client.get(
            reverse("link_delete", args=[self.users_url.short_url]),
            data={"pk": "sdf93c10"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shortener/link_confirm_delete.html")
        self.assertTrue(
            ShortUrl.objects.filter(original_url="https://0.0.0.0/qqq").exists()
        )

        response = self.client.post(
            reverse("link_delete", args=[self.users_url.short_url]),
            data={"pk": "sdf93c10"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            ShortUrl.objects.filter(original_url="https://0.0.0.0/qqq").exists()
        )
