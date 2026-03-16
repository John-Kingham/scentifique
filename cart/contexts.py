from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Colour, Fragrance, Product


def cart_contents(request):
    """Return the shopping cart context."""

    total = 0
    cart_items = []
    cart = request.session.get("cart", {})
    for cart_item_key, quantity in cart.items():
        [product_id, colour_id, fragrance_id] = cart_item_key.split("_")
        product = get_object_or_404(Product, pk=product_id)
        colour = get_object_or_404(Colour, pk=colour_id)
        fragrance = get_object_or_404(Fragrance, pk=fragrance_id)
        total += product.price * quantity
        cart_items.append(
            {
                "key": cart_item_key,
                "product": product,
                "colour": colour,
                "fragrance": fragrance,
                "quantity": quantity,
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
