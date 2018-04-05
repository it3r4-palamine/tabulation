# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-05 10:21
from __future__ import unicode_literals

from django.db import migrations

def delete_exercises(apps,schema_editor):
	Transaction_type = apps.get_model("systech_account","Transaction_type")
	Question = apps.get_model("systech_account","Assessment_question")

	transaction_types = Transaction_type.objects.all()
	for transaction_type in transaction_types:
		if transaction_type.exercise_id:
			if Question.objects.filter(transaction_type=transaction_type.pk,is_active=True).exists():
				continue
			else:
				transaction_type.is_active = False
				transaction_type.save()

class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0022_auto_20180402_1438'),
    ]

    operations = [
    	migrations.RunPython(delete_exercises)
    ]
