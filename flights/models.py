# Django packages
from django.db import models

# in app models
from accounts.models import User


# Flight model for DB
class Flights(models.Model):
    """
    this is a model to store Flights plan in the DB to use them to sell Tickets to the users
    """
    flight_id = models.IntegerField(primary_key=True, unique=True)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    pilot = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pilot')
    flight_capacity = models.IntegerField()
    flight_price = models.BigIntegerField()

    def __str__(self):
        return f'flight {self.flight_id} is leaving {self.departure} to {self.destination}.'


# Tickets model for DB
class Tickets(models.Model):
    """
    this is a model to store Tickets information that we sold to the users.
    """
    flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE, related_name='flight')
    ticket_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_owner')

    def __str__(self):
        return f'{self.ticket_owner.full_name} owns Ticket for {self.flight_id.flight_id} flight.'


class homepage_objects(models.Model):
    object_id = models.IntegerField(primary_key=True, unique=True)
    back_ground_for_flights = models.ImageField(upload_to='obj/')

    def __str__(self):
        return str(self.object_id)
