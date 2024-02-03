from django.db import models
import uuid
# from django.contrib.auth.models import AbstractUser

class User(models.Model):
    id = models.AutoField(primary_key=True)
    USER_TYPE = (
        ('ops', 'Operational User'),
        ('client', 'Client User'),
    )
    username = models.CharField(max_length =80, unique=True)
    password = models.CharField(max_length = 50, default="SOME STRING")
    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default='client')
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "user"


class Files(models.Model):
    FILE_TYPE = (
        ('pptx', 'Powerpoint file'),
        ('docx', 'Document/Word file'),
        ('xlsx', 'Excel file'),
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    file = models.CharField(max_length=50, blank=False)
    upload_date = models.DateTimeField(auto_now=True)
    user_id_upload = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='uploaded_files')
    file_present = models.BooleanField(default=True)
    user_id_delete = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='deleted_files')
    file_type=models.CharField(max_length=50, choices=FILE_TYPE, default='docx')

    def __str__(self):
        return self.filename
    
    class Meta:
        db_table = "files"

        
class File_Download_History(models.Model):
    download_id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    file_id = models.ForeignKey(Files, on_delete=models.CASCADE)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    generation_date=models.DateTimeField(auto_now=True)
    file_downloaded = models.BooleanField(default=False)
    
    class Meta:
        db_table = "file_download_history"