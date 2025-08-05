# DRF models
from rest_framework import serializers


# register serializer
class api_register(serializers.Serializer):
    """
    this serializer is going to be used to get registration information from the user
    """
    phone_number = serializers.CharField(max_length=11)
    full_name = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=500)
    password = serializers.CharField(max_length=100)
    password_confirm = serializers.CharField(max_length=100)


# account activation serializer
class api_activation(serializers.Serializer):
    """
    this serializer is going to be used to get activation code from the user
    """
    activation_code = serializers.CharField(max_length=4)


# get JWT token serializer
class api_get_JWT(serializers.Serializer):
    """
    with this we will get user and password from user, if the information was right
    """
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=100)


# retrieve flight serializer
class api_retrieve_flights(serializers.Serializer):
    """
    this serializer is going to be used to serialize app's flights plans
    """
    flight_id = serializers.IntegerField()
    departure = serializers.CharField(max_length=100)
    destination = serializers.CharField(max_length=100)
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()
    flight_capacity = serializers.IntegerField()
    flight_price = serializers.IntegerField()


# filter flights serializer
class api_filter_flights(serializers.Serializer):
    """
    this serializer is going to be used to serialize the users departure and destination info
    """
    departure = serializers.CharField(max_length=100)
    destination = serializers.CharField(max_length=100)
