# Generated by Django 3.0.3 on 2020-05-09 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0017_option_poll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='post',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='feed.Post'),
        ),
    ]
