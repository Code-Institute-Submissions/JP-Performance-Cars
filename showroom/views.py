from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Car, Manufacturer, Model

# Create your views here.


def showroom(request):

    cars = Car.objects.all()
    manufacturers = Manufacturer.objects.all()
    manufacturer = None
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

        if 'manufacturerq' in request.GET:
            manufacturerQuery = request.GET['manufacturerq']
            modelQuery = request.GET['modelq']
            min_priceQuery = request.GET['min_priceq']
            max_priceQuery = request.GET['max_priceq']
            vehicle_search = f'{manufacturerQuery}&{modelQuery}&{min_priceQuery}&{max_priceQuery}'
            if not vehicle_search:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('showroom'))

            queries = Q(name__icontains=modelQuery) | Q(description__icontains=manufacturerQuery)
            cars = Car.objects.filter(queries)
 

    current_sorting = f'{sort}_{direction}'

    context = {
        'cars_for_sale': cars,
        'current_manufacturer': manufacturer,
        'manufacturers': manufacturers,
        'models': models,
        'current_sorting': current_sorting,
    }

    template = 'showroom/showroom.html'
    
    return render(request, template, context)


def car_detail(request, car_id):
    """ A view to show individual car details """

    car = get_object_or_404(Car, pk=car_id)

    context = {
        'car': car,
        'fixed_header': False
    }

    return render(request, 'showroom/car_detail.html', context)