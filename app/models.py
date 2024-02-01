from django.db import models
# from django.contrib.auth.models import AbstractUser

class User(models.Model):
    id = models.AutoField(primary_key=True)
    USER_TYPE = (
        ('ops', 'Operational User'),
        ('client', 'Client User'),
    )
    username = models.CharField(max_length =80, unique=True)
    email = models.EmailField(max_length=150)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default='client')
    email_verified = models.BooleanField(default=False)
    special_token = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "user"


class Files(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=100)
    file = models.FileField(upload_to='files')
    upload_date = models.DateTimeField(auto_now=True)
    user_id_upload = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='uploaded_files')
    file_present = models.BooleanField(default=True)
    user_id_delete = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='deleted_files')

    def __str__(self):
        return self.filename
    
    class Meta:
        db_table = "files"


class Download_History(models.Model):
    id = models.AutoField(primary_key=True)
    download_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file = models.ForeignKey(Files, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.file.filename} - {self.download_datetime}"
    
    class Meta:
        db_table = "download_history"