import uuid
from django.db import models
from django_countries.fields import CountryField

from booking.models import ServiceCar
from accounts.models import UserAccount

class Booking(models.Model):
    booking_number = models.CharField(max_length=32, null=False, editable=False)
    user_account = models.ForeignKey(UserAccount, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name="bookings")
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    annual = 1
    minor = 2
    service_type = (
        (annual, ('Annual')),
        (minor, ('Minor')),
    )
    booking_deposit = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    car = models.ForeignKey(ServiceCar, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    COMPLETED = 1
    IN_PROGRESS = 2
    NOT_STARTED = 3
    STATUS = (
        (COMPLETED, ('Completed')),
        (IN_PROGRESS, ('In Progress')),
        (NOT_STARTED, ('Not Started')),
    )
    stripe_pid = models.CharField(
        max_length=254, null=True, blank=True, default='')

    def _generate_booking_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = self._generate_booking_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_number