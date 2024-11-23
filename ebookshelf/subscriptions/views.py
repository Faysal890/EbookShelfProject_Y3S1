# import datetime
from django.shortcuts import render
from django.views import View
import stripe
from django.conf import settings
import os
import logging
from flask import Flask, app, jsonify, json, request, current_app
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from .models import Subscription
from subscriptions.models import ProcessedEvent
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET = 'whsec_eb44c2095e5ad88cd989b9fed78855ee84f8889dc3320dd3b6b8a0b50365ac49'

        


def packages(request):
    return render(request, 'membership.html')


def create_checkout_session(request):
    if request.method == 'POST':
        membership_type = request.POST.get('membership')
        request.session['membership_type'] = membership_type

        # Map membership types to Stripe price IDs
        price_mapping = {
            'daily': 'price_1PbpTLGNnECLqhp0f3APuEQT',  
            'monthly': 'price_1PbpTrGNnECLqhp02elybbvp',  
            'yearly': 'price_1PbpUAGNnECLqhp0gFx3xf8C', 
        }

        price_id = price_mapping.get(membership_type)

        if not price_id:
            return JsonResponse({'error': 'Invalid membership type selected.'}, status=400)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='subscription',
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                # success_url=request.build_absolute_uri('/subscriptions/success/?session_id={CHECKOUT_SESSION_ID}'),
                # cancel_url=request.build_absolute_uri('/subscriptions/cancel/'),
    #              success_url='http://127.0.0.1:8000/subscriptions/success/?session_id={CHECKOUT_SESSION_ID}',
    # cancel_url='http://127.0.0.1:8000/subscriptions/cancel/',
                success_url = request.build_absolute_uri('/subscriptions/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url = request.build_absolute_uri('/subscriptions/cancel/'),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# def success(request):
#     return render(request, 'success.html')



def success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return JsonResponse({"error": "Session ID not provided"}, status=400)

    try:
        # Retrieve the session from Stripe
        checkout_session = stripe.checkout.Session.retrieve(session_id)


        membership_type = request.session.get('membership_type')
        

        # Extract necessary details
        subscription_id = checkout_session['subscription']
        customer_id = checkout_session['customer']
        amount = checkout_session['amount_total'] / 100  # Convert cents to dollars
        currency = checkout_session['currency']
        created_timestamp = checkout_session['created']  # Created timestamp
        stripe_expires_at = checkout_session.get('expires_at')  # Stripe expiration timestamp

      
        expires_at = datetime.fromtimestamp(stripe_expires_at) if stripe_expires_at else None
        if membership_type == 'daily':
            expires_at = datetime.now() + timedelta(days=1)
        elif membership_type == 'monthly':
            expires_at = datetime.now() + relativedelta(months=1)
        elif membership_type == 'yearly':
            expires_at = datetime.now() + relativedelta(years=1)
        # Saving Subscription model
        Subscription.objects.create(
            user=request.user,
            stripe_subscription_id=subscription_id,
            amount=amount,
            currency=currency,
            expires_at=expires_at
        )

        return render(request, 'success.html', {'subscription_id': subscription_id, 'amount': amount, 'currency': currency, 'created_timestamp': created_timestamp, 'expires_at': expires_at})
    except stripe.error.InvalidRequestError as e:
        return JsonResponse({"error": str(e)}, status=400)



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'whsec_eb44c2095e5ad88cd989b9fed78855ee84f8889dc3320dd3b6b8a0b50365ac49'

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    event_id = event['id']

    # Checking if the event has already been processed
    if ProcessedEvent.objects.filter(event_id=event_id).exists():
        return JsonResponse({'status': 'Event already processed'}, status=200)

    # Process the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session['customer_details']['email']
        stripe_subscription_id = session['subscription']

        ProcessedEvent.objects.create(event_id=event_id)

    return JsonResponse({'status': 'success'}, status=200)


def handle_checkout_session(session):
    """
    Process a successful checkout session.
    """
    print("Checkout session completed:", session)


def handle_invoice_payment(invoice):
    """
    Process a successful invoice payment.
    """
    print("Invoice payment succeeded:", invoice)


def handle_subscription_cancellation(subscription):
    """
    Process a subscription cancellation.
    """
    print("Subscription canceled:", subscription)