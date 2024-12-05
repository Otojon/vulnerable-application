# middleware.py
import jwt
from django.http import JsonResponse
from django.conf import settings

SECRET_KEY = "mysecret"

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt_token')
        if token:
            try:
                # Vulnerable decode: No algorithm specified allows algorithm confusion
                decoded = jwt.decode(token, SECRET_KEY, options={"verify_signature": False})
                request.user_id = decoded.get('userID')
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expired'}, status=403)
            except jwt.DecodeError:
                return JsonResponse({'error': 'Invalid token'}, status=403)

        return self.get_response(request)
