from django.shortcuts import render
from .models import Car

# Create your views here.


def showroom(request):

    cars = Car.objects.all()

    template = 'showroom/showroom.html'
    context = {
        'cars_for_sale': cars,
    }
    
    return render(request, template, context)