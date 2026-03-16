from django.conf import settings
from django.shortcuts import redirect, render

from products.models import Colour, Fragrance


def view_cart(request):
    """A view for the shopping cart page."""
    context = {
        "colours": Colour.objects.all(),
        "fragrances": Fragrance.objects.all(),
        "quantities": range(1, settings.MAX_LINE_ITEM_QUANTITY+1)
    }
    return render(request, "cart/cart.html", context)


def add_to_cart(request, product_id):
    """Add items to the cart."""

    colour_id = int(request.POST.get("colour_id"))
    fragrance_id = int(request.POST.get("fragrance_id"))
    quantity = int(request.POST.get("quantity"))
    cart = request.session.get("cart", {})
    cart_item_key = f"{product_id}_{colour_id}_{fragrance_id}"
    if cart_item_key in cart:
        cart[cart_item_key] += quantity
    else:
        cart[cart_item_key] = quantity
    request.session["cart"] = cart
    return redirect(request.POST.get("redirect_url"))
