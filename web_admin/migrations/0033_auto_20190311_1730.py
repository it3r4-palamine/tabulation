# Generated by Django 2.1 on 2019-03-11 09:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0032_auto_20190311_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsession',
            name='session_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
