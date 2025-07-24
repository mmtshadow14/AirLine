# Django packages
from django import forms


# flight filter form
class flight_filter_form(forms.Form):
    """
    a form to get info from user to filter the flights for him
    """
    departure = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'departure'}))
    destination = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'destination'}))
