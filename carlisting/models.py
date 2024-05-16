from django.db import models
from django.contrib.auth.models import User
from userauthentication.models import Profile

CAR_TYPE = (
    ('SUV', 'SUV'),
    ('EV', 'EV'),
    ('Truck', 'Truck'),
    ('Sedan', 'Sedan'),
)
STATUS = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Paid', 'Paid'),
    ('Completed', 'Completed'),
)
AVAILABILITY = (
    ('Unlisted', 'Unlisted'),
    ('Booked', 'Booked'),
    ('Available', 'Available'),
)

# Create your models here.

# car details table model
class CarDetail(models.Model):
    renter_name = models.CharField(max_length=100, null=True)
    renter_contact = models.CharField(max_length=10, null=True)
    car_type = models.CharField(max_length=100, choices=CAR_TYPE, null=True)
    car_model = models.CharField(max_length=100, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY, null=True, default='Available')
    image = models.ImageField(default='static/img/lambo.jpg', upload_to='static/img/car_images')

    # display what is shown in the product name
    def __str__(self):
        return f'{self.car_model} - {self.car_type} - {self.renter_name} '

# car orders table model
class CarOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(CarDetail, on_delete=models.DO_NOTHING)
    rentee = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, default='Pending')
    
    # display what is shown in the order name
    def __str__(self):
        return f'{self.rentee} - {self.product} - {self.total_price} - {self.status}'