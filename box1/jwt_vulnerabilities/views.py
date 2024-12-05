# views.py
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
SECRET_KEY = 'mine'
from django.shortcuts import redirect, render

from django.shortcuts import render

@api_view(['GET'])
def home_view(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect

@api_view(['GET', 'POST'])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            payload = {
                'userID': user.id,
                'username': user.username,
                'isAdmin': user.userprofile.role == 'admin',
                'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            response = redirect('/profile/')  # Redirect to the profile page
            response.set_cookie('jwt', token, httponly=True, max_age=3600)  # Set the token in a cookie
            return response
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

@api_view(['GET'])
def profile_view(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        decoded = jwt.decode(token, SECRET_KEY, options={"verify_signature": False}, algorithms=['HS256'])
        context = {
            'username': decoded.get('username'),
            'isAdmin': decoded.get('isAdmin')
        }
        return render(request, 'profile.html', context)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Token has expired. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def admins(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        decoded = jwt.decode(token, SECRET_KEY, options={"verify_signature": False}, algorithms=['HS256'])
        if decoded.get('isAdmin'):
            context = {'username': decoded.get('username')}
            return render(request, 'admin.html', context)
        else:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Token has expired. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def admin2(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        decoded = jwt.decode(token, SECRET_KEY, options={"verify_signature": False}, algorithms=['HS256'])
        if decoded.get('isAdmin'):
            context = {'username': decoded.get('username')}
            return render(request, 'admin2.html', context)
        else:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Token has expired. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)