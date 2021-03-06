# Generated by Django 2.1 on 2019-03-20 06:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0007_auto_20190314_2123'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transaction_type',
            new_name='Exercise',
        ),
        migrations.RenameModel(
            old_name='SessionExercise',
            new_name='StudentSessionExercise',
        ),
        migrations.AlterField(
            model_name='assessment_question',
            name='transaction_types',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(verbose_name='Exercise'), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='company_assessment',
            name='transaction_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(verbose_name='Exercise'), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='company_rename',
            name='transaction_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(verbose_name='Exercise'), blank=True, null=True, size=None),
        ),
    ]
