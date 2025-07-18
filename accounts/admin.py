# django models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# employees app models
from .models import User, ActivationCode


# custom UserModel Admin
class CustomUserAdmin(UserAdmin):
    """
    custom user admin
    """
    model = User
    list_display = ['phone_number', 'is_staff', 'is_superuser', 'is_active', ]
    list_filter = ['phone_number', 'is_staff', 'is_superuser', 'is_active', ]
    fieldsets = [
        ('Authentication', {'fields': ('phone_number', 'full_name', 'password', 'role')}),
        ('Financial', {'fields': ('wallet',)}),
        ('User Role', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone_number", "full_name", "password1", "password2", "is_staff", "is_superuser",
                           "is_active"],
            },
        ),
    ]
    search_fields = ['phone_number', ]
    ordering = ['full_name', ]
    filter_horizontal = []


"""
Register your models here.
"""
# Register Models
admin.site.register(User, CustomUserAdmin)
admin.site.register(ActivationCode)
