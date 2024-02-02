from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from app.models import User, Files, Download_History
from app.serializers import UserSerializer, FilesSerializer, Download_HistorySerializer
from app.auth import generate_jwt_token
from File_Sharing_System.settings import SPECIAL_TOKEN
from .services import validate_input
from .constant import SIGNUP_INPUT, SIGNUP_INPUT_TEMP, LOGIN_INPUT
from .exception import InputException, TokenException


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
