from http import HTTPStatus
import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

import stripe

from cart.contexts import cart_contents
from checkout.forms import OrderForm
from checkout.models import Order, OrderLineItem
from products.models import Colour, Fragrance, Product
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from scentifique import settings


def checkout(request):
    """A view for the checkout page."""

    if request.method == "POST":
        return _save_order(request)
    else:
        return _view_checkout(request)


def _view_checkout(request):
    """Return the checkout page for a get request."""

    # Send error message if cart is empty.
    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Your shopping cart is empty!")
        return redirect(reverse("products"))

    # Set up Stripe payment intent.
    grand_total_pence = round(cart_contents(request)["grand_total"] * 100)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payment_intent = stripe.PaymentIntent.create(
        amount=grand_total_pence, currency=settings.STRIPE_CURRENCY
    )

    # Initialise order from.
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(
                initial={
                    "full_name": profile.user.get_full_name(),
                    "email": profile.user.email,
                    "phone_number": profile.default_phone_number,
                    "street_address1": profile.default_street_address1,
                    "street_address2": profile.default_street_address2,
                    "town_or_city": profile.default_town_or_city,
                    "county": profile.default_county,
                    "postcode": profile.default_postcode,
                    "country": profile.default_country,
                }
            )
        except UserProfile.DoesNotExist:
            order_form = OrderForm()
    else:
        order_form = OrderForm()

    # Return the rendered checkout page.
    context = {
        "order_form": order_form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": payment_intent.client_secret,
    }
    template = "checkout/checkout.html"
    return render(request, template, context)


def _save_order(request):
    """Save an order to the database."""

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
        # Save the order
        order = order_form.save(commit=False)
        stripe_pi_id = request.POST.get("client_secret").split("_secret")[0]
        order.stripe_pi_id = stripe_pi_id
        cart = request.session.get("cart", {})
        order.original_cart = json.dumps(cart)
        order.save()
        # Save the order's line items
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

    # Clear the cart, ready for the user's next order.
    request.session.pop("cart")

    order = get_object_or_404(Order, order_number=order_number)
    if request.user.is_authenticated:
        # Attach the user's profile to the order.
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()
        if request.session.get("save_info"):
            # Save the user's info.
            profile_data = {
                "default_phone_number": order.phone_number,
                "default_street_address1": order.street_address1,
                "default_street_address2": order.street_address2,
                "default_town_or_city": order.town_or_city,
                "default_county": order.county,
                "default_postcode": order.postcode,
                "default_country": order.country,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
            else:
                error_msg = "User profile data invalid! Please contact us."
                messages.error(request, error_msg)
    # Render the checkout sucess page.
    context = {"order": order}
    template = "checkout/checkout_success.html"
    return render(request, template, context)


@require_POST
def cache_checkout_data(request):
    """Add checkout data to the Stripe payment intent."""

    try:
        client_secret = request.POST.get("client_secret")
        payment_intent_id = client_secret.split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            payment_intent_id,
            metadata={
                "cart": json.dumps(request.session.get("cart", {})),
                "save_info": request.POST.get("save_info"),
                "username": request.user.username,
            },
        )
        return HttpResponse(status=HTTPStatus.OK)
    except Exception as e:
        messages.error(
            request,
            "We were unable to process your order. Please try again later.",
        )
        return HttpResponse(content=e, status=HTTPStatus.BAD_REQUEST)
