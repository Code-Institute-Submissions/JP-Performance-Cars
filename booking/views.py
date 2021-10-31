from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import datetime

from .models import ServiceCar, Manufacturer, Model
# Create your views here.

def book_in(request):
   if request.method == "POST":
       form = {
            'service_date': request.POST.get('service_date'),
       }
       if form["service_date"]:
           service_date = datetime.strptime(form["service_date"], '%Y-%m-%d').date()
           if service_date >= datetime.today().date():
              model = request.POST.get('model')
              manufacturer = request.POST.get('manufacturer')
              carQ = Q(manufacturer__name=manufacturer) & Q(model__name=model)
              car_id = ServiceCar.objects.filter(carQ).first().id
              form_data = {
                  "date": request.POST.get('date'),
                  "manufacturer": request.POST.get('manufacturer'),
                  "model": model,
                  "service_type": request.POST.get('service_type'),
                  "car_id": car_id
              }
              request.session['booking_request'] = form_data
              return redirect('checkout')
           else:
               messages.error(request, 'Your book in date can not be in the past. \
                            Please select another date.')
               return redirect(reverse('book_in'))
       else:
           messages.error(request, 'Please select a book in date.')
           return redirect(reverse('book_in'))
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


def check_availability(
        check_in, check_out, check_in_request, check_out_request):
    """
    Checks overlap with requested check-in and check-out
    Compared to existing reservations
    """
    overlap = False
    if check_in_request == check_out or check_out_request == check_in:
        overlap = False
    elif (check_in_request >= check_in and check_in_request <= check_out) or (
          check_out_request >= check_in and check_out_request <= check_out):
        overlap = True
    elif check_in_request <= check_in and check_out_request >= check_out:
        overlap = True

    return overlap