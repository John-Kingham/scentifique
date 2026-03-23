import uuid

from django.conf import settings
from django.db import models
from django.db.models import Sum

from products.models import Colour, Fragrance, Product


class Order(models.Model):
    """A customer's order"""

    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    lineitems_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    original_cart = models.TextField(null=False, blank=False, default="")
    stripe_pi_id = models.CharField(
        max_length=254, null=False, blank=False, default=""
    )

    def _generate_order_number(self):
        """Generate a unique order number."""
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """Save the order with a unique order number."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def update_grand_total(self):
        """Update the order's grand total, including delivery costs."""
        result = self.lineitems.aggregate(lineitems_total=Sum("total"))
        self.lineitems_total = result["lineitems_total"] or 0
        self.delivery = settings.DELIVERY_FEE
        self.grand_total = self.lineitems_total + self.delivery
        self.save()

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """A line item in an order."""

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    colour = models.ForeignKey(
        Colour, null=False, blank=False, on_delete=models.CASCADE
    )
    fragrance = models.ForeignKey(
        Fragrance, null=False, blank=False, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """Save the line item with an updated total."""
        self.total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.product.name}, {self.colour.name}, "
            f"{self.fragrance.name}, on order {self.order}"
        )
