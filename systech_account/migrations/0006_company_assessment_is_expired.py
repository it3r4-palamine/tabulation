# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-17 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0005_auto_20180809_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_assessment',
            name='is_expired',
            field=models.BooleanField(default=0),
        ),
    ]
