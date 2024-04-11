
# File-Sharing-System Project
The File Sharing System Project is a robust Django and Python-based REST API built on the Django Rest Framework. This system facilitates the secure and efficient sharing of files among users within a controlled environment. It ensures that only operational users can upload files and client users only download files, thereby maintaining data integrity and access control.

# Introduction
Powered by Django and Django Rest Framework, this project offers a versatile and scalable solution for managing file sharing operations. Leveraging the flexibility of Python, it provides a robust backend infrastructure capable of handling various user interactions and file management tasks. With SQLite as the underlying database, the system ensures data persistence and reliability while keeping the setup process straightforward and hassle-free.

You can learn more about [Django](https://docs.djangoproject.com/en/5.0/) and [Django Rest Framework](https://www.django-rest-framework.org/) to deepen your understanding of the technologies driving the File Sharing System Project.

# Key Features
- **User Authentication:** Users are required to sign up and log in before accessing the file sharing functionalities.

- **Access Control:** Differentiate between operational and client users to control who can upload and download files. Operational users have the privilege to upload files, while client users can only download files.

- **File Upload and Download:** Seamlessly upload files to the system for sharing purposes, and securely download files as needed. All file transfers are facilitated through the RESTful API endpoints, ensuring compatibility with various client applications.

- **Download link generation:** When client request for download API will generate a secure download link using [UUIDs](https://docs.python.org/3/library/uuid.html), this is one time download link and can not be used again. 

# Requirements
- Python 3.x
- Django
- Django Rest Framework

# Installation

1. **Clone the repository:**
```powershell
git clone git@github.com:rupsri5/File-Sharing-System.git
```
2. **Navigate to the project directory:**
```powershell
cd file-sharing-system
```
3. **Create virtual environemt:**
```powershell
python -m venv venv
```
Activate environment:

In powershell:
```powershell
venv/scripts/Activate
```
In git bash:
```powershell
venv/bin/activate
```
4. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

5. **Apply migrations:**
```powershell
python manage.py makemigrations
```
```powershell
python manage.py migrate
```

## Usage

1. Start the Django development server:
```powershell
python manage.py runserver
```
or use postman

2. Access the API endpoints:
- **POST:** User Signup: /signup
- **POST:** User Login: /login
- **POST:** File Upload: /file_upload
- **POST:** Download Link: /generate_download_link
- **GET:** File Download: /download/<secure_download_link>
- **GET:** List Files: /list_file
- **GET:** List client's downloaded Files: /list_myfile
- **DELETE:** Delete File: /delete_myfile
- **DELETE:** Delete user account: /delete_my_account

## Authentication
User signup is required before accessing any functionalities.
Upon successful login/signup, a new JWT token is generated for limited time and will expire after that time. This token is essential for accessing protected endpoints and performing actions within the system.
Authentication for uploading files is restricted to operational users.
Only client users can download files.
