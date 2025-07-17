# Django packages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages


# in app models
from flights.models import Flights, Tickets


