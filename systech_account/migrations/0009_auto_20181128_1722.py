# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-28 09:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('systech_account', '0008_auto_20181128_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('session_credits', models.DurationField(blank=True, null=True)),
                ('session_start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('session_end_date', models.DateTimeField(blank=True, null=True)),
                ('enrollment_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systech_account.Company')),
                ('company_rename', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='systech_account.Company_rename')),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'enrollments',
            },
        ),
        migrations.CreateModel(
            name='EnrollmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systech_account.Company')),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'enrollment_types',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('official_receipt_no', models.CharField(blank=True, max_length=15, null=True)),
                ('enrollment_form_no', models.CharField(blank=True, max_length=15, null=True)),
                ('payment_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('created_on', models.DateField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systech_account.Company')),
                ('enrollment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='systech_account.Enrollment')),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'payments',
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='systech_account.Company')),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'payment_types',
            },
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='systech_account.PaymentType'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='enrollment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='systech_account.EnrollmentType'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_enrolled', to='systech_account.School'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]