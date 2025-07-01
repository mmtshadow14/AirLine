# Python packages
import random

# Django packages
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

# employees app's models
from .models import User, ActivationCode

# employees app's forms
from .forms import register_form, activation_form, login_form

# utils
from utils import store_activation_info


# home page view
class home(View):
    """
    a class to render the home page and show home page objects
    """

    def get(self, request):
        return render(request, 'accounts/index.html')


# register normal users
class register(View):
    """
    this view is used to register a new normal user and send an activation code to users phone number to activate
    their account.
    """
    from_class = register_form
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.from_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            is_phone_number_exist = User.objects.filter(phone_number=form.cleaned_data['phone_number'])
            if not is_phone_number_exist:
                user = User.objects.create_user(phone_number=form.cleaned_data['phone_number'],
                                                password=form.cleaned_data['password'],
                                                full_name=form.cleaned_data['full_name'],
                                                address=form.cleaned_data['address'],
                                                role='user')
                activation_code = random.randint(1000, 9999)
                ActivationCode.objects.create(phone_number=form.cleaned_data['phone_number'],
                                              activation_code=activation_code)
                store_info = store_activation_info(request, form.cleaned_data['phone_number'], activation_code)
                store_info.store_activation_info_in_session()
                user.save()
                messages.success(request, 'Account was successfully created, new lets activate your account')
                return redirect('accounts:activation')
            messages.error(request, "this phone already exists")
            return redirect('accounts:register')
        messages.error(request, 'information was Invalid, please try again')
        return redirect('accounts:register')


# active normal users account
class activation(View):
    """
    this view will get the verification code via form from the user and check it with the obj created in db with
     Activation_Code in thr model and if it was correct it will activate the user's account.
    """
    template_name = 'accounts/activation.html'
    form_class = activation_form

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            session_phone_number = request.session.get('activation_phone_number')
            activation_info = ActivationCode.objects.get(phone_number=session_phone_number)
            user = User.objects.get(phone_number=session_phone_number)
            if activation_info.activation_code == form.cleaned_data['activation_code']:
                user.is_active = True
                user.save()
                activation_info.delete()
                messages.success(request, 'Account was successfully activated')
                return redirect('accounts:home')
            messages.error(request, 'Incorrect activation code')
            return redirect('accounts:activation')
        messages.error(request, 'something went wrong')
        return redirect('accounts:activation')


# login via this view
class loginView(View):
    """
    this is a view to log users in
    """
    template_name = 'accounts/login.html'
    form_class = login_form

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.get(phone_number=form.cleaned_data['phone_number'])
            if user.is_active and user.password == form.cleaned_data['password']:
                login(request, user)
                messages.success(request, 'You are now logged in', 'success')
                return redirect('accounts:home')
            messages.error(request, 'we couldn\'t be able to verify you with this information')
            return redirect('accounts:login')
        messages.error(request, 'invalid credentials')
        return redirect('accounts:login')

# logout via this view
class logoutView(LoginRequiredMixin, View):
    """
    this is a view to log users out
    """

    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully')
        return redirect('accounts:home')
