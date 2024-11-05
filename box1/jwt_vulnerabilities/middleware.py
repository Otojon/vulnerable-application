import jwt
from django.http import JsonResponse
from django.conf import settings
from access_control.models import UserProfile

SECRET_KEY = "mysecret"

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt_token')
        if token:
            try:
                decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                request.user_id = decoded.get('userID')
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expired'}, status=403)
            except jwt.DecodeError:
                return JsonResponse({'error': 'Invalid token'}, status=403)

        return self.get_response(request)
