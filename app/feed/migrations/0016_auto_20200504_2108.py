# Generated by Django 3.0.3 on 2020-05-05 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0015_auto_20200504_2102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at'], 'verbose_name': 'post'},
        ),
    ]