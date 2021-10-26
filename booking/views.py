from django.shortcuts import render

# Create your views here.

def book_in(request):
    return render(request, 'booking/book-in.html') 