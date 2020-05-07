import uuid
import os

from django.db import models
#from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AbstractUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_delete, post_save


def user_profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profile/', filename)


class UserManager(AbstractUserManager):
    """"Use this class to manage user related features"""
    def create_user(self, username, email, password=None, **kwargs):
        """This function create a new User"""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.username = username
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    image =  models.ImageField(null=True, upload_to=user_profile_image_path)
    phone = models.IntegerField(default=0, null=True)
    bio = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()


class FollowManager(models.Manager):
    use_for_related_fields = True
    def all(self):
        qs = self.get_queryset().all()
        try:     
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = Follow.objects.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            is_following = True
        else:
            user_profile.following.add(to_toggle_user)
            is_following = False
        return is_following

    def is_following(self, user, followed_by_user):
        user_profile, created = Follow.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

#Steam related class
class Follow(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='followed_by')

    objects = FollowManager()

    def __str__(self):
        return self.user.username


    def get_following(self):
        return self.following.all().exclude(username=self.user)

    def get_follow_url(self):
        return reverse_lazy("user:follow", kwargs={"username":self.user.username})

    def get_absolute_url(self):
        return reverse_lazy("user:profile", kwargs={"username":self.user.username})


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = Follow.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)