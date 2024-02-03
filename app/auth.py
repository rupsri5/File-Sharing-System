import jwt
from datetime import datetime, timedelta
from File_Sharing_System.settings import SECRET_KEY
from django.http import JsonResponse
from rest_framework import status
from .models import User
import inspect

SECRET_KEY = SECRET_KEY

def generate_jwt_token(data):
    # Set the expiry time to 3 minutes from now
    expiry_time = datetime.utcnow() + timedelta(minutes=3)

    # Create the payload with data and expiry time
    payload = {
        'data': data,
        'exp': expiry_time
    }

    # Generate the JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token

def decode_jwt_token(token):

    # Decode the token
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    # Check if the token is expired
    if datetime.utcnow() > datetime.utcfromtimestamp(payload['exp']):
        raise jwt.ExpiredSignatureError("Token has expired")

    # Return the decoded data
    return payload['data']

    
    
def validate_token(fx):
    def wrapper(request, *args, **kwargs):
        headers=request.headers
        token = headers.get('token', None)
        
        if not token:
            return JsonResponse({"error": "Token not found"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            data=decode_jwt_token(token)
            user=User.objects.filter(id=data['user_id']).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            if 'user' in inspect.getfullargspec(fx).args:
                kwargs['user']=user
            return fx(request, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            # Handle expired token
            print("Token has expired")
            return JsonResponse({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.InvalidTokenError:
            # Handle invalid token
            print("Invalid token")
            return JsonResponse({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return wrapper