from django.db import models

# Create your models here.

# distributor user table model
class Distributor(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=100, null=True)
    image = models.ImageField(default='static/img/profileicon.png', upload_to='static/img/user_images')

# user table model
class Vroom_User(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=100, null=True)
    image = models.ImageField(default='static/img/profileicon.png', upload_to='static/img/user_images')