# Django models
from django.shortcuts import render

# DRF models
from rest_framework.views import APIView
from rest_framework.response import Response

# api app models
from .serializers import api_register

# accounts app models
from accounts.models import User, ActivationCode


# flights app models
from flights.models import Flights, Tickets


# register user via api
class api_register(APIView):
    """
    user can register in app via this api view
    """
    def post(self, request):
        ser_data = api_register(data=request.data)
        if ser_data.is_valid():
            pass
