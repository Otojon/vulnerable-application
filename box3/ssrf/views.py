from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests
from urllib.parse import urlparse
import subprocess

@csrf_exempt
def internal_api(request):
    """
    Internal API that restricts access to requests made by Python's requests library
    and validates URL-based authentication.
    """
    # Ensure request comes from Python requests library
    if 'python-requests' not in request.META.get('HTTP_USER_AGENT', ''):
        return JsonResponse({'error': 'Access denied: not from local interface'}, status=403)

    # Validate URL-based authentication
    user = request.GET.get('user')
    token = request.GET.get('token')

    if user != settings.USER or token != settings.TOKEN:
        return JsonResponse({'error': 'Authentication failed'}, status=401)

    return JsonResponse({'message': 'Authenticated access to internal API'})


def fetch_url(request):
    """
    Proxy endpoint to fetch content from any given URL, supporting multiple protocols dynamically.
    """
    fetch_url = request.GET.get('fetch')
    if not fetch_url:
        return JsonResponse({'error': 'No URL provided'}, status=400)

    # Parse the URL
    parsed_url = urlparse(fetch_url)
    if not parsed_url.scheme:
        return JsonResponse({'error': 'Invalid URL: Missing scheme'}, status=400)

    try:
        # Use Python's requests library for HTTP/HTTPS
        if parsed_url.scheme in ['http', 'https']:
            response = requests.get(fetch_url, timeout=5)
            response.raise_for_status()
            return JsonResponse({'response': response.text})

        # Handle other protocols dynamically via subprocess without hardcoding them
        result = subprocess.run(
            ['curl','-k','-H "python-requests/2.32.3"', '-L', fetch_url], capture_output=True, text=True, timeout=10, check=True
        )
        return JsonResponse({'response': result.stdout})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': f'Failed to fetch URL (Subprocess Error): {e.stderr}'}, status=400)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Failed to fetch URL (Requests Error): {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected Error: {str(e)}'}, status=500)