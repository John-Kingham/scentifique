from decimal import Decimal
from django.conf import settings


def cart_contents(request):
    """Return the shopping cart context."""

    cart_items = []
    delivery = settings.DELIVERY_FEE
    subtotal = 0
    grand_total = subtotal + delivery
    context = {
        "cart_items": cart_items,
        "delivery": delivery,
        "subtotal": subtotal,
        "grand_total": grand_total,
    }
    return context
