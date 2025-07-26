# Django packages
from django import forms


# flight filter form
class flight_filter_form(forms.Form):
    """
    A form to get info from user to filter flights
    """
    departure = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Departure'
        }),
        required=False
    )

    destination = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Destination',
        }),
        required=False,
    )

    def clean_departure(self):
        """Convert empty departure to None"""
        departure = self.cleaned_data.get('departure')
        return departure if departure else None  # Returns None for empty string

    def clean_destination(self):
        """Convert empty destination to None"""
        destination = self.cleaned_data.get('destination')
        return destination if destination else None  # Returns None for empty string
