from django.db import models
from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
    """
    Represents parking facility managers. Extends Django's built-in User model.
    """
    modified = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username} ({self.address})"


class ParkingUser(models.Model):
    """
    Represents employees/users who have parking access.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='parking_users'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('client', 'email')
        indexes = [
            models.Index(fields=['client']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class LicencePlate(models.Model):
    """
    Represents a licence plate that can be used to identify a vehicle.
    """
    licence_plate = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    parking_user = models.ForeignKey(
        ParkingUser,
        on_delete=models.CASCADE,
        related_name='licence_plates'
    )

    def __str__(self):
        return f"{self.licence_plate} ({self.region})"
