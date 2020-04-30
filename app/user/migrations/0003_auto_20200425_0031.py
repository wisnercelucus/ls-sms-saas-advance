# Generated by Django 3.0.3 on 2020-04-25 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='target',
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(related_name='followed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
