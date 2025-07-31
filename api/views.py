# Python packages
import random

# DRF models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# api app models
from .serializers import api_register, api_activation, api_get_JWT

# accounts app models
from accounts.models import User, ActivationCode

# flights app models
from flights.models import Flights, Tickets

# utils
from utils import store_activation_info

# JWT
from jwt import create_access_token, retrieve_user_via_jwt


# register user via api
class api_register(APIView):
    """
    user can register in app via this api view
    """
    def post(self, request):
        ser_data = api_register(data=request.data)
        if ser_data.is_valid():
            is_phone_number_exist = User.objects.filter(phone_number=ser_data.validated_data['phone_number'])
            if not is_phone_number_exist:
                user = User.objects.create_user(phone_number=ser_data.validated_data['phone_number'],
                                                password=ser_data.validated_data['password'],
                                                full_name=ser_data.validated_data['full_name'],
                                                address=ser_data.validated_data['address'],
                                                role='user')
                activation_code = random.randint(1000, 9999)
                ActivationCode.objects.create(phone_number=ser_data.validated_data['phone_number'],
                                              activation_code=activation_code)
                store_info = store_activation_info(request, ser_data.validated_data['phone_number'], activation_code)
                store_info.store_activation_info_in_session()
                user.save()
                return Response({"message": "User registered successfully, check your email for activation code"}, status=status.HTTP_201_CREATED)
            return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# activate user account via api
class api_activation(APIView):
    """
    the user can activate their account via this api view after they registered
    """
    def post(self, request):
        ser_data = api_activation(data=request.data)
        if ser_data.is_valid():
            session_phone_number = request.session.get('activation_phone_number')
            activation_info = ActivationCode.objects.get(phone_number=session_phone_number)
            user = User.objects.get(phone_number=session_phone_number)
            if activation_info.activation_code == ser_data.validated_data['activation_code']:
                user.is_active = True
                user.save()
                activation_info.delete()
                return Response({"message": "User activated successfully"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid activation code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Invalid activation code"}, status=status.HTTP_400_BAD_REQUEST)


# generate JWT access token
class get_JWT(APIView):
    """
    with this api view we will generate the user a new JWT token if his account was active
    """
    def post(self, request):
        ser_data = api_get_JWT(data=request.data)
        if ser_data.is_valid():
            user = User.objects.get(phone_number=ser_data.validated_data['phone_number'])
            if user.is_active and user.password == ser_data.validated_data['password']:
                generated_token = create_access_token(ser_data.validated_data['phone_number'])
                return Response({"token": generated_token}, status=status.HTTP_201_CREATED)
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)









