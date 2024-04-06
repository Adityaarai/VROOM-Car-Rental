from django.contrib import admin
from .models import CarDetails
from django.contrib.auth.models import Group

admin.site.site_header = 'VROOM database'

class CardetailsAdmin(admin.ModelAdmin):
    list_display = ('renter_name', 'car_type', 'car_model', 'availability')
    list_filter = ['car_type', 'car_model', 'availability']

# Register your models here.
admin.site.register(CarDetails, CardetailsAdmin)
admin.site.unregister(Group)