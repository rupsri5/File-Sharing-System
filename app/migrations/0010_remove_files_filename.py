# Generated by Django 5.0.1 on 2024-02-03 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_download_status_file_download_history_file_downloaded_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='filename',
        ),
    ]