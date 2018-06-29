# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-21 08:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0033_assessment_answer_image_is_sync'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson_update_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lesson_update_detail',
            },
        ),
        migrations.CreateModel(
            name='Lesson_update_header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'lesson_update_header',
            },
        ),
        migrations.RemoveField(
            model_name='user_lesson_update',
            name='to_dos_topic',
        ),
        migrations.RemoveField(
            model_name='user_lesson_update',
            name='user',
        ),
        migrations.DeleteModel(
            name='User_lesson_update',
        ),
        migrations.AddField(
            model_name='lesson_update_detail',
            name='lesson_update_header',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systech_account.Lesson_update_header'),
        ),
        migrations.AddField(
            model_name='lesson_update_detail',
            name='to_dos_topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systech_account.To_dos_topic'),
        ),
    ]