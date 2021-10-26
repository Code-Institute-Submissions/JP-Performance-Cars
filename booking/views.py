from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .models import ServiceCar, Manufacturer, Model
# Create your views here.

def book_in(request):
    service_cars = ServiceCar.objects.filter(do_service=True)
    manufacturers = Manufacturer.objects.all()
    models = Model.objects.all()

    context = {
        'service_cars': service_cars,
        'manufacturers': manufacturers,
        'models': models,
    }

    return render(request, 'booking/book-in.html', context) 