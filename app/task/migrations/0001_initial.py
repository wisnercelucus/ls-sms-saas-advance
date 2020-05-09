# Generated by Django 3.0.3 on 2020-05-08 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField()),
                ('status', models.CharField(choices=[('not started', 'Not started'), ('in progress', 'In progress'), ('completed', 'Completed'), ('waiting on someone else', 'Waiting on someone else'), ('deffered', 'Deffered')], max_length=150)),
                ('subject', models.CharField(max_length=250)),
                ('priority', models.CharField(choices=[('high', 'High'), ('normal', 'Normal'), ('low', 'Low')], max_length=150)),
                ('reminder_date', models.DateTimeField(blank=True, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('assigned_to', models.ManyToManyField(related_name='doers', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modifier', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]