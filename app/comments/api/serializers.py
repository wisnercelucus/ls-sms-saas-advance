from rest_framework import serializers
from user.api.serializers import UserModelSerializer
from django.utils.timesince import timesince
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from comments.models import Comment
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

def comment_create_serializer(model_type='post', pk=None, parent_id=None, user=None):
	class CommentCreateSerializer(serializers.ModelSerializer):
		class Meta:
			model = Comment
			fields = [
				'id',
				'content',
				'created_at',
			]

		def __init__(self, *args, **kwargs):
			self.model_type = model_type
			self.pk = pk
			self.parent_obj = None
			if parent_id:
				parent_qs = Comment.objects.filter(pk=parent_id)
				if parent_qs.exists() and parent_qs.count() == 1:
					self.parent_obj = parent_qs.first()
			return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

		def validate(self, data):
			model_type = self.model_type
			model_qs = ContentType.objects.filter(model=model_type)
			if not model_qs.exists():
				raise serializers.ValidationError("This is not a valid content type")
			PostModel = model_qs.first().model_class()

			obj_qs = PostModel.objects.filter(pk=self.pk)
			if not obj_qs.exists():
				raise serializers.ValidationError("This is not a valid post")

			return data

		def create(self, validated_data):
			content = validated_data.get('content')
			self.model_type = model_type
			self.pk = pk
			main_user = None
			if user:
				main_user = user
			else:
				main_user = User.objects.all().first()

			parent_obj = self.parent_obj

			comment = Comment.objects.create_by_model_type(
				model_type, pk, content, main_user, parent_obj=parent_obj)
			comment
						
			return comment

	return CommentCreateSerializer


class CommentModelSerializer(serializers.ModelSerializer):
	user = UserModelSerializer(read_only=True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()
	reply_count = serializers.SerializerMethodField()
	#likes = serializers.SerializerMethodField()
	#did_like = serializers.SerializerMethodField()
	#redirect_ = serializers.SerializerMethodField()

	
	class Meta:
		model = Comment
		fields = [
			'user',
			'content',
			'created_at',
			'date_display',
			'timesince',
			'url',
			'content_type',
			'object_id',
			'reply_count',
			#'likes',
			#'did_like',
			#'redirect_',
		]

	#def get_redirect_(self, obj):
	#	return '/feed'

	#def get_did_like(self, obj):
	#	request = self.context.get("request")
	#	if request:
	#		if request.user.is_authenticated:
	#			if request.user in obj.liked.all():
	#				return True
	#	return False

	#def get_likes(self, obj):
	#	return obj.liked.all().count()

	def get_date_display(self, obj):
		return obj.created_at.strftime("%b %d, %Y at %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.created_at) + " ago"

	def get_url(self, obj):
		return reverse_lazy("feed:comments:comments-api:comment_thread", kwargs={"pk": obj.pk})

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0


class CommentChildSerializer(serializers.ModelSerializer):
	user = UserModelSerializer(read_only=True)
	
	class Meta:
		model = Comment
		fields = [
			'id',
			'user',
			'content',
			'created_at',
			'content_type',
			'object_id',

		]

class CommentDetailSerializer(serializers.ModelSerializer):
	user = UserModelSerializer(read_only=True)
	replies = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()
	content_object_url = serializers.SerializerMethodField()
	
	class Meta:
		model = Comment
		fields = [
			'id',
			'user',
			'content',
			'created_at',
			'url',
			'content_type',
			'object_id',
			'content_object_url',
			'replies',
			
		]

		read_only_fields =['content_type', 'object_id', 'replies']

	def get_content_object_url(self, obj):
		try:
			return obj.content_object.get_api_url()
		except:
			return None
		
	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True).data
		return None

	def get_url(self, obj):
		return reverse_lazy("feed:comments:comment_thread", kwargs={"pk": obj.pk})
