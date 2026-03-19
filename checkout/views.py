from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

import stripe

from cart.contexts import cart_contents
from checkout.forms import OrderForm
from checkout.models import Order, OrderLineItem
from products.models import Colour, Fragrance, Product
from scentifique import settings


def checkout(request):
    """A view for the checkout page."""

    if request.method == "POST":
        return _save_order(request)
    else:
        return _view_checkout(request)


def _view_checkout(request):
    """Return the checkout page for a get request."""

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


def _save_order(request):
    """Save an order to the database."""

    cart = request.session.get("cart", {})
    form_data = {
        "full_name": request.POST["full_name"],
        "email": request.POST["email"],
        "phone_number": request.POST["phone_number"],
        "country": request.POST["country"],
        "postcode": request.POST["postcode"],
        "town_or_city": request.POST["town_or_city"],
        "street_address1": request.POST["street_address1"],
        "street_address2": request.POST["street_address2"],
        "county": request.POST["county"],
    }
    order_form = OrderForm(form_data)
    if order_form.is_valid():
        order = order_form.save()
        for lineitem_key, quantity in cart.items():
            [product_id, colour_id, fragrance_id] = lineitem_key.split("_")
            try:
                product = Product.objects.get(id=product_id)
                colour = Colour.objects.get(id=colour_id)
                fragrance = Fragrance.objects.get(id=fragrance_id)
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    colour=colour,
                    fragrance=fragrance,
                    quantity=quantity,
                )
                order_line_item.save()
            except (
                Product.DoesNotExist,
                Colour.DoesNotExist,
                Fragrance.DoesNotExist,
            ):
                messages.error(
                    request,
                    (
                        "A product, colour or fragrance in your "
                        "shopping cart is no longer available. "
                        "Please contact us for assistance."
                    ),
                )
                order.delete()
                return redirect(reverse("view_cart"))
        request.session["save_info"] = "save-info" in request.POST
        return redirect(reverse("checkout_success", args=[order.order_number]))
    else:
        messages.error(
            request, "Error processing form: Please check your information."
        )
        return redirect(reverse("view_cart"))


def checkout_success(request, order_number):
    """Handle a successful checkout."""

    request.session.pop("cart")
    template = "checkout/checkout_success.html"
    order = get_object_or_404(Order, order_number=order_number)
    context = {"order": order}
    return render(request, template, context)
