from django.shortcuts import get_object_or_404
from .models import ServiceCar

def booking_details(request):

    deposit_cost = 0
    car = ""
    service_type = ""

    booking_req = request.session.get('booking_request', {})
    if "car_id" in booking_req:
        car = get_object_or_404(ServiceCar, pk=booking_req["car_id"])
        service_type = booking_req["service_type"]
        if booking_req["service_type"] == "annual":
            deposit_cost += float(car.annual_service_price) - float(car.annual_service_price) * .90
        elif booking_req["service_type"] == "minor":
            deposit_cost += float(car.minor_service_price) - float(car.minor_service_price) * .90

    context = {
        'car': car,
        'deposit_cost': deposit_cost,
        'service_type': service_type,
    }

    return context