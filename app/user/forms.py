from django.contrib.auth.forms import (
	UserCreationForm, 
	PasswordChangeForm,
	)
from user.models import User
from django import forms

class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class ChangePasswordForm(PasswordChangeForm):
	model = User