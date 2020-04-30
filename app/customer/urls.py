from django.urls import path
from customer import views

app_name = 'customer'
urlpatterns = [
    path('register/', views.registerProspect, name='register'),
    path('register/success', views.registerSuccess, name='register_success'),
]
