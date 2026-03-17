from http import HTTPStatus

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from products.models import Colour, Fragrance, Product


def view_cart(request):
    """A view for the shopping cart page."""

    context = {
        "colours": Colour.objects.all(),
        "fragrances": Fragrance.objects.all(),
        "quantities": range(1, settings.MAX_LINE_ITEM_QUANTITY + 1),
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
    product = get_object_or_404(Product, pk=product_id)
    messages.success(request, f"{quantity} x {product.name} added to cart.")
    return redirect(request.POST.get("redirect_url"))


def update_cart(request, cart_item_key):
    """Update an item in the cart."""

    product_id = cart_item_key.split("_")[0]
    colour_id = int(request.POST.get("colour_id"))
    fragrance_id = int(request.POST.get("fragrance_id"))
    quantity = int(request.POST.get("quantity"))
    cart = request.session.get("cart", {})
    new_cart_item_key = f"{product_id}_{colour_id}_{fragrance_id}"

    if new_cart_item_key == cart_item_key:
        cart[cart_item_key] = quantity
    elif new_cart_item_key in cart:
        cart[new_cart_item_key] += quantity
        if cart[new_cart_item_key] > settings.MAX_LINE_ITEM_QUANTITY:
            cart[new_cart_item_key] = settings.MAX_LINE_ITEM_QUANTITY
        cart.pop(cart_item_key)
    else:
        cart[new_cart_item_key] = quantity
        cart.pop(cart_item_key)

    request.session["cart"] = cart
    messages.success(request, "Shopping cart updated.")
    return redirect(reverse("view_cart"))


def remove_from_cart(request, cart_item_key):
    """Remove an item from the cart."""

    cart = request.session.get("cart", {})
    cart.pop(cart_item_key, None)
    request.session["cart"] = cart
    messages.success(request, "Item removed from shopping cart.")
    return HttpResponse(status=HTTPStatus.OK)
