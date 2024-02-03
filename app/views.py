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
        return JsonResponse({"message": "Success", "token": token})
    except InputException as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@csrf_exempt
@api_view(['POST'])
def file_upload(request):
    user_id = request.data.get('user_id_upload')
    user=User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error":"Invalid user"}, status=status.HTTP_400_BAD_REQUEST)
    if user.user_type=='client':
        return JsonResponse({"error":"Access Denied"}, status=status.HTTP_400_BAD_REQUEST)
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
        file_serializer.save(id=file_id)

        return JsonResponse(file_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def generate_download_link(request, id):
#     try:
#         file_obj = Files.objects.get(pk=id)
#         # Generate one-time downloadable link logic goes here

#         # For simplicity, just return the file URL for now
#         download_url = file_obj.file.url

#         response_data = {"downloadable_url": download_url, "message": "success"}
#         return JsonResponse(response_data)

#     except Files.DoesNotExist:
#         return JsonResponse({"message": "File not found"}, status=404)

@csrf_exempt
@api_view(['POST'])
def generate_download_link(request):
    file_id = request.data.get('file_id')
    user_id = request.data.get('user_id')
    
    file=Files.objects.filter(id=file_id).first()
    if not file and not file.file_present:
        return JsonResponse({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    user=User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error":"Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
    if user.user_type=='ops':
        return JsonResponse({"error": "You are not allowed to perform the operation"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    file_instance = get_object_or_404(Files, id=file_id)
    user_instance = get_object_or_404(User, id=user_id)
    download_history_instance = File_Download_History()
    download_history_instance.file_id=file_instance
    download_history_instance.user_id=user_instance
    # download_object=File_Download_History.objects.create(file_id=file_id, user_id=user_id)
    download_history_instance.save()
    download_url = request.build_absolute_uri(f'/download/{download_history_instance.download_id}')
    return JsonResponse({"link": download_url})

@csrf_exempt
@api_view(['POST'])
def download(request, uuid):
    user_id = request.data.get('user_id')
    
    user=User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error":"Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
    
    link=File_Download_History.objects.filter(download_id=uuid).first()
    if not link or link.file_downloaded:
        return JsonResponse({"error": "Invalid download link"}, status=status.HTTP_400_BAD_REQUEST)
    
    if link.user_id.id!=user_id:
        return JsonResponse({"error": "Access Denied"}, status=status.HTTP_400_BAD_REQUEST)
    
    link.file_downloaded=True
    link.save()
    
    file=Files.objects.filter(id=link.file_id.id).first()
    if not file and not file.file_present:
        return JsonResponse({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    with open(f'media/files/{file.id}.{file.file_type}', 'rb') as input_file:
        response=HttpResponse(input_file.read(), content_type="application/octet-stream")
        response['Content-Disposition']=f"attachment; filename={file.file}"
        return response
    
        
    
    
    
    
    # file_obj = Files.objects.get(id=id)
    
    # if not file_obj:
    #     return JsonResponse({"error": "File doesn't exists."})
    
    # file_path = os.path.join(settings.MEDIA_ROOT, str(file_obj.file))  
    
    # if os.path.exists(file_path):
    #     with open(file_path, 'rb') as file:
    #         response = HttpResponse(file.read(), content_type='application/octet-stream')
    #         response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
    #         return response
    # else:
    #     return JsonResponse({"error": "File not found"}, status=404)