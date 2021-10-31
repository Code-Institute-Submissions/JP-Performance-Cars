from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

from .models import UserAccount
from .forms import UserAccountForm

from checkout.models import Booking


def account(request):
    """ Display the user's account. """
    account = get_object_or_404(UserAccount, user=request.user)

    if request.method == 'POST':
        form = UserAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'account updated successfully')
    form = UserAccountForm(instance=account)
    booking = account.bookings.all()

    template = 'accounts/account.html'
    context = {
        'form': form,
        'bookings': booking,
        'on_account_page': True
    }

    return render(request, template, context)


@login_required
def booking_confirmation(request, booking_number):
    """
    Displays booking overview with clear message that
    this confirmation is from the past
    """
    booking = get_object_or_404(Booking,
                                    booking_number=booking_number)

    messages.info(request, f'This is a past confirmation for booking \
         number {booking_number}. \
             A confirmation email was sent on the reservation date')

    template = 'checkout/checkout_success.html'
    context = {
        'booking': booking,
        'from_profile': True,
    }
    return render(request, template, context)