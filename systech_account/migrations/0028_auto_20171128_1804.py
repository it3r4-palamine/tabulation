# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-28 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0027_display_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_intelex',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='session_credits',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='session_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
