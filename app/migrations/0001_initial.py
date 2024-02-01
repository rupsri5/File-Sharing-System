# Generated by Django 5.0.1 on 2024-02-01 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=80, unique=True)),
                ('email', models.EmailField(max_length=150)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('user_type', models.CharField(choices=[('ops', 'Operational User'), ('client', 'Client User')], default='client', max_length=50)),
                ('email_verified', models.BooleanField(default=False)),
                ('special_token', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='files')),
                ('upload_date', models.DateTimeField(auto_now=True)),
                ('file_present', models.BooleanField(default=True)),
                ('user_id_delete', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_files', to='app.user')),
                ('user_id_upload', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_files', to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='DownloadHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('download_datetime', models.DateTimeField(auto_now=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.files')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.user')),
            ],
        ),
    ]