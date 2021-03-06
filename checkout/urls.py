from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name="checkout"),
    path('checkout_success/<booking_number>', views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
]