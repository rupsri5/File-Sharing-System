# Generated by Django 5.0.1 on 2024-02-03 06:53

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_download_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='download_link',
            name='file_id',
        ),
        migrations.RemoveField(
            model_name='download_link',
            name='user_id',
        ),
        migrations.CreateModel(
            name='File_Download_History',
            fields=[
                ('download_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('generation_date', models.DateTimeField(auto_now=True)),
                ('download_status', models.BooleanField(default=False)),
                ('file_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.files')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
            options={
                'db_table': 'file_download_history',
            },
        ),
        migrations.DeleteModel(
            name='Download_History',
        ),
        migrations.DeleteModel(
            name='Download_link',
        ),
    ]