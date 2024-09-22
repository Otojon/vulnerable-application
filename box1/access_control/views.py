# access_control/views.py

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .models import UserProfile,User

# Middleware to handle Basic Authentication
def basic_auth(request):
    auth = request.META.get('HTTP_AUTHORIZATION')
    if auth and auth.startswith('Basic'):
        import base64
        base64_credentials = auth.split()[1]
        credentials = base64.b64decode(base64_credentials).decode('utf-8')
        username, password = credentials.split(':')
        user = authenticate(username=username, password=password)
        if user:
            return user
    return None

# Login API (returns user's role)
@api_view(['POST'])
def login_user(request):
    user = basic_auth(request)
    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=403)
    
    # Get the user's role from UserProfile
    user_profile = UserProfile.objects.get(user=user)
    return JsonResponse({'message': f'Welcome, {user.username}!', 'role': user_profile.role})

# Privilege escalation ("Make-Me" functionality)
@api_view(['POST'])
def make_me_admin(request):
    user = basic_auth(request)
    if not user:
        return JsonResponse({'error': 'Authentication failed'}, status=403)
    
    # Vulnerable: Any user can change their own role
    target_user = request.data.get('target_user')
    new_role = request.data.get('new_role', 'normal')

    try:
        target = User.objects.get(username=target_user)
        target_profile = UserProfile.objects.get(user=target)
        target_profile.role = new_role
        target_profile.save()
        return JsonResponse({'message': f'{target_user} is now {new_role}'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
