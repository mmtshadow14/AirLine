# Django models
from django.contrib import admin

# in app models
from .models import Flights, Tickets, homepage_objects, support_massages

# Register the models we want to show in the admin
admin.site.register(Flights)
admin.site.register(Tickets)
admin.site.register(homepage_objects)
admin.site.register(support_massages)
