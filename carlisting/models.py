from django.db import models
from django.contrib.auth.models import User

CAR_TYPE = (
    ('SUV', 'SUV'),
    ('EV', 'EV'),
    ('Truck', 'Truck'),
    ('Sedan', 'Sedan'),
)

# Create your models here.

# car details table model
class CarDetails(models.Model):
    renter_name = models.CharField(max_length=100, null=True)
    renter_contact = models.CharField(max_length=100, null=True)
    car_type = models.CharField(max_length=100, choices=CAR_TYPE, null=True)
    car_model = models.CharField(max_length=100, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    availability = models.BooleanField(default=True)

    # display what is shown in the product name
    def __str__(self):
        return f'{self.car_model} - {self.car_type} - {self.renter_name} '

# car orders table model
class CarOrders(models.Model):
    product = models.ForeignKey(CarDetails, on_delete=models.CASCADE)
    distributor = models.ForeignKey(User, models.CASCADE, null=True)
    number_of_days = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
    # display what is shown in the order name
    def __str__(self):
        return f'{self.product} distributed by {self.distributor}.'