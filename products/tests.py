from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Colour, Fragrance, Product


class ProductsTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.colour = Colour(
            name="Red", hex="#FF0000", description="Test colour descrtption."
        )
        cls.fragrance = Fragrance(
            name="Rose", description="Test fragrance description."
        )
        cls.product = Product(
            name="Test Product",
            description="Test product description.",
            price=12.34,
        )

    def test_products_view(self):
        """Test that the products list view lists all products"""
        self.response = self.client.get(reverse("products"))
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
