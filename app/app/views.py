from django.shortcuts import render
from app.decorators import unauthenticated_user

@unauthenticated_user
def index(request):
	return render(request, 'pages/index.html')

@unauthenticated_user
def about(request):
	return render(request, 'pages/about.html')

@unauthenticated_user
def donors(request):
	return render(request, 'pages/donors.html')

@unauthenticated_user
def contact(request):
	return render(request, 'pages/contact.html')

# Errors handlers

def handler404(request):
	return render(request, 'errors/404.html')

def handler500(request):
	return render(request, 'errors/500.html')
