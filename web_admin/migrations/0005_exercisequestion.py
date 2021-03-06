# Generated by Django 2.1 on 2019-03-14 10:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0004_auto_20190314_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseQuestion',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('exercise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web_admin.Transaction_type')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_admin.Question')),
            ],
            options={
                'db_table': 'exercise_questions',
            },
        ),
    ]
