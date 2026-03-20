from http import HTTPStatus

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWebhookHandler

import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe."""

    # Try to construct the event.
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WH_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    except Exception as e:
        return HttpResponse(content=e, status=HTTPStatus.BAD_REQUEST)

    handler = StripeWebhookHandler(request)
    event_methods = {
        "payment_intent.succeeded": handler.handle_payment_succeeded,
        "payment_intent.payment_failed": handler.handle_payment_failed,
    }
    event_handler_method = event_methods.get(
        event["type"], handler.handle_event
    )
    response = event_handler_method(event)
    return response
