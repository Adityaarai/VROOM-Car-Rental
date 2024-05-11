from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, null=True)
    license_number = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.user.username} - Profile'