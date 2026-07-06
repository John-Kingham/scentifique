from http import HTTPStatus

from django.test import TestCase


class HandlerTests(TestCase):
    def test_404(self):
        response = self.client.get("nosuchpage.html")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, "errors/404.html")
