from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from access_control.models import UserProfile
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Secret key for JWT encoding (Replace with a stronger key in production)
SECRET_KEY = 'your_secret_key'


# Register Endpoint - Creates a new user and sets their profile
@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    # Create new user and assign a normal role by default
    user = User.objects.create_user(username=username, password=password)
    UserProfile.objects.create(user=user, role='normal')

    return Response({'success': 'Account created successfully'}, status=status.HTTP_201_CREATED)


# Login Endpoint - Issues JWT token and stores it in a cookie
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        # Create the JWT token payload
        payload = {
            'userID': user.id,
            'username': user.username,
            'isAdmin': user.userprofile.role == 'admin',
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        }

        # Encode JWT token
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # Set JWT token in an HttpOnly cookie
        response = Response({'message': 'Login successful', 'token': token}, status=status.HTTP_200_OK)
        response.set_cookie('jwt', token, httponly=True, max_age=3600)  # Set HttpOnly cookie for 1 hour
        return response

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Home Endpoint - Checks JWT from cookies to display user-specific info
@api_view(['GET'])
def home_view(request):
    # Retrieve JWT from cookies
    token = request.COOKIES.get('jwt')

    if not token:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Decode JWT without verifying the signature (for testing vulnerability)
        decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=['HS256'])

        user_data = {
            'userID': decoded.get('userID'),
            'username': decoded.get('username'),
            'isAdmin': decoded.get('isAdmin')
        }

        return Response(user_data, status=status.HTTP_200_OK)

    except jwt.ExpiredSignatureError:
        return Response({'error': 'Token has expired. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


# Admin-Only Endpoint - Access restricted to users with isAdmin set to true in JWT
@api_view(['GET'])
def admin_view(request):
    # Retrieve JWT from cookies
    token = request.COOKIES.get('jwt')

    if not token:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Decode JWT without verifying the signature (for testing vulnerability)
        decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=['HS256'])

        # Check if user is an admin
        is_admin = decoded.get('isAdmin')
        if is_admin:
            return Response({'message': 'Welcome to the admin page'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

    except jwt.ExpiredSignatureError:
        return Response({'error': 'Token has expired. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


# Logout Endpoint - Clears the JWT cookie without using sessions
@api_view(['POST'])
def logout_view(request):
    response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    response.delete_cookie('jwt')  # Remove the JWT cookie
    return response
