from django.urls import path
from . import views

urlpatterns = [
    path('', views.account, name="account"),
    path('booking_confirmation/<booking_number>/',
         views.booking_confirmation, name='booking_confirmation'),
]