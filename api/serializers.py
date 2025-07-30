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
