from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import About


class AboutViewTests(TestCase):

    def setUp(self):
        self.title = "Test About Title"
        self.content = "Test about content."
        self.about = About(title=self.title, content=self.content)
        self.about.save()
        self.response = self.client.get(reverse("about"))

    def test_about_view(self):
        """Test that the About page has the correct information."""
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertContains(self.response, self.title)
        self.assertContains(self.response, self.content)
        self.assertEqual(
            timezone.localtime(self.about.updated).date(),
            timezone.localdate(),
        )
