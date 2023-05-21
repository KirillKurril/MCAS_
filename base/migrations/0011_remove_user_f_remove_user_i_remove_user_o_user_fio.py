# Generated by Django 4.2.1 on 2023-05-21 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_file_author_file_department_file_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='f',
        ),
        migrations.RemoveField(
            model_name='user',
            name='i',
        ),
        migrations.RemoveField(
            model_name='user',
            name='o',
        ),
        migrations.AddField(
            model_name='user',
            name='fio',
            field=models.CharField(default='ФИО', max_length=200, verbose_name='ФИО'),
        ),
    ]
