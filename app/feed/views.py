from django.shortcuts import render, get_object_or_404 
from django.views.generic import (
	CreateView,
	DeleteView,
	DetailView, 
	ListView, 
	UpdateView,
	)
from .models import Post, HashTag
from .forms import PostModelForm
from django.forms.utils import ErrorList
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.views import View
from django.http import HttpResponseRedirect


class PostCreateView(LoginRequiredMixin, CreateView):
	form_class = PostModelForm
	template_name = 'feed/add_new_post.html'
	login_url = reverse_lazy('user:login')
	success_url = reverse_lazy('feed:home')

	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.user = self.request.user
			return super(PostCreateView, self).form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be login to continue"])
			return self.form_invalid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
	queryset = Post.objects.all()
	form_class = PostModelForm
	template_name = 'feed/update_post.html'
	login_url = reverse_lazy('user:login')
	success_url = reverse_lazy('feed:create_post')


class PostDeleteView(DeleteView):
	model = Post
	template_name = 'feed/delete_post_confirm.html'
	success_url = reverse_lazy('feed:home')

class PostListView(LoginRequiredMixin, ListView):
	login_url = reverse_lazy('user:login')
	template_name = 'feed/index.html'

	def get_queryset(self, *args, **kwargs):
		query = self.request.GET.get('q', None)
		in_following = self.request.user.profile.get_following()
		qs1 = Post.objects.filter(user__in=in_following)
		qs2 = Post.objects.filter(user=self.request.user)
		qs = (qs1 | qs2).distinct().order_by("-created_at")
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				)
			return qs
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(PostListView, self).get_context_data(*args, **kwargs)
		context['form'] = PostModelForm()
		context['create_url'] = reverse_lazy('feed:create_post')
		return context


class PostDetailView(LoginRequiredMixin, DetailView):
	login_url = reverse_lazy('user:login')
	template_name = 'feed/post_detail.html'

	queryset = Post.objects.all()


class PostShareView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        new_post = Post.objects.share(request.user, post)
        return HttpResponseRedirect("/feed")


class HashTagView(LoginRequiredMixin, View):
	login_url = reverse_lazy('user:login')
	template_name = 'feed/hash_tag.html'

	def get(self, request, hashtag, *args, **kwargs):
		obj, created = HashTag.objects.get_or_create(tag=hashtag)
		context = {"obj":obj}
		return render(request, self.template_name, context)