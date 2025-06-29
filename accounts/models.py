# django modules
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """
    a manager for our custom user model
    """

    def create_user(self, phone_number, password, **extra_fields):
        """
        creates a normal user
        """
        if not phone_number:
            raise ValueError('Users must have an email address')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        creates a superuser via the terminal
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom user model that uses phone number instead of username
    """
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=255)
    wallet = models.BigIntegerField(default=0)
    address = models.TextField()
    role = models.CharField(max_length=255)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.phone_number


class ActivationCode(models.Model):
    """
    we save activation code for user with this model
    """
    phone_number = models.CharField(max_length=11, unique=True)
    activation_code = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number
