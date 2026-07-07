from decimal import Decimal, ROUND_HALF_UP
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Colour, Fragrance, Product
from scentifique import settings


class CartTests(TestCase):

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

    def test_view_cart(self):
        # Test empty cart
        response = self.client.get(reverse("view_cart"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cart/cart.html")
        self.assertContains(response, "Shopping Cart")
        self.assertNotContains(response, "Grand Total")
        self.assertContains(response, "Your shopping cart is empty")
        # Test non-empty cart
        subtotal1, subtotal2, grand_total = self._build_cart()
        response = self.client.get(reverse("view_cart"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product1.price)
        self.assertContains(response, subtotal1)
        self.assertContains(response, self.product2.name)
        self.assertContains(response, self.product2.price)
        self.assertContains(response, subtotal2)
        self.assertContains(response, grand_total)

    def _build_cart(self):
        """Create a cart with items and add it to the session"""
        cart = {}
        item1_key = f"{self.product1.id}_{self.colour.id}_{self.fragrance.id}"
        item1_quantity = 2
        cart[item1_key] = item1_quantity
        item2_key = f"{self.product2.id}_{self.colour.id}_{self.fragrance.id}"
        item2_quantity = 4
        cart[item2_key] = item2_quantity
        subtotal1 = self.product1.price * item1_quantity
        subtotal1 = subtotal1.quantize(Decimal("0.01"), ROUND_HALF_UP)
        subtotal2 = self.product2.price * item2_quantity
        subtotal2 = subtotal2.quantize(Decimal("0.01"), ROUND_HALF_UP)
        grand_total = subtotal1 + subtotal2 + settings.DELIVERY_FEE
        grand_total = grand_total.quantize(Decimal("0.01"), ROUND_HALF_UP)
        session = self.client.session
        session["cart"] = cart
        session.save()
        session = self.client.session
        return subtotal1, subtotal2, grand_total
