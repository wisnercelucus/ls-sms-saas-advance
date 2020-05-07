from django.shortcuts import render, redirect, get_object_or_404
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required


@login_required
def comment(request, pk):

	if request.method == 'POST':
		if request.user.is_authenticated:
			form = CommentForm(request.POST or None)
			if form.is_valid():
				c_type = form.cleaned_data.get('content_type')
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

				return redirect('/feed')
			else:
				print(form.errors)
				return redirect('/feed')
	return redirect('/feed')


@login_required
def comment_thread(request, pk):

	if request.method == 'POST':
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

				return redirect(parent_obj.get_absolute_url())
			else:
				print(form.errors)

	obj = get_object_or_404(Comment, pk=pk)
	intial_data = {
				'content_type': obj.content_type,
				'object_id': obj.object_id
	}

	form = CommentForm(initial=intial_data)

	context = {'comment': obj, 'comment_form': form}
	return render(request, 'comments/comment_thread.html', context)
