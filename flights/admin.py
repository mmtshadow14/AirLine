# Django models
from django.contrib import admin

# in app models
from .models import Flights, Tickets

# Register the models we want to show in the admin
admin.site.register(Flights)
admin.site.register(Tickets)
