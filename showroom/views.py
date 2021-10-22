from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Car, Manufacturer, Model

# Create your views here.


def showroom(request):

    cars = Car.objects.all()
    manufacturers = Manufacturer.objects.all()
    models = Model.objects.all()
    query = None
    sort = None
    direction = None
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                cars = cars.annotate(lower_name=Lower('name'))
            if sortkey == 'model':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            cars = cars.order_by(sortkey)

        if 'manufacturer' in request.GET:
            manufacturer = request.GET['manufacturer']
            cars = Car.objects.filter(manufacturer__name=manufacturer)
 

    current_sorting = f'{sort}_{direction}'
    print(manufacturers)
    context = {
        'cars_for_sale': cars,
        'current_manufacturer': manufacturer,
        'manufacturers': manufacturers,
        'search_term': query,
        'models': models,
        'current_sorting': current_sorting,
    }

    template = 'showroom/showroom.html'
    
    return render(request, template, context)