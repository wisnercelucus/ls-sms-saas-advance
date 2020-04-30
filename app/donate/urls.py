from django.contrib import admin
from django.urls import path, include
from donate import views


app_name = 'donate'

urlpatterns = [
    path('', views.index, name='index'),
    path('process-donation/', views.charge_carte, name='process-donation'),
    path('thank-you/<str:args>/', views.thank_you, name='thank-you'),
]
