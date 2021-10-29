from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from booking.contexts import booking_details

from .forms import BookingForm
from .models import Booking

import stripe

# Create your views here.
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
       booking = request.session.get('booking_request', {})
    else:
        booking = request.session.get('booking_request', {})
        if not booking:
            messages.error(request, "Please create a booking first.")
            return redirect(reverse('book_in'))

        current_booking = booking_details(request)
        deposit_cost = current_booking['deposit_cost']
        stripe_total = round(deposit_cost * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        booking_form = BookingForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'booking_form': booking_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
