# Django packages
from django.db import models

# in app models
from accounts.models import User


class Flights(models.Model):
    flight_id = models.IntegerField(primary_key=True)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    pilot = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pilot')
    flight_capacity = models.IntegerField()
    flight_price = models.BigIntegerField()


class Tickets(models.Model):
    flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE, related_name='flight')
    ticket_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_owner')


