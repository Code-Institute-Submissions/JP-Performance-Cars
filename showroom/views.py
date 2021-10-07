from django.shortcuts import render

# Create your views here.


def showroom(request):
    template = 'showroom/showroom.html'

    return render(request, template)