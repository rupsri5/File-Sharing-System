# Generated by Django 5.0.1 on 2024-02-03 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_files_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file',
            field=models.CharField(max_length=50),
        ),
    ]
