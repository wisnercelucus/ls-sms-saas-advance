from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import reverse


class Commentmanager(models.Manager):
    def all(self):
        return super(Commentmanager, self).filter(parent=None)
        
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(Commentmanager, self).filter(
                content_type=content_type, 
                object_id=obj_id).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, pk, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)

        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            print(SomeModel)
            obj_qs = SomeModel.objects.filter(pk=pk)
            if obj_qs.exists():
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
            return "Could note create it"
        return None


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = Commentmanager()

    class Meta:
        ordering=['-created_at']

    def children(self):
        return Comment.objects.filter(parent=self)

    def get_absolute_url(self):
        return reverse('feed:comments:comment_thread', kwargs={'pk':self.pk})

    def is_parent(self):
        if self.parent is not None:
            return False
        else:
            return True


    def __str__(self):
        return self.content

