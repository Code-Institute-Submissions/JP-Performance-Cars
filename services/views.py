from django.shortcuts import render

# Create your views here.
def services(request):
    template = 'services/services.html'

    return render(request, template)