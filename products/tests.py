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
        cls.nonadmin_password = "adminpassword123"
        cls.nonadmin = User.objects.create_user(
            username="nonadmin",
            password=cls.nonadmin_password,
            email="nonadmin@email.com",
        )

    def test_products_view(self):
        """Test that the products page contains the correct information"""
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertContains(response, "Luxury Candles")
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)
        self.assertContains(response, settings.MEDIA_URL + "noimage.png")

    def test_product_detail(self):
        """
        Test that the product details page contains the correct information.
        """
        response = self.client.get(
            reverse("product_detail", args=[self.product1.id])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertContains(response, "Candle Details")
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product1.price)
        self.assertContains(response, self.product1.description)
        self.assertContains(response, settings.MEDIA_URL + "noimage.png")
        self.assertContains(response, self.colour.name)
        self.assertContains(response, self.fragrance.name)

    def test_add_product(self):
        """Test that the add product page has the correct information"""
        # Test as a guest
        response = self.client.get(reverse("add_product"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTemplateNotUsed(response, "products/add_product.html")
        # Test as a logged in superuser
        self.client.login(
            username=self.admin.username, password=self.admin_password
        )
        response = self.client.get(reverse("add_product"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/add_product.html")
        self.assertContains(response, "Add Product")
        self.assertContains(response, reverse("add_product"))

    def test_edit_product(self):
        """Test that the edit product page has the correct information"""
        # Test as a guest
        response = self.client.get(
            reverse("edit_product", args=[self.product1.id])
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # Test as a logged in non-superuser
        self.client.login(
            username=self.nonadmin.username, password=self.nonadmin_password
        )
        response = self.client.get(
            reverse("edit_product", args=[self.product1.id]),
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertContains(response, "Sorry")

        # Test as a logged in superuser
        self.client.login(
            username=self.admin.username, password=self.admin_password
        )
        response = self.client.get(
            reverse("edit_product", args=[self.product1.id])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/edit_product.html")
        self.assertContains(response, "Edit Product")

        # Test editing a product
        edited_product_name = "Edited Product Name"
        form_data = {
            "name": edited_product_name,
            "description": self.product1.description,
            "price": str(self.product1.price),
        }
        response = self.client.post(
            reverse("edit_product", args=[self.product1.id]),
            form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertContains(response, edited_product_name)
        self.product1.refresh_from_db()
        self.assertEquals(self.product1.name, edited_product_name)

    def test_delete_product(self):
        """Test that deleting a product works correctly"""
        # Test as a guest
        response = self.client.get(
            reverse("delete_product", args=[self.product1.id])
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # Test as a logged in non-superuser
        self.client.login(
            username=self.nonadmin.username, password=self.nonadmin_password
        )
        response = self.client.get(
            reverse("delete_product", args=[self.product1.id]),
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertContains(response, "Sorry")

        # Test as a logged in superuser
        self.client.login(
            username=self.admin.username, password=self.admin_password
        )
        response = self.client.get(
            reverse("delete_product", args=[self.product1.id]),
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertContains(response, self.product1.name)
