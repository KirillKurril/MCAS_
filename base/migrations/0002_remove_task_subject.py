# Generated by Django 4.2.1 on 2023-05-14 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='subject',
        ),
    ]
