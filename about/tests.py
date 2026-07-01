from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import About


class AboutTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.title = "Test About Title"
        cls.content = "Test about content."
        cls.about = About(title=cls.title, content=cls.content)
        cls.about.save()

    def test_about_view(self):
        """Test that the About page has the correct information."""
        self.response = self.client.get(reverse("about"))
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "about/about.html")
        self.assertContains(self.response, self.title)
        self.assertContains(self.response, self.content)

    def test_about_model(self):
        """Test that About fields have correct auto-generated values."""
        self.assertEqual(
            timezone.localtime(self.about.updated).date(),
            timezone.localdate(),
        )
