from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

import stripe

from cart.contexts import cart_contents
from checkout.forms import OrderForm
from scentifique import settings


def checkout(request):
    """A view for the checkout page."""

    # Set up Stripe payment intent
    grand_total_pence = round(cart_contents(request)["grand_total"] * 100)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payment_intent = stripe.PaymentIntent.create(
        amount=grand_total_pence, currency=settings.STRIPE_CURRENCY
    )

    # Set up context
    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Your shopping cart is empty!")
        return redirect(reverse("products"))
    template = "checkout/checkout.html"
    order_form = OrderForm()
    context = {
        "order_form": order_form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": payment_intent.client_secret,
    }
    return render(request, template, context)
