from django import forms


# register form for normal users
class register_form(forms.Form):
    """
    Registration Form For The normal users which they are going to use the site services and clean password to check if
    the password and password confirmation match.
    """
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cd = super().clean()
        password = cd['password']
        password_confirm = cd['password_confirm']
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords must match')


# activation form for activating normal users
class activation_form(forms.Form):
    """
    this form is to get activation code that we sent to users phone number in the Register view in employees.views.py
    to confirm the user's phone number and activate their account.
    """
    activation_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activation Code'}))

    def clean(self):
        cd = super().clean()
        activation_code = cd['activation_code']
        char_count = 0
        for char in activation_code:
            char_count += 1
        if char_count > 4:
            raise forms.ValidationError('Activation code is too long')


# login form
class login_form(forms.Form):
    """
    a form to get phone number and password for the user to log in his account.
    """
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class add_staff_form(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    role = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Role'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cd = super().clean()
        password = cd['password']
        password_confirm = cd['password_confirm']
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords must match')




















