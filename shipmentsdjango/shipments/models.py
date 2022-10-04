from pyexpat import model
from random import choices
from django.db import models
from django.forms import CharField

# Create your models here.
class Shipment(models.Model):
    IN_PROGRESS = 'In progress'
    COMPLETED = 'Completed'
    DELAYED = 'Delayed'

    STATUS_CHOICES = (
        (IN_PROGRESS, "Shipment is in progress"),
        (COMPLETED, "Shipment completed"),
        (DELAYED, "Shipment is delayed. Await further instructions."),
    )

    departureLocation = models.CharField(max_length=200)
    destinationLocation = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default=IN_PROGRESS)

    def __str__(self) -> str:
        return f"Shipment from {self.departureLocation} to {self.destinationLocation}. With status: {self.status}"