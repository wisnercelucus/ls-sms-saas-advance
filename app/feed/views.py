from django.shortcuts import render, redirect, get_object_or_404 
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

from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from comments.forms import CommentForm


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

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		instance = kwargs['object']

		intial_data = {
				'content_type': instance.get_content_type,
				'object_id': instance.id
		}

		comment_form = CommentForm(initial=intial_data)
		context['comment_form'] = comment_form
		return context

	def post(self, request, *args, **kwargs):
		instance = self.queryset.filter(pk=kwargs['pk']).first()

		if request.user.is_authenticated:
			form = CommentForm(request.POST or None)
			if form.is_valid():
				c_type = form.cleaned_data.get('content_type')
				c_type = c_type.split('|')[1].strip()
				content_type = ContentType.objects.get(model=c_type)
				obj_id = form.cleaned_data.get('object_id')
				content = form.cleaned_data.get('content')
				parent_obj = None
				try:
					parent_id = int(request.POST.get("parent_id"))
				except:
					parent_id = None
				if parent_id:
					parent_qs = Comment.objects.filter(pk=parent_id)
					if parent_qs.exists():
						parent_obj = parent_qs.first()
				new_comment , created = Comment.objects.get_or_create(
					user=request.user,
					content_type=content_type,
					object_id=obj_id,
					content=content,
					parent=parent_obj
					)
				return redirect("feed:detail_post", pk=kwargs['pk'])
			else:
				print(form.errors)
		return HttpResponseRedirect("/feed")


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