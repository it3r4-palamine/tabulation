# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-11 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0046_auto_20171211_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction_type',
            name='program_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
