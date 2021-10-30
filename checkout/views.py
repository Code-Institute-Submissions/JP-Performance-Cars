from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from booking.contexts import booking_details
from booking.models import ServiceCar

from .forms import BookingForm
from .models import Booking
from accounts.models import UserAccount
from accounts.forms import UserAccountForm

import stripe
import json

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'booking_request': json.dumps(request.session.get('booking_request', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
       booking_req = request.session.get('booking_request', {})

       form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

       booking_form = BookingForm(form_data)

       if booking_form.is_valid():
           booking = booking_form.save(commit=False)
           pid = request.POST.get('client_secret').split('_secret')[0]
           booking.stripe_pid = pid
           booking.save()
           try:
               car = ServiceCar.objects.get(id=booking_req["car_id"])
               booking.car = car
               booking.save()
           except ServiceCar.DoesNotExist:
               messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please call us for assistance!")
                    )
               booking.delete()
               return redirect(reverse('book_in'))
       else:
            messages.error(request, 'There was an error with your form. \
            Please double check your information.')

       request.session['save_info'] = 'save-info' in request.POST
       return redirect(reverse('checkout_success', args=[booking.booking_number]))

    else:
        booking_req = request.session.get('booking_request', {})
        if not booking_req:
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


def checkout_success(request, booking_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    booking = get_object_or_404(Booking, booking_number=booking_number)

    if request.user.is_authenticated:
        account = UserAccount.objects.get(user=request.user)
        booking.user_account = account
        booking.save()

        if save_info:
            account_data = {
                'default_phone_number': booking.phone_number,
                'default_country': booking.country,
                'default_postcode': booking.postcode,
                'default_town_or_city': booking.town_or_city,
                'default_street_address1': booking.street_address1,
                'default_street_address2': booking.street_address2,
                'default_county': booking.county,
            }
            user_account_form = UserAccountForm(account_data, instance=account)
            if user_account_form.is_valid():
                user_account_form.save()

    messages.success(request, f'booking successfully processed! \
        Your booking number is {booking_number}. A confirmation \
        email will be sent to {booking.email}.')

    if 'booking_req' in request.session:
        del request.session['booking_req']

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
    }

    return render(request, template, context)