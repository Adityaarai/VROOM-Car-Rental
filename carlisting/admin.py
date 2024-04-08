from django.contrib import admin
from .models import CarDetails, CarOrders
from django.contrib.auth.models import Group

# changing admin site header
admin.site.site_header = 'VROOM database'

# adding how the list displays and also adding filter fields
class CardetailsAdmin(admin.ModelAdmin):
    list_display = ('renter_name', 'car_type', 'car_model', 'availability')
    list_filter = ['car_type', 'car_model', 'availability']

class CarordersAdmin(admin.ModelAdmin):
    list_display = ('product', 'distributor', 'date', 'number_of_days', 'status')
    list_filter = ['distributor']


# Register your models here.
admin.site.register(CarDetails, CardetailsAdmin)
admin.site.register(CarOrders, CarordersAdmin)
admin.site.unregister(Group)