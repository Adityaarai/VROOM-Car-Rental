from django.db import models

CAR_TYPE = (
    ('SUV', 'SUV'),
    ('EV', 'EV'),
    ('Truck', 'Truck'),
    ('Sedan', 'Sedan'),
)

# Create your models here.
class CarDetails(models.Model):
    renter_name = models.CharField(max_length=100, null=True)
    renter_contact = models.CharField(max_length=100, null=True)
    car_type = models.CharField(max_length=100, choices=CAR_TYPE, null=True)
    car_model = models.CharField(max_length=100, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.renter_name} - {self.car_type} - {self.car_model} - {self.availability}'

