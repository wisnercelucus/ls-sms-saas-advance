from rest_framework import serializers
from user.api.serializers import UserModelSerializer
from django.utils.timesince import timesince
from django.urls import reverse_lazy
from feed.models import Post
from comments.models import Comment
from comments.api.serializers import (CommentModelSerializer, CommentChildSerializer, 
	CommentDetailSerializer,
	)


class ParentPostModelSerializer(serializers.ModelSerializer):
	user = UserModelSerializer(read_only=True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()

	class Meta:
		model = Post
		fields = [
			'id',
			'user',
			'content',
			'created_at',
			'date_display',
			'timesince',
			'url',
			'image',
		]


	def get_date_display(self, obj):
		return obj.created_at.strftime("%b %d, %Y at %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.created_at) + " ago"

	def get_url(self, obj):
		return reverse_lazy("feed:detail_post", kwargs={"pk": obj.pk})


class PostModelSerializer(serializers.ModelSerializer):
	user = UserModelSerializer(read_only=True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()
	parent = ParentPostModelSerializer(read_only=True)
	likes = serializers.SerializerMethodField()
	did_like = serializers.SerializerMethodField()
	redirect_ = serializers.SerializerMethodField()
	comments = serializers.SerializerMethodField()
	total_comments = serializers.SerializerMethodField()

	
	class Meta:
		model = Post
		fields = [
			'id',
			'user',
			'content',
			'created_at',
			'date_display',
			'total_comments',
			'timesince',
			'url',
			'parent',
			'likes',
			'did_like',
			'image',
			'redirect_',
			'comments',
			
		]

	def get_redirect_(self, obj):
		return '/feed'

	def get_did_like(self, obj):
		request = self.context.get("request")
		if request:
			if request.user.is_authenticated:
				if request.user in obj.liked.all():
					return True
		return False

	def get_likes(self, obj):
		return obj.liked.all().count()

	def get_date_display(self, obj):
		return obj.created_at.strftime("%b %d, %Y at %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.created_at) + " ago"

	def get_url(self, obj):
		return reverse_lazy("feed:detail_post", kwargs={"pk": obj.pk})

	def get_comments(self, obj):
		content_type = obj.get_content_type
		object_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentModelSerializer(c_qs, many=True).data
		return comments

	def get_total_comments(self, obj):
		return len(Comment.objects.filter(object_id=obj.id))

	def update(self, instance, validated_data):
		"""Update a user, setting the password correctly and return it"""
		
		post = super().update(instance, validated_data)

		return post



