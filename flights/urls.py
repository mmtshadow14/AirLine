# Django packages
from django.urls import path

# in app models
from . import views

app_name = 'flights'

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('flight_detail/<int:flight_id>/', views.flight_detail.as_view(), name='flight_detail'),
    path('book_flight/<int:flight_id>/', views.book_flight.as_view(), name='book_flight'),
    path('flight_ready_to_be_booked/<str:flight_dep>/<str:flight_des>/', views.all_flight.as_view(), name='all_flight'),
]
