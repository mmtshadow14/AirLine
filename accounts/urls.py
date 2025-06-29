from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('register/', views.register.as_view(), name='register'),
    path('activation/', views.activation.as_view(), name='activation'),
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout.as_view(), name='logout'),
]
