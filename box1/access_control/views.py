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

# Login API (returns user's role)  ,  path('sandbox1/login/', login_user, name='login-user')
@api_view(['POST'])
def login_user(request):
    user = basic_auth(request)
    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=403)
    
    # Get the user's role from UserProfile
    user_profile = UserProfile.objects.get(user=user)
    return JsonResponse({'message': f'Welcome, {user.username}!', 'role': user_profile.role})


# Privilege escalation ("change user role" functionality , supposed to work for admin only) ,  path('sandbox1/change-user-role/', change_user_role, name='change-user-role'),  # Updated URL
@api_view(['POST'])
def change_user_role(request):
    user = basic_auth(request)
    if not user:
        return JsonResponse({'error': 'Authentication failed'}, status=403)
    
    # Get the target user and the new role
    target_user = request.data.get('target_user')
    new_role = request.data.get('new_role')

    # Ensure that only "admin" or "normal" are accepted as valid roles
    if new_role not in ['admin', 'normal']:
        return JsonResponse({'error': 'Invalid role. Role must be either "admin" or "normal".'}, status=400)

    # Update the user's role
    try:
        target = User.objects.get(username=target_user)
        target_profile = UserProfile.objects.get(user=target)
        target_profile.role = new_role
        target_profile.save()
        return JsonResponse({'message': f'{target_user} is now {new_role}'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

#   path('sandbox1/fetch-user-details/', fetch_user_details, name='fetch-user-details'),
@api_view(['GET'])
def fetch_user_details(request):
    # Fetch user details by user ID (vulnerable to IDOR)
    target_user_id = request.GET.get('user_id')

    try:
        target_user = User.objects.get(id=target_user_id)
        target_profile = UserProfile.objects.get(user=target_user)

        # Add an IDOR flag for a specific user (simulated)
        flag = "IDOR_FLAG_12345" if target_user.username == "idor_target" else None

        # Return user details, including password hash and last login
        return JsonResponse({
            'username': target_user.username,
            'password_hash': target_user.password,
            'last_login': target_user.last_login,
            'role': target_profile.role,
            'flag': flag
        })

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


# endpoint for admin panel access 
@api_view(['POST'])
def admin_panel(request):
    user = basic_auth(request)
    if not user:
        return JsonResponse({'error': 'Authentication failed'}, status=403)

    user_profile = UserProfile.objects.get(user=user)
    
    # Only allow access if the logged-in user is an admin
    if user_profile.role != 'admin':
        return JsonResponse({'error': 'Permission denied: Admins only.'}, status=403)
    
    # Get the action type (delete, edit, or change_role)
    action = request.data.get('action')
    target_user_id = request.data.get('user_id')

    try:
        target_user = User.objects.get(id=target_user_id)
        target_profile = UserProfile.objects.get(user=target_user)

        if action == 'delete':
            target_user.delete()
            return JsonResponse({'message': f'User {target_user_id} deleted.'})

        elif action == 'edit':
            new_username = request.data.get('new_username')
            if new_username:
                target_user.username = new_username
                target_user.save()
                return JsonResponse({'message': f'User {target_user_id} username updated.'})
            else:
                return JsonResponse({'error': 'No new username provided.'}, status=400)

        elif action == 'change_role':
            new_role = request.data.get('new_role')
            if new_role not in ['admin', 'normal']:
                return JsonResponse({'error': 'Invalid role. Role must be either "admin" or "normal".'}, status=400)
            
            target_profile.role = new_role
            target_profile.save()
            return JsonResponse({'message': f'User {target_user_id} role changed to {new_role}.'})

        else:
            return JsonResponse({'error': 'Invalid action.'}, status=400)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)

#for updating profile of the user which is vulnerable to BAC
# access_control/views.py

@api_view(['POST'])
def update_profile(request):
    user = basic_auth(request)
    if not user:
        return JsonResponse({'error': 'Authentication failed'}, status=403)
    
    # The vulnerable part: user can specify a target user ID to update their profile
    target_user_id = request.GET.get('user_id')
    
    try:
        target_user = User.objects.get(id=target_user_id)
        new_username = request.data.get('new_username')

        # Allow users to update the username only
        if new_username:
            target_user.username = new_username
            target_user.save()
            return JsonResponse({'message': f'Username updated for user {target_user_id}'})
        else:
            return JsonResponse({'error': 'No new username provided.'}, status=400)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found.'}, status=404)
