# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-05 03:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0029_assessment_answer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment_answer_image',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
    ]