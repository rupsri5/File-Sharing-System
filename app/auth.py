import jwt
from datetime import datetime, timedelta
from File_Sharing_System.settings import SECRET_KEY

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
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Check if the token is expired
        if datetime.utcnow() > datetime.utcfromtimestamp(payload['exp']):
            raise jwt.ExpiredSignatureError("Token has expired")

        # Return the decoded data
        return payload['data']

    except jwt.ExpiredSignatureError:
        # Handle expired token
        print("Token has expired")
        return None

    except jwt.InvalidTokenError:
        # Handle invalid token
        print("Invalid token")
        return None