# Django models
from django.urls import path

# aoi app models
from . import views

app_name = 'api'

urlpatterns = [
    path('register/', views.api_register.as_view(), name='api_register'),
    path('activation/', views.api_activation.as_view(), name='api_activation'),
]