# Generated by Django 2.1 on 2019-04-22 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0018_studentanswer_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web_admin.Program'),
        ),
    ]