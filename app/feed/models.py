import uuid
import os
from django.db import models
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.db.models.signals import post_save
import re
from feed.signals import parsed_hashtags
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

def user_feed_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/feed/', filename)

class PostManager(models.Manager):
    def share(self, user, parent_obj):
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj

        qs = self.get_queryset().filter(
                user=user, parent=og_parent
                ).filter(
                    created_at__year=timezone.now().year,
                    created_at__month=timezone.now().month,
                    created_at__day=timezone.now().day,
                )

        if qs.exists():
        	return None

        obj = self.model(
                parent = og_parent,
                user = user,
                content = parent_obj.content,
            )
        obj.save()

        return obj

    def like_toggle(self, user, post_obj):
        if user in post_obj.liked.all():
            is_liked = False
            post_obj.liked.remove(user)
            likes = post_obj.liked.all().count()
        else:
            is_liked = True
            post_obj.liked.add(user)
            likes = post_obj.liked.all().count()
        return (is_liked, likes)


class Post(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    #content = models.TextField(max_length=250)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    image =  models.ImageField(null=True, blank=True, upload_to=user_feed_image_path)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("feed:detail_post", kwargs={"pk":self.pk})

    def get_api_url(self):
        url = reverse("feed:feed-api:detail_post", kwargs={"pk":self.pk})
        print('get-call' + url)
        return url

    @property
    def comments(self):
        instance = self
        return Comment.objects.filter_by_instance(instance)

    @property
    def total_comments(self):
        instance = self
        return len(Comment.objects.filter(object_id=instance.id))

    @property
    def get_content_type(self):
        instance = self
        return ContentType.objects.get_for_model(instance.__class__)

    objects = PostManager()

    class Meta:
        ordering =["-created_at"]
        verbose_name = "post"


class HashTag(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(blank=True, null=True)
	tag = models.CharField(max_length=80)
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.tag

	def get_posts(self):
		return Post.objects.filter(
			Q(content__icontains='#' + self.tag)
			)
        

def post_save_receiver(sender, instance, created, *args, **kwargs):
    if created and not instance.parent:
        # notify a user
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.content)
        print(usernames)
        # send notification to user here.

        hash_regex = r'#(?P<hashtag>[\w\d-]+)'
        hashtags = re.findall(hash_regex, instance.content)
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)

def parsed_hashtags_receiver(sender, hashtag_list, *args, **kwargs):
    if len(hashtag_list) > 0:
        for tag_var in hashtag_list:
            new_tag, create = HashTag.objects.get_or_create(tag=tag_var)


post_save.connect(post_save_receiver, sender=Post)
parsed_hashtags.connect(parsed_hashtags_receiver)
