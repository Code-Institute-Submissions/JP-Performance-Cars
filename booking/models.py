from django.db import models

# Create your models here.
class Manufacturer(models.Model):
    
    class Meta:
        verbose_name_plural = 'Manufacturers'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Model(models.Model):
    
    class Meta:
        verbose_name_plural = 'Models'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class ServiceCar(models.Model):
    
    name = models.CharField(max_length=50)
    annual_service_price = models.DecimalField(max_digits=6, decimal_places=2, default=False, null=True, blank=True)
    minor_service_price = models.DecimalField(max_digits=6, decimal_places=2, default=False, null=True, blank=True)
    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, on_delete=models.SET_NULL)
    model = models.ForeignKey('Model', null=True, blank=True, on_delete=models.SET_NULL)
    do_service = models.BooleanField(default=False, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.name