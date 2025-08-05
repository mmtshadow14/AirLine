# Django models
from django.urls import path

# aoi app models
from . import views

app_name = 'api'

urlpatterns = [
    path('register/', views.register.as_view(), name='api_register'),
    path('activation/', views.activation.as_view(), name='api_activation'),
    path('get_token/', views.get_JWT.as_view(), name='api_activation'),
    path('get_flights/', views.get_all_flight().as_view(), name='api_get_all_flights'),
]