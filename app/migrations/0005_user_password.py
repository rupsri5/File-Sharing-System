# Generated by Django 5.0.1 on 2024-02-02 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='SOME STRING', max_length=50),
        ),
    ]
