# Django packages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages

# in app models
from flights.models import Flights, Tickets, homepage_objects


# view for showing the home page
class home(View):
    """
    this is a view to show the objects of the home page
    """

    def get(self, request):
        all_flights = Flights.objects.all()
        back_ground_obj = homepage_objects.objects.get(object_id=1)
        return render(request, 'flights/home.html', {'all_flights': all_flights, 'bgo': back_ground_obj})


# flight detail view to show the detail of the flight
class flight_detail(View):
    """
    this is a view to show the flight details in a new page and book the Ticket
    """
    template_name = 'flights/flight_detail.html'

    def get(self, request, flight_id):
        flight = get_object_or_404(Flights, flight_id=flight_id)
        return render(request, self.template_name, {'flight': flight})
