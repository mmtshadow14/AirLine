# Django packages
from django import forms


# flight filter form
class flight_filter_form(forms.Form):
    """
    a form to get info from user to filter the flights for him
    """
    departure = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Departure'
        }), required=False
    )
    destination = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Destination',
        }), required=False
    )
