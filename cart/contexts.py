from decimal import Decimal
from django.conf import settings


def cart_contents(request):
    """Return the shopping cart context."""

    cart_items = []
    delivery = settings.DELIVERY_FEE
    total = 0
    grand_total = total + delivery
    context = {
        "cart_items": cart_items,
        "delivery": delivery,
        "total": total,
        "grand_total": grand_total,
      }
    return context
