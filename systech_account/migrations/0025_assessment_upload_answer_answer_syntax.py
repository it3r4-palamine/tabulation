# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-15 02:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0024_auto_20180503_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment_upload_answer',
            name='answer_syntax',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]