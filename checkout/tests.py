from decimal import ROUND_HALF_UP, Decimal
from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products.models import Colour, Fragrance, Product
from scentifique import settings


class CheckoutTests(TestCase):

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
            price=Decimal("11.11"),
        )
        cls.product1.save()
        cls.product2 = Product(
            name="Test Product 2",
            description="Test product 2 description.",
            price=Decimal("22.22"),
        )
        cls.product2.save()
        cls.user_password = "userpass123"
        cls.user = User.objects.create_user(
            username="user",
            password=cls.user_password,
            email="user@email.com",
        )
        cls.user.userprofile.default_phone_number = "123123123"
        cls.user.userprofile.save()

    def test_cannot_checkout_with_empty_cart(self):
        response = self.client.get(reverse("checkout"), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertContains(response, "Your shopping cart is empty!")

    def test_view_checkout_with_cart_items_and_user_profile(self):
        self.client.login(
            username=self.user.username, password=self.user_password
        )
        quantity = 2
        self._add_to_cart(
            self.product1.id, self.colour.id, self.fragrance.id, quantity
        )
        sub_total = (self.product1.price * quantity).quantize(
            Decimal("0.01"), ROUND_HALF_UP
        )
        grand_total = (sub_total + settings.DELIVERY_FEE).quantize(
            Decimal("0.01"), ROUND_HALF_UP
        )
        response = self.client.get(reverse("checkout"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "checkout/checkout.html")
        self.assertContains(response, "Checkout")
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.colour.name)
        self.assertContains(response, self.fragrance.name)
        self.assertContains(response, sub_total)
        self.assertContains(response, grand_total)
        self.assertContains(
            response, self.user.userprofile.default_phone_number
        )

    def _add_to_cart(self, product_id, colour_id, fragrance_id, quantity):
        form_data = {
            "colour_id": str(colour_id),
            "fragrance_id": str(fragrance_id),
            "quantity": str(quantity),
            "redirect_url": reverse("product_detail", args=[product_id]),
        }
        response = self.client.post(
            reverse("add_to_cart", args=[product_id]),
            form_data,
            follow=True,
        )
        return response
