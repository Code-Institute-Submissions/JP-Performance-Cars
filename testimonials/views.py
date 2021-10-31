from django.shortcuts import render

# Create your views here.
def testimonials(request):
    template = 'testimonials/testimonials.html'

    return render(request, template)