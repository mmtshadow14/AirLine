# AI
from openai import OpenAI

# Django packages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# in app models
from flights.models import Flights, Tickets, homepage_objects, support_massages

# in app forms
from flights.forms import flight_filter_form, support_form

# OpenAI config
client = OpenAI(
    api_key="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"
)


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
                flight.flight_capacity -= 1
                user.save()
                new_ticket.save()
                flight.save()
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

        if flight_dep == "None":
            flight_dep = None
        if flight_des == "None":
            flight_des = None

        if flight_dep is not None and flight_des is not None:
            flights = flights.filter(departure=flight_dep, destination=flight_des)
            if flights:
                return render(request, self.template_name, {'flights': flights, 'form': form})
            messages.warning(request, 'we don\'t have any flights to fit your conditions.')
            return redirect('flights:all_flight')
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
                return redirect('flights:all_flight')
            elif form.cleaned_data['departure'] and form.cleaned_data['destination']:
                departure_filter = form.cleaned_data['departure']
                destination_filter = form.cleaned_data['destination']
                return redirect('flights:filter_flight', departure_filter, destination_filter)
            elif form.cleaned_data['departure'] and not form.cleaned_data['destination']:
                departure_filter = form.cleaned_data['departure']
                return redirect('flights:filter_flight', departure_filter, None)
            else:
                destination_filter = form.cleaned_data['destination']
                return redirect('flights:filter_flight', None, destination_filter)
        messages.error(request, 'something went wrong!')
        return redirect('flights:all_flight')


# support massage handler view
class support(LoginRequiredMixin, View):
    """
    this is the view if the user was authenticated he can ask question from the support and the support
     which is an AI will answer this his questions base on the information that we learned our AI.
    """
    template_name = 'flights/support.html'
    form_class = support_form

    def get(self, request):
        form = self.form_class
        all_messages = support_massages.objects.filter(user=request.user)
        return render(request, 'flights/support.html', {'form': form, 'all_messages': all_messages, })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            if form.cleaned_data['message']:
                user_message = support_massages.objects.create(user=user, msg_sender_role='user',
                                                               message=form.cleaned_data['message'])
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
                            "content": form.cleaned_data['message']
                        }
                    ],
                    store=True,
                )
                AI_response = response.output_text
                AI_message = support_massages.objects.create(user=user, msg_sender_role='AI', message=AI_response)
                user_message.save()
                AI_message.save()
                return redirect('flights:support')
            return redirect('flights:support')
        messages.error(request, 'something went wrong!!!')
        return redirect('flights:support')


# view to see the booked tickets
class my_tickets(LoginRequiredMixin, View):
    """
    this is a view for the user to see the flights that he already booked.
    """
    template_name = 'flights/my_tickets.html'

    def get(self, request):
        booked_tickets = Tickets.objects.filter(ticket_owner=request.user)
        return render(request, self.template_name, {'booked_tickets': booked_tickets})
