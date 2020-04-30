from django.shortcuts import render, redirect, get_object_or_404 
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.generic import DetailView
from user.models import User, Follow
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from user.forms import (
	UserRegistrationForm,
	ChangePasswordForm,
	)
from user.decorators import unauthenticated_user, allowed_users, admin_only
from django.views import View

class UserDetailView(DetailView, LoginRequiredMixin):
	queryset = User.objects.all()
	login_url = reverse_lazy('user:login')
	template_name = 'user/userprofile.html'

	def get_object(self):
		return get_object_or_404(
					User, 
					username__iexact=self.kwargs.get("username")
				)
	def own_profile(self):
		if self.get_object().username == self.request.user.username:
			return True
		else:
			return False

	def get_context_data(self, *args, **kwargs):
		context = super(UserDetailView, self).get_context_data(*args, **kwargs)
		following = Follow.objects.is_following(self.request.user, self.get_object())
		context['following'] = following
		context['own_profile'] = self.own_profile()
		return context

class UserFollowView(View, LoginRequiredMixin):
	login_url = reverse_lazy('user:login')

	def get(self, request, username, *args, **kwargs):
		toggle_user = get_object_or_404(User, username__iexact=self.kwargs.get("username"))
		is_following = Follow.objects.toggle_follow(request.user, toggle_user)
		return redirect("user:profile", username=username)


@login_required
def user_profile(request):
	user=request.user
	context = {'user': user}
	return render(request, 'user/userprofile.html')

@unauthenticated_user
def registerPage(request):
	form = UserRegistrationForm()
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		
	context = {'form':form}
	return render(request, 'user/register.html', context)

@unauthenticated_user
def LoginUser(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')
		context = {}
	return render(request, 'user/login.html', context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user:login')
    else:
    	form = ChangePasswordForm(user=request.user)
    	context = {'form': form}
    	return render(request, 'user/change_password.html', context)

@login_required
def logoutUser(request):
	logout(request)
	return redirect('user:login')










