# Generated by Django 2.1 on 2019-03-21 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0012_courseprogram'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web_admin.Course'),
        ),
    ]
