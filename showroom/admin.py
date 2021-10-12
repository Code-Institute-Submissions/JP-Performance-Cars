from django.contrib import admin
from .models import Car

# Register your models here.
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'status',
        'engine_information',
        'mileage',
    )

admin.site.register(Car, CarAdmin)