# Generated by Django 5.0.1 on 2024-02-03 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_files_file_present'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file_present',
            field=models.BooleanField(default=True),
        ),
    ]
