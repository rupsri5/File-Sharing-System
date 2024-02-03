from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from app.models import User, Files, File_Download_History
from app.serializers import UserSerializer, FilesSerializer
from app.auth import generate_jwt_token
from File_Sharing_System.settings import SPECIAL_TOKEN
from .services import validate_input
from .constant import SIGNUP_INPUT, SIGNUP_INPUT_TEMP, LOGIN_INPUT
from .exception import InputException, TokenException
import uuid
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from .auth import validate_token


@csrf_exempt
@api_view(['POST'])
def user_signup(request):
    try:
        validate_input(request.data, SIGNUP_INPUT, SIGNUP_INPUT_TEMP)
        username = request.data.get('username')
        special_token = request.data.get('special_token')
        
        existing_user = User.objects.filter(username=request.data.get('username')).first()
        
        if existing_user:
            return JsonResponse({"error": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)    
        
        user_data = request.data.copy()
        if special_token:
            if special_token!=SPECIAL_TOKEN:
                raise TokenException()
            user_data['user_type']='ops'
            
                
        user_serializer=UserSerializer(data = user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token = generate_jwt_token({"user_id": user.id, "user_type": user.user_type})
            return JsonResponse({"message":f"{user.user_type} user signup successful.", "token": token}, status=status.HTTP_200_OK)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except InputException as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


@csrf_exempt
@api_view(['POST'])
def user_login(request):
    try:
        validate_input(request.data, LOGIN_INPUT)
        username = request.data.get('username')
        password = request.data.get('password')
        
        existing_user = User.objects.filter(username=username, password=password).first()
        
        if not existing_user:
            return JsonResponse({"errors": "Invalid Credentials."}, status=status.HTTP_400_BAD_REQUEST)
        token = generate_jwt_token({"user_id": existing_user.id, "user_type": existing_user.user_type})
        return JsonResponse({"message": f"Success, {existing_user.user_type} user logged in", "token": token})
    except InputException as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@csrf_exempt
@api_view(['POST'])
@validate_token
def file_upload(request, user):
    if user.user_type=='client':
        return JsonResponse({"error":"Access Denied for Client user"}, status=status.HTTP_400_BAD_REQUEST)
    if not request.FILES.get('file'):
        return JsonResponse({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    uploaded_file = request.FILES['file']
    request.data['file']=uploaded_file.name
    
    file_serializer = FilesSerializer(data=request.data)

    if file_serializer.is_valid():
        # Generate a unique filename using UUID
        file_id= str(uuid.uuid4())
        new_file_name= f"{file_id}.{uploaded_file.name.split('.')[-1].lower()}"
        
        default_storage.save(f'files/{new_file_name}', uploaded_file)
        file_serializer.save(id=file_id, user_id_upload=user, file_present=True)

        return JsonResponse(file_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@validate_token
def generate_download_link(request, user):
    file_id = request.data.get('file_id')
    
    file=Files.objects.filter(id=file_id).first()
    if not file or not file.file_present:
        return JsonResponse({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)
    

    if user.user_type=='ops':
        return JsonResponse({"error": "Ops user is not allowed to perform the operation"}, status=status.HTTP_400_BAD_REQUEST)
    
    download_object=File_Download_History.objects.create(file_id=file, user_id=user)
    download_url = request.build_absolute_uri(f'/download/{download_object.download_id}')
    return JsonResponse({"link": download_url})


@csrf_exempt
@api_view(['GET'])
@validate_token
def download(request, uuid, user):        
    link=File_Download_History.objects.filter(download_id=uuid).first()
    if not link or link.file_downloaded:
        return JsonResponse({"error": "Invalid download link"}, status=status.HTTP_400_BAD_REQUEST)
    
    if link.user_id.id!=user.id:
        return JsonResponse({"error": "Access Denied, this link is generated by other user"}, status=status.HTTP_400_BAD_REQUEST)
    
    link.file_downloaded=True
    link.save()
    
    file=Files.objects.filter(id=link.file_id.id).first()
    if not file or not file.file_present:
        return JsonResponse({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    with open(f'media/files/{file.id}.{file.file_type}', 'rb') as input_file:
        response=HttpResponse(input_file.read(), content_type="application/octet-stream")
        response['Content-Disposition']=f"attachment; filename={file.file}"
        return response
    
@csrf_exempt
@api_view(['GET'])
@validate_token
def list_file(request, user):
    if user.user_type=='ops':
        return JsonResponse({"error": "Ops user is not allowed to perform the operation"}, status=status.HTTP_400_BAD_REQUEST)
    files = Files.objects.all()
    serializer = FilesSerializer(files, many=True)
    return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@validate_token
def list_myfile(request, user):
    if user.user_type=='client':
        return JsonResponse({"error": "Client is not allowed to perform the operation"}, status=status.HTTP_400_BAD_REQUEST)
    files = Files.objects.filter(user_id_upload=user.id)
    serializer = FilesSerializer(files, many=True)
    return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['DELETE'])
@validate_token
def delete_myfile(request, user):
    if user.user_type=='client':
        return JsonResponse({"error": "Client is not allowed to perform the operation"}, status=status.HTTP_400_BAD_REQUEST)
    
    file_id = request.data.get('file_id')
    
    file=Files.objects.filter(id=file_id).first()
    if not file or not file.file_present:
        return JsonResponse({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    file=Files.objects.filter(id=file_id, user_id_upload=user).first()
    if not file and not file.file_present:
        return JsonResponse({"error": "Operation Failed, this file is not associated with you"}, status=status.HTTP_401_UNAUTHORIZED)
    
    file.file_present=False
    file.save()
    
    if default_storage.exists(f'files/{file.id}.{file.file_type}'):
        default_storage.delete(f'files/{file.id}.{file.file_type}')
        
    return JsonResponse({"message": f"File {file.file} deleted successfully"}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['DELETE'])
@validate_token
def delete_my_account(request, user):
    user.delete()
    return JsonResponse({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)
