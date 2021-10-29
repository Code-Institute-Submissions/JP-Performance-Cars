from django.contrib import admin
from .models import Booking


class BookingAdmin(admin.ModelAdmin):

    readonly_fields = ('booking_number', 'date', 'stripe_pid')

    fields = ('car', 'service_type', 'booking_number', 'user_account',
              'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'booking_deposit',
              'stripe_pid', 'status')

    list_display = ('booking_number', 'date', 'full_name',
                    'car', 'booking_deposit', 
                    )

    ordering = ('-date',)

admin.site.register(Booking, BookingAdmin)