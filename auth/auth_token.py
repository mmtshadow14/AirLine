# Python packages
import jwt
import datetime
import time

# django packages
from rest_framework.response import Response

# AirLine project models
from AirLine import settings

# account app models
from accounts.models import User


# create JWT access token
def create_access_token(user_phone_number):
    """
    we will generate a JWT token for the user with placing his account ID in the payload of the JWT token.
    """
    payload = {
        'user_phone_number': user_phone_number,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    secret_key = 'jwt'
    return jwt.encode(payload, secret_key, algorithm='HS256')


# retrieve the user
def retrieve_user_via_jwt(token):
    """
    retrieve the user from the JWT token that is sent in the head of the request to use it in the routes
     to do CRUD operations.
    """
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
    if payload['exp'] < int(time.time()):
        return {'message': 'Token is expired'}
    user = User.objects.get(phone_number=payload['user_phone_number'])
    if user:
        return user
    return {'message': 'User not found'}


# check JWT validation status
def jwt_token_status(token):
    """
    check the JWT token validation
    """
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
    if payload['exp'] < int(time.time()):
        return Response({"detail": "Token has expired"}, status=401)
    user = User.objects.get(phone_number=payload['user_phone_number'])
    if user:
        return True
    return False
