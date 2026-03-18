from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from checkout.forms import OrderForm


def checkout(request):
    """A view for the checkout page."""

    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Your shopping cart is empty!")
        return redirect(reverse("products"))
    template = "checkout/checkout.html"
    order_form = OrderForm()
    context = {"order_form": order_form}
    return render(request, template, context)
