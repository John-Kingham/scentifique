from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class HomeTests(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("home"))

    def test_index_view(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "home/index.html")
        self.assertContains(self.response, "Luxury Candles")
