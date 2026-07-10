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

    def test_view_empty_cart(self):
        response = self.client.get(reverse("view_cart"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cart/cart.html")
        self.assertNotContains(response, "Grand Total")
        self.assertContains(response, "Your shopping cart is empty")

    def test_view_nonempty_cart(self):
        quantity1 = 2
        self._add_to_cart(
            self.product1.id, self.colour.id, self.fragrance.id, quantity1
        )
        quantity2 = 3
        self._add_to_cart(
            self.product2.id, self.colour.id, self.fragrance.id, quantity2
        )
        subtotal1 = (self.product1.price * quantity1).quantize(
            Decimal("0.01"), ROUND_HALF_UP
        )
        subtotal2 = (self.product2.price * quantity2).quantize(
            Decimal("0.01"), ROUND_HALF_UP
        )
        grand_total = (subtotal1 + subtotal2 + settings.DELIVERY_FEE).quantize(
            Decimal("0.01"), ROUND_HALF_UP
        )
        response = self.client.get(reverse("view_cart"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cart/cart.html")
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product1.price)
        self.assertContains(response, subtotal1)
        self.assertContains(response, self.product2.name)
        self.assertContains(response, self.product2.price)
        self.assertContains(response, subtotal2)
        self.assertContains(response, grand_total)

    def test_add_one_item_to_cart(self):
        quantity = 1
        response = self._add_to_cart(
            self.product1.id, self.colour.id, self.fragrance.id, quantity
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertContains(response, self.product1.name)
        self.assertContains(response, "added to cart")
        cart = self.client.session["cart"]
        cart_item_key = (
            f"{self.product1.id}_{self.colour.id}" f"_{self.fragrance.id}"
        )
        self.assertEqual(cart[cart_item_key], quantity)
        self.assertEqual(len(cart), 1)

    def test_add_multiple_items_to_cart(self):
        quantity = 1
        self._add_to_cart(
            self.product1.id, self.colour.id, self.fragrance.id, quantity
        )
        response = self._add_to_cart(
            self.product2.id, self.colour.id, self.fragrance.id, quantity
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertContains(response, self.product2.name)
        self.assertContains(response, "added to cart")
        cart = self.client.session["cart"]
        cart_item1_key = (
            f"{self.product1.id}_{self.colour.id}" f"_{self.fragrance.id}"
        )
        self.assertEqual(cart[cart_item1_key], quantity)
        cart_item2_key = (
            f"{self.product2.id}_{self.colour.id}" f"_{self.fragrance.id}"
        )
        self.assertEqual(cart[cart_item2_key], quantity)
        self.assertEqual(len(cart), 2)

    def test_add_duplicate_item_to_cart(self):
        quantity = 1
        self._add_to_cart(
            self.product1.id, self.colour.id, self.fragrance.id, quantity
        )
        response = self._add_to_cart(
            self.product1.id, self.colour.id, self.fragrance.id, quantity
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertContains(response, self.product1.name)
        self.assertContains(response, "two items have been merged into one")
        cart = self.client.session["cart"]
        self.assertEqual(len(cart), 1)
        cart_item_key = (
            f"{self.product1.id}_{self.colour.id}" f"_{self.fragrance.id}"
        )
        total_quantity = quantity * 2
        self.assertEqual(cart[cart_item_key], total_quantity)

    def test_add_invalid_quantity_of_items_to_cart(self):
        self._add_to_cart(
            self.product1.id,
            self.colour.id,
            self.fragrance.id,
            settings.MAX_LINE_ITEM_QUANTITY,
        )
        response = self._add_to_cart(
            self.product1.id, self.colour.id, self.fragrance.id, 1
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertContains(response, self.product1.name)
        self.assertContains(response, "two items have been merged into one")
        cart = self.client.session["cart"]
        cart_item_key = (
            f"{self.product1.id}_{self.colour.id}" f"_{self.fragrance.id}"
        )
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[cart_item_key], settings.MAX_LINE_ITEM_QUANTITY)

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
