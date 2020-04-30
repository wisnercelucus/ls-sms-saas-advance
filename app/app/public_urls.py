from django.contrib import admin
from django.urls import path, include
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('donors/', views.donors, name='donors'),
    path('donate/', include('donate.urls')),
    path('contact/', views.contact, name='contact'),
    path('prospect/',  include('customer.urls')),
]
