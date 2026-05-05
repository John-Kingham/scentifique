from http import HTTPStatus
import json
import time

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string

import stripe

from checkout.models import Order, OrderLineItem
from products.models import Colour, Fragrance, Product
from profiles.models import UserProfile


class StripeWebhookHandler:
    """Handle Stripe webhooks."""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send an order confirmation email to the user."""

        subject_template = "checkout/emails/confirmation_email_subject.txt"
        context = {"order": order}
        email_subject = render_to_string(subject_template, context)
        body_template = "checkout/emails/confirmation_email_body.txt"
        context = {
            "order": order,
            "contact_email": settings.DEFAULT_FROM_EMAIL,
        }
        email_body = render_to_string(body_template, context)
        to_email = order.email
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
        )

    def handle_event(self, event):
        """Handle generic webhook event."""

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=HTTPStatus.OK,
        )

    def handle_payment_succeeded(self, event):
        """Handle payment_intent.succeeded event."""

        # Initialise variables
        payment_intent = event.data.object
        stripe_pi_id = payment_intent.id
        original_cart = payment_intent.metadata.cart
        stripe_charge = stripe.Charge.retrieve(payment_intent.latest_charge)
        billing_details = stripe_charge.billing_details
        shipping_details = payment_intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Fix blank shipping details.
        for field_name, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field_name] = None

        # Update user profile for logged in users
        username = payment_intent.metadata.get("username", "")
        profile = None
        if username:
            profile = UserProfile.objects.get(user__username=username)
            save_info = payment_intent.metadata.get("save_info", "")
            if save_info == "true":
                self._update_user_profile(profile, shipping_details)

        # Check if order already exists
        attempt = 1
        MAX_ATTEMPTS = 5
        while attempt <= MAX_ATTEMPTS:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    town_or_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    postcode__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    grand_total=grand_total,
                    original_cart=original_cart,
                    stripe_pi_id=stripe_pi_id,
                )
                # Order exist
                self._send_confirmation_email(order)
                response_message = (
                    f"Webhook received: {event['type']} | "
                    "SUCCESS: Verified order is in database"
                )
                return HttpResponse(
                    content=response_message, status=HTTPStatus.OK
                )
            except Order.DoesNotExist:
                attempt += 1
                ONE_SECOND = 1
                time.sleep(ONE_SECOND)

        # Order doesn't exist, so create it
        order = None
        try:
            order = Order.objects.create(
                full_name=shipping_details.name,
                user_profile=profile,
                email=billing_details.email,
                phone_number=shipping_details.phone,
                street_address1=shipping_details.address.line1,
                street_address2=shipping_details.address.line2,
                town_or_city=shipping_details.address.city,
                county=shipping_details.address.state,
                postcode=shipping_details.address.postal_code,
                country=shipping_details.address.country,
                grand_total=grand_total,
                original_cart=original_cart,
                stripe_pi_id=stripe_pi_id,
            )
            original_cart = payment_intent.metadata.cart
            for lineitem_key, quantity in json.loads(original_cart).items():
                [product_id, colour_id, fragrance_id] = lineitem_key.split("_")
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
        except Exception as e:
            # Order creation failed, so return error response
            if order:
                order.delete()
            content = f"Webhook received: {event['type']} | ERROR: {e}"
            return HttpResponse(
                content=content, status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        # Order created in webhook
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(
                f"Webhook received: {event['type']} |"
                " SUCCESS: Created order in webhook"
            ),
            status=HTTPStatus.OK,
        )

    def _update_user_profile(self, profile, shipping_details):
        """Update the user profile for logged-in users."""

        profile.default_phone_number = shipping_details.phone
        profile.default_street_address1 = shipping_details.address.line1
        profile.default_street_address2 = shipping_details.address.line2
        profile.default_town_or_city = shipping_details.address.city
        profile.default_postcode = shipping_details.address.postal_code
        profile.default_county = shipping_details.address.state
        profile.default_country = shipping_details.address.country
        profile.save()

    def handle_payment_failed(self, event):
        """Handle payment_intent.payment_failed event."""

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=HTTPStatus.OK,
        )
