from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.user_login, name='user_login'),
    path('signup', views.user_signup, name='user_signup'),
    path('file_upload', views.file_upload, name='file_upload'),
    path('generate_download_link', views.generate_download_link, name='generate_download_link'),
    path('download/<uuid:uuid>', views.download, name="download"),
    path('list_file', views.list_file, name="list_file"),
]
