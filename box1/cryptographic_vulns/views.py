from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.models import User
from cryptographic_vulns.models import UserProfile
from rest_framework.decorators import api_view
import hashlib
import time

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        return JsonResponse({'message': 'Login successful', 'username': user.username})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=403)
@api_view(['GET'])
def profile_view(request):
    username = request.GET.get('username')

    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)

        # Return profile information with the flag for the admin
        return JsonResponse({
            'username': user.username,
            'role': profile.role,
            'flag': profile.flag if profile.role == 'admin' else None
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@api_view(['POST'])
def password_reset_view(request):
    username = request.data.get('username')

    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)

        # Simulate insecure randomness for token generation
        current_time = str(int(time.time() * 1000))  # Milliseconds since epoch
        token = hashlib.sha256((username + current_time).encode()).hexdigest()

        if profile.role == 'admin':
            return JsonResponse({'message': 'Password reset link sent to your inbox'})
        else:
            # Return the reset token to the normal user
            reset_link = f"http://localhost:8000/sandbox1/reset/{token}"
            return JsonResponse({'reset_link': reset_link})

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)