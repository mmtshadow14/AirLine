# Django models
from django.contrib import admin

# in app models
from .models import Flights, Tickets, homepage_objects

# Register the models we want to show in the admin
admin.site.register(Flights)
admin.site.register(Tickets)
admin.site.register(homepage_objects)
