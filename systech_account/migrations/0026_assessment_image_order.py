# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-22 06:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0025_assessment_upload_answer_answer_syntax'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment_image',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]