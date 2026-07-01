from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from scentifique import settings

from .models import Colour, Fragrance, Product


class ProductsTests(TestCase):

    @classmethod
    def setUp(cls):
        cls.colour = Colour(
            name="Red", hex="#FF0000", description="Test colour descrtption."
        )
        cls.colour.save()
        cls.fragrance = Fragrance(
            name="Rose", description="Test fragrance description."
        )
        cls.fragrance.save()
        cls.product1 = Product(
            name="Test Product 1",
            description="Test product 1 description.",
            price=11.11,
        )
        cls.product1.save()
        cls.product2 = Product(
            name="Test Product 2",
            description="Test product 2 description.",
            price=22.22,
        )
        cls.product2.save()
        cls.admin_password = "adminpassword123"
        cls.admin = User.objects.create_superuser(
            username="admin",
            password=cls.admin_password,
            email="admin@email.com",
        )

    def test_products_view(self):
        """Test that the products page contains the correct information"""
        self.response = self.client.get(reverse("products"))
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "products/products.html")
        self.assertContains(self.response, "Luxury Candles")
        self.assertContains(self.response, self.product1.name)
        self.assertContains(self.response, self.product2.name)
        self.assertContains(self.response, settings.MEDIA_URL + "noimage.png")

    def test_product_details_view(self):
        """
        Test that the product details page contains the correct information.
        """
        self.response = self.client.get(
            reverse("product_detail", args=[self.product1.id])
        )
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "products/product_detail.html")
        self.assertContains(self.response, "Candle Details")
        self.assertContains(self.response, self.product1.name)
        self.assertContains(self.response, self.product1.price)
        self.assertContains(self.response, self.product1.description)
        self.assertContains(self.response, settings.MEDIA_URL + "noimage.png")
        self.assertContains(self.response, self.colour.name)
        self.assertContains(self.response, self.fragrance.name)

    def test_add_product_view(self):
        """Test that the add product page has the correct information"""
        # Test as a guest
        self.response = self.client.get(reverse("add_product"))
        self.assertEqual(self.response.status_code, HTTPStatus.FOUND)
        # Test as a logged in admin
        self.client.login(
            username=self.admin.username, password=self.admin_password
        )
        self.response = self.client.get(reverse("add_product"))
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, "products/add_product.html")
        self.assertContains(self.response, "Add Product")
        self.assertContains(self.response, reverse("add_product"))

