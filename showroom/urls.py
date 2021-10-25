from django.urls import path
from . import views

urlpatterns = [
    path('', views.showroom, name="showroom"),
    path('<int:car_id>/', views.car_detail, name="car_detail")
]