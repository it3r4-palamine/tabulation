# Generated by Django 2.1 on 2019-04-22 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0017_auto_20190405_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='enrollment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web_admin.Enrollment'),
        ),
    ]