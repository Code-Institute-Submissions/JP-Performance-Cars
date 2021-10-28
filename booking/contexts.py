from django.shortcuts import get_object_or_404
from .models import ServiceCar

def booking_details(request):

    deposit_cost = 0
    booking_req = request.session.get('booking_request', {})
    car = get_object_or_404(ServiceCar, pk=booking_req["car_id"])

    if booking_req["service_type"] == "annual":
        deposit_cost += float(car.annual_service_price) - float(car.annual_service_price) * .90
    else:
        deposit_cost += float(car.minor_service_price) - float(car.minor_service_price) * .90

    context = {
        'car': car,
        'deposit_cost': deposit_cost,
    }

    return context