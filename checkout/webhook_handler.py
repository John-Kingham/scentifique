from http import HTTPStatus

from django.http import HttpResponse


class StripeWebhookHandler:
    """Handle Stripe webhooks."""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle generic webhook event."""

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=HTTPStatus.OK,
        )

    def handle_payment_succeeded(self, event):
        """Handle payment_intent.succeeded event."""

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=HTTPStatus.OK,
        )

    def handle_payment_failed(self, event):
        """Handle payment_intent.payment_failed event."""

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=HTTPStatus.OK,
        )
