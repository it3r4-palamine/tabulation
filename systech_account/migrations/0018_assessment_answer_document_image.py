# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-09 08:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0017_auto_20171107_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessment_answer',
            name='document_image',
            field=models.ImageField(blank=True, null=True, upload_to=b'assessment/document_images/'),
        ),
    ]
