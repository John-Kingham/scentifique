from http import HTTPStatus

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from products.models import Colour, Fragrance, Product


class CartView(TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["colours"] = Colour.objects.all()
        context["fragrances"] = Fragrance.objects.all()
        context["quantities"] = range(1, settings.MAX_LINE_ITEM_QUANTITY + 1)
        return context


class AddToCart(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        colour_id = int(request.POST.get("colour_id"))
        fragrance_id = int(request.POST.get("fragrance_id"))
        quantity = int(request.POST.get("quantity"))
        cart = request.session.get("cart", {})
        cart_item_key = f"{product_id}_{colour_id}_{fragrance_id}"
        product = get_object_or_404(Product, pk=product_id)

        # Handle matching items already in the cart
        if cart_item_key in cart:
            success_message = (
                " Your choice of candle, colour and fragrance matched another"
                " item in the cart, so the two items have been merged"
                " into one."
            )
            cart[cart_item_key] += quantity
            if cart[cart_item_key] > settings.MAX_LINE_ITEM_QUANTITY:
                cart[cart_item_key] = settings.MAX_LINE_ITEM_QUANTITY
        else:
            cart[cart_item_key] = quantity
            success_message = f"{quantity} x {product.name} added to cart."

        request.session["cart"] = cart
        messages.success(request, success_message)
        return redirect(request.POST.get("redirect_url"))


def update_cart(request, cart_item_key):
    """Update an item in the cart."""

    product_id = cart_item_key.split("_")[0]
    colour_id = int(request.POST.get("colour_id"))
    fragrance_id = int(request.POST.get("fragrance_id"))
    quantity = int(request.POST.get("quantity"))
    cart = request.session.get("cart", {})
    new_cart_item_key = f"{product_id}_{colour_id}_{fragrance_id}"

    colour_and_fragrance_unchanged = new_cart_item_key == cart_item_key
    updated_item_matches_another_item = new_cart_item_key in cart
    success_message = "Shopping cart updated."
    if colour_and_fragrance_unchanged:
        # Just update the quantity
        cart[cart_item_key] = quantity
    elif updated_item_matches_another_item:
        # Combine the items into a single cart item
        cart[new_cart_item_key] += quantity
        if cart[new_cart_item_key] > settings.MAX_LINE_ITEM_QUANTITY:
            cart[new_cart_item_key] = settings.MAX_LINE_ITEM_QUANTITY
        cart.pop(cart_item_key)
        success_message += (
            " The updated item matched another item in the"
            " cart, so the two items have been merged into one."
        )
    else:
        cart[new_cart_item_key] = quantity
        cart.pop(cart_item_key)

    request.session["cart"] = cart
    messages.success(request, success_message)
    return redirect(reverse("view_cart"))


def remove_from_cart(request, cart_item_key):
    """Remove an item from the cart."""

    cart = request.session.get("cart", {})
    cart.pop(cart_item_key, None)
    request.session["cart"] = cart
    messages.success(request, "Item removed from shopping cart.")
    return HttpResponse(status=HTTPStatus.OK)
