from django.contrib import admin
from .models import ServiceCar, Manufacturer, Model

# Register your models here.
class ServiceCarAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'service_price',
        'manufacturer',
        'model'
    )

admin.site.register(ServiceCar, ServiceCarAdmin)
admin.site.register(Manufacturer)
admin.site.register(Model)