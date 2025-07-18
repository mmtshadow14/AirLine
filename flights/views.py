# Django packages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages

# in app models
from flights.models import Flights, Tickets


class home(View):
    def get(self, request):
        all_flights = Flights.objects.all()
        return render(request, 'flights/home.html', {'all_flights': all_flights})
