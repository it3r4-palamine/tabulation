# Generated by Django 2.1 on 2019-04-22 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0019_studentanswer_program'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='is_post_test',
            field=models.BooleanField(default=False),
        ),
    ]
