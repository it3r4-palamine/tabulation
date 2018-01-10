# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-10 05:30
from __future__ import unicode_literals

from django.db import migrations
from ..views.common import *

def delete_dbs(apps,schema_editor):
	table_names = [
		'Company_assessment',
		'Assessment_upload_answer',
		'Assessment_session'
	]

	for table_name in table_names:
		table = str2model(table_name).objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0007_assessment_score_uploaded_question'),
    ]

    operations = [
    	migrations.RunPython(delete_dbs)
    ]
