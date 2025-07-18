from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register.as_view(), name='register'),
    path('activation/', views.activation.as_view(), name='activation'),
    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', views.logoutView.as_view(), name='logout'),
    path('add_staff/', views.add_staff.as_view(), name='add_staff'),
]
