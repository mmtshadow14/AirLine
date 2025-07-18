# Django packages
from django.urls import path

# in app models
from . import views

app_name = 'flights'

urlpatterns = [
    path('flight_detail/<int:flight_id>/', views.flight_detail.as_view(), name='flight_detail'),
]
