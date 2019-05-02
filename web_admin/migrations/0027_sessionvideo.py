# Generated by Django 2.1 on 2019-05-02 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_admin', '0026_exercisevideo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_admin.Session')),
            ],
            options={
                'db_table': 'session_videos',
            },
        ),
    ]
