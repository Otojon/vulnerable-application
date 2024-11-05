# jwt_vulnerabilities/views.py
from django.contrib.auth import logout, authenticate

from access_control.models import UserProfile
import jwt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib import messages

# Secret key for JWT encoding
SECRET_KEY = 'your_secret_key'  # Replace with a stronger key in production


# Register View - Creates a new user and sets their profile
@api_view(['GET', 'POST'])
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'register.html')

        # Create new user and assign a normal role by default
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, role='normal')

        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'register.html')


# Login View - Issues JWT token and stores it in a cookie
@api_view(['GET', 'POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

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
            response = redirect('home')  # Redirect to home page
            response.set_cookie('jwt', token, httponly=True, max_age=3600)  # Set HttpOnly cookie for 1 hour
            return response

        messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')


# Home View - Checks JWT from cookies to display user-specific info
@api_view(['GET'])
def home_view(request):
    # Retrieve JWT from cookies
    token = request.COOKIES.get('jwt')

    if not token:
        return redirect('login')

    try:
        # Decode JWT without verifying the signature
        decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=['HS256'])

        user_id = decoded.get('userID')
        username = decoded.get('username')
        is_admin = decoded.get('isAdmin')

        # Render home page with user information
        return render(request, 'home.html', {
            'userID': user_id,
            'username': username,
            'isAdmin': is_admin
        })

    except jwt.DecodeError:
        messages.error(request, 'Invalid token')
        return redirect('login')
    except jwt.ExpiredSignatureError:
        messages.error(request, 'Token has expired. Please log in again.')
        return redirect('login')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('login')


# Logout View - Clears the JWT cookie without using sessions
@api_view(['POST'])
def logout_view(request):
    response = redirect('login')
    response.delete_cookie('jwt')  # Remove the JWT cookie
    return response


# Admin-Only View - Access restricted to users with isAdmin set to true in JWT
@api_view(['GET'])
def admin_view(request):
    # Retrieve JWT from cookies
    token = request.COOKIES.get('jwt')

    if not token:
        return redirect('login')  # Redirect if no token is found

    try:
        # Decode JWT without verifying the signature (for testing vulnerability)
        decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=['HS256'])

        # Check if user is an admin
        is_admin = decoded.get('isAdmin')
        if is_admin:
            # Render admin page if user has admin privileges
            return render(request, 'admin.html')
        else:
            # Redirect non-admin users to login with a message
            messages.error(request, "You do not have permission to access the admin page.")
            return redirect('login')

    except jwt.DecodeError:
        messages.error(request, 'Invalid token')
        return redirect('login')
    except jwt.ExpiredSignatureError:
        messages.error(request, 'Token has expired. Please log in again.')
        return redirect('login')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('login')


        messages.error(request, str(e))
        return redirect('home')


from django.shortcuts import render, redirect
from django.contrib import messages
import jwt
from rest_framework.decorators import api_view

@api_view(['GET'])
def admin_view(request):
    # Retrieve JWT from cookies
    token = request.COOKIES.get('jwt')

    if not token:
        return redirect('login')  # Redirect if no token is found

    try:
        # Decode JWT without verifying the signature (for testing vulnerability)
        decoded = jwt.decode(token, options={"verify_signature": False}, algorithms=['HS256'])

        # Check if user is an admin
        is_admin = decoded.get('isAdmin')
        if is_admin:
            # Render admin page if user has admin privileges
            return render(request, 'admin.html')
        else:
            # Redirect non-admin users to login with a message
            messages.error(request, "You do not have permission to access the admin page.")
            return redirect('login')

    except jwt.DecodeError:
        messages.error(request, 'Invalid token')
        return redirect('login')
    except jwt.ExpiredSignatureError:
        messages.error(request, 'Token has expired. Please log in again.')
        return redirect('login')
    except Exception as e:
        messages.error(request, str(e))
        print("General Exception:", e)
        return redirect('login')
