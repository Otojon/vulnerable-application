from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests
from urllib.parse import urlparse

@csrf_exempt
def internal_api(request):
    # Check if the request is coming from the local interface
    client_ip = request.META.get('REMOTE_ADDR')
    if client_ip != '127.0.0.1':
        return JsonResponse({'error': 'Access denied: not from local interface'}, status=403)

    # Validate URL-based authentication
    user = request.GET.get('user')
    token = request.GET.get('token')

    if user != settings.USER or token != settings.TOKEN:
        return JsonResponse({'error': 'Authentication failed'}, status=401)

    return JsonResponse({'message': 'Authenticated access to internal API'})
def fetch_url(request):
    fetch_url = request.GET.get('fetch')
    if not fetch_url:
        return JsonResponse({'error': 'No URL provided'}, status=400)

    # Validate the URL scheme
    parsed_url = urlparse(fetch_url)
    if parsed_url.scheme not in ['http', 'https', 'ftp', 'file']:
        return JsonResponse({'error': 'Unsupported URL scheme'}, status=400)

    try:
        response = requests.get(fetch_url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'response': response.text})