from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import reverse


PRIORITIES = (
	('high', 'High'),
	('normal', 'Normal'),
	('low', 'Low'),
	)

STATUSES = (
	('not started', 'Not started'),
	('in progress', 'In progress'),
	('completed', 'Completed'),
	('waiting on someone else', 'Waiting on someone else'),
	('deffered', 'Deffered'),
	)



class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modifier',
        on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='doers')
    comment = models.TextField()
    status = models.CharField(choices=STATUSES, max_length=150)
    subject = models.CharField(max_length=250)
    priority = models.CharField(choices=PRIORITIES, max_length=150)
    reminder_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    class Meta:
    	ordering = ['-created_at']

    def __str__(self):
    	return self.subject
