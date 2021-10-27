from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .models import ServiceCar, Manufacturer, Model
# Create your views here.

def book_in(request):
   if request.method == "POST":
        form_data = {
            "date": request.POST.get('date'),
            "manufacturer": request.POST.get('manufacturer'),
            "model": request.POST.get('model'),
            "service_type": request.POST.get('service_type')
        }

        return redirect('checkout')
   else:

    service_cars = ServiceCar.objects.filter(do_service=True)
    manufacturers = Manufacturer.objects.all()
    models = Model.objects.all().order_by('name')
        
    context = {
        'service_cars': service_cars,
        'manufacturers': manufacturers,
        'models': models,
    }

    return render(request, 'booking/book-in.html', context) 