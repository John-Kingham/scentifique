from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class HomeTests(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertContains(response, "Luxury Candles")
