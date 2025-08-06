# Python packages
import random

# DRF models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# api app models
from .serializers import api_register, api_activation, api_get_JWT, api_retrieve_flights, api_filter_flights, api_booked_flights, api_support_retrieve_message, api_support_create_message

# accounts app models
from accounts.models import User, ActivationCode

# flights app models
from flights.models import Flights, Tickets, support_massages

# utils
from utils import store_activation_info

# JWT
from auth.auth_token import create_access_token, jwt_token_status, retrieve_user_via_jwt

# AI
from openai import OpenAI

# OpenAI config
client = OpenAI(
    api_key="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"
)

# register user via api
class register(APIView):
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
class activation(APIView):
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


# retrieve all flights
class get_all_flight(APIView):
    """
    ret
    """
    def get(self, request):
        header_token = request.headers.get('Authorization')
        if header_token:
            token_status = jwt_token_status(header_token)
            if token_status:
                flights = Flights.objects.all()
                ser_data = api_retrieve_flights(instance=flights, many=True)
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No Token Retrieved'}, status=status.HTTP_400_BAD_REQUEST)


# filter flights api view
class filter_flight(APIView):
    """
    with this api view we will filter the flight based on user departure and destination
    """
    def post(self, request):
        header_token = request.headers.get('Authorization')
        if header_token:
            token_status = jwt_token_status(header_token)
            if token_status:
                ser_data = api_filter_flights(data=request.data)
                if ser_data.is_valid():
                    departure = ser_data.validated_data['departure']
                    destination = ser_data.validated_data['destination']
                    if departure is not None and destination is not None:
                        flights = Flights.objects.filter(departure=departure, destination=destination)
                        flights_ser_data = api_retrieve_flights(instance=flights, many=True)
                        if flights_ser_data:
                            return Response(flights_ser_data.data, status=status.HTTP_200_OK)
                        return Response({'message': 'we don\'t have any flights to fit your conditions.'}, status=status.HTTP_404_NOT_FOUND)
                    elif departure is not None and destination is None:
                        flights = Flights.objects.filter(departure=departure)
                        flights_ser_data = api_retrieve_flights(instance=flights, many=True)
                        if flights_ser_data:
                            return Response(flights_ser_data.data, status=status.HTTP_200_OK)
                        return Response({'message': 'we don\'t have any flights to fit your conditions.'}, status=status.HTTP_404_NOT_FOUND)
                    elif departure is None and destination is not None:
                        flights = Flights.objects.filter(destination=destination)
                        flights_ser_data = api_retrieve_flights(instance=flights, many=True)
                        if flights_ser_data:
                            return Response(flights_ser_data.data, status=status.HTTP_200_OK)
                        return Response({'message': 'we don\'t have any flights to fit your conditions.'}, status=status.HTTP_404_NOT_FOUND)
                    return Response({'message': 'something went wrong!!!.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No Token Retrieved'}, status=status.HTTP_400_BAD_REQUEST)


# API book flight
class book_flight(APIView):
    """
    the user can book a flight via this API view
    """
    def get(self, request, flight_id):
        header_token = request.headers.get('Authorization')
        if header_token:
            user = retrieve_user_via_jwt(header_token)
            if user and user.is_active:
                flight = Flights.objects.get(flight_id=flight_id)
                if flight:
                    if user.wallet > flight.flight_price:
                        user.wallet -= flight.flight_price
                        new_ticket = Tickets.objects.create(flight_id=flight, ticket_owner=user)
                        flight.flight_capacity -= 1
                        user.save()
                        new_ticket.save()
                        flight.save()
                        return Response({'message': f'Ticket for Flight Number {flight.flight_id} has been successfully booked.'}, status=status.HTTP_201_CREATED,)
                    return Response({'message': 'Your wallet doesn\'t have enough credit.'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'we coulden\'t find the flight with that ID'},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'we coulden\'t find the User with this credentials'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No Token Retrieved'}, status=status.HTTP_400_BAD_REQUEST)


# retrieve user's booked tickets
class booked_flights(APIView):
    """
    retrieve the user's booked tickets via API
    """
    def get(self, request):
        header_token = request.headers.get('Authorization')
        if header_token:
            user = retrieve_user_via_jwt(header_token)
            if user and user.is_active:
                booked_tickets = Tickets.objects.filter(ticket_owner=user)
                if booked_tickets:
                    ser_data = api_booked_flights(instance=booked_tickets, many=True)
                    return Response(ser_data.data, status=status.HTTP_200_OK)
                return Response({'message': 'no booked ticket found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'we coulden\'t find the User with this credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No Token Retrieved'}, status=status.HTTP_400_BAD_REQUEST)


# retrieve user wallet
class retrieve_user_wallet(APIView):
    """
    retrieve the wallet of the user via API
    """
    def get(self, request):
        header_token = request.headers.get('Authorization')
        if header_token:
            user = retrieve_user_via_jwt(header_token)
            if user and user.is_active:
                return Response({'wallet': user.wallet}, status=status.HTTP_200_OK)
            return Response({'message': 'we coulden\'t find the User with this credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No Token Retrieved'}, status=status.HTTP_400_BAD_REQUEST)


# AI support via API
class support(APIView):
    """
    with this view you can communicate with the AI which is learned with the site information and
     AI can guid you in the site and all this happens via API view.
    """
    def get(self, request):
        header_token = request.headers.get('Authorization')
        if header_token:
            user = retrieve_user_via_jwt(header_token)
            if user and user.is_active:
                all_messages = support_massages.objects.filter(user=user)
                ser_data = api_support_retrieve_message(instance=all_messages, many=True)
                if ser_data.data:
                    return Response(ser_data.data, status=status.HTTP_200_OK)
                return Response({'message': 'no message found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'we coulden\'t find the User with this credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No Token Retrieved'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        header_token = request.headers.get('Authorization')
        if header_token:
            user = retrieve_user_via_jwt(header_token)
            if user and user.is_active:
                ser_data = api_support_create_message(data=request.data)
                if ser_data.is_valid():
                    user_message = support_massages.objects.create(user=user, msg_sender_role='user',
                                                                   message=ser_data.validated_data['message'])
                    response = client.responses.create(
                        model="gpt-4o-mini",
                        input=[
                            {
                                "role": "system",
                                "content": "be the support of an Airline site and answer the questions base on the information that I will give you now,"
                                           " you can buy tickets from the the main page and flights page and you can filter flights with the departure and destination that you want,"
                                           " and you can see the tickets that you booked in my tickets page, and we sell plane tickets in this site.",
                            },
                            {
                                "role": "user",
                                "content": ser_data.validated_data['message']
                            }
                        ],
                        store=True,
                    )
                    AI_response = response.output_text
                    AI_message = support_massages.objects.create(user=user, msg_sender_role='AI', message=AI_response)
                    user_message.save()
                    AI_message.save()
                    return Response({'message': 'message sent and now you can retrieve it via GET methode'}, status=status.HTTP_201_CREATED)
                return Response({'message': 'invalid data'}, status=status.HTTP_406_NOT_ACCEPTABLE_OK)
            return Response({'message': 'we coulden\'t find the User with this credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'No Token Retrieved'}, status=status.HTTP_400_BAD_REQUEST)

















