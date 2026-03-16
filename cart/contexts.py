from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product


def cart_contents(request):
    """Return the shopping cart context."""

    total = 0
    cart_items = []
    cart = request.session.get("cart", {})
    for cart_item_key, quantity in cart.items():
        [product_id, colour_id, fragrance_id] = cart_item_key.split("_")
        product = get_object_or_404(Product, pk=product_id)
        total += product.price * quantity
        cart_items.append(
            {
                "product_id": product_id,
                "colour_id": colour_id,
                "fragrance_id": fragrance_id,
                "quantity": quantity,
                "product": product,
            }
        )

    delivery = settings.DELIVERY_FEE
    grand_total = total + delivery
    context = {
        "cart_items": cart_items,
        "delivery": delivery,
        "total": total,
        "grand_total": grand_total,
    }
    return context
