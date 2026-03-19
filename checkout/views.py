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
    context = {
        "order_form": order_form,
        "stripe_public_key": (
            "pk_test_51TCdcpGtQSzblww04CfnJuoWHCbL2jdZipJKGHNr1SdfJvvYQ7J1TM"
            "nltHYcwLL6FPWIUK14A6nNiR3CNpvSr8s300bmr72TAD"
        ),
        "client_secret": "TEST CLIENT SECRET",
    }
    return render(request, template, context)
