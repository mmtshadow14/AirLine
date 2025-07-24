# Django packages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# in app models
from flights.models import Flights, Tickets, homepage_objects

# in app forms
from flights.forms import flight_filter_form


# view for showing the home page
class home(View):
    """
    this is a view to show the objects of the home page
    """

    def get(self, request):
        all_flights = Flights.objects.all()
        back_ground_obj = homepage_objects.objects.get(object_id=1)
        return render(request, 'flights/home.html', {'all_flights': all_flights, 'bgo': back_ground_obj})


# flight detail view to show the detail of the flight
class flight_detail(View):
    """
    this is a view to show the flight details in a new page and book the Ticket
    """
    template_name = 'flights/flight_detail.html'

    def get(self, request, flight_id):
        flight = get_object_or_404(Flights, flight_id=flight_id)
        back_ground_obj = homepage_objects.objects.get(object_id=1)
        delta_t = flight.arrival_time - flight.departure_time
        return render(request, self.template_name, {'flight': flight, 'bgo': back_ground_obj, "delta_t": delta_t})


# book flight
class book_flight(LoginRequiredMixin, View):
    """
    a view to book a flight if the user have enough money in his wallet
    """

    def get(self, request, flight_id):
        flight = get_object_or_404(Flights, flight_id=flight_id)
        user = request.user
        if user.is_authenticated and user.is_active == True:
            if user.wallet > flight.flight_price:
                user.wallet -= flight.flight_price
                new_ticket = Tickets.objects.create(flight_id=flight, ticket_owner=user)
                user.save()
                new_ticket.save()
                messages.success(request, 'Your flight has been successfully booked.')
                return redirect('flights:home')
            messages.warning(request, 'Your wallet doesn\'t have enough credit.')
            return redirect('book_flight', flight_id)
        messages.error(request, 'you dont have an account or your account haven\'t activated yet')
        return redirect('accounts:register')


# all or filtered flights
class all_flight(View):
    """
    a view to show all of the flights that are ready to be booked or to filter flights by dep and des
    """
    template_name = 'flights/all_flights.html'
    form_class = flight_filter_form

    def get(self, request, flight_dep=None, flight_des=None):
        flights = Flights.objects.all()
        form = self.form_class
        if flight_dep is not None and flight_des is not None:
            flights = flights.filter(departure=flight_dep, destination=flight_des)
            if flights:
                return render(request, self.template_name, {'flights': flights, 'form': form})
            messages.warning(request, 'we don\'t have any flights to fit your conditions.')
            return redirect('all_flights')
        elif flight_dep is not None and flight_des is None:
            flights = flights.filter(departure=flight_dep)
            if flights:
                return render(request, self.template_name, {'flights': flights, 'form': form})
            messages.warning(request, 'we don\'t have any flights to fit your conditions.')
            return redirect('all_flights')
        elif flight_dep is None and flight_des is not None:
            flights = Flights.objects.filter(destination=flight_des)
            if flights:
                return render(request, self.template_name, {'flights': flights, 'form': form})
            messages.warning(request, 'we don\'t have any flights to fit your conditions.')
            return redirect('all_flights')
        return render(request, self.template_name, {'flights': flights, 'form': form})

    def post(self, request, flight_dep=None, flight_des=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            if not form.cleaned_data['departure'] and not form.cleaned_data['destination']:
                return redirect('flights:filter_flight')
            elif form.cleaned_data['departure'] and form.cleaned_data['destination']:
                departure_filter = form.cleaned_data['departure']
                destination_filter = form.cleaned_data['destination']
                return redirect('flights:filter_flight', departure_filter, destination_filter)
            elif form.cleaned_data['departure'] and not form.cleaned_data['destination']:
                departure_filter = form.cleaned_data['departure']
                return redirect('flights:filter_flight', departure_filter)
            else:
                destination_filter = form.cleaned_data['destination']
                return redirect('flights:filter_flight', destination_filter)
        messages.error(request, 'something went wrong!')
        return redirect('flights:all_flight')
