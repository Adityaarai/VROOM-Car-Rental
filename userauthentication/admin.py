from django.contrib import admin
from .models import Distributor, Vroom_User

# Register your models here.

class DistributorsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact', 'email')

class UsersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact', 'email')

admin.site.register(Distributor, DistributorsAdmin)
admin.site.register(Vroom_User, UsersAdmin)