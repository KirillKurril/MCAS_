# Generated by Django 4.2.1 on 2023-05-12 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='department',
            field=models.CharField(choices=[('1', 'Фортепианное'), ('2', 'Струнно-смычковое'), ('3', 'Народное'), ('4', 'Струнно-народное'), ('5', 'Хоровое'), ('6', 'Теоретическое')], default='piano', max_length=20),
        ),
    ]
