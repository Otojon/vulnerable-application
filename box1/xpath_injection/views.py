from django.shortcuts import render
import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os

# Path to the XML file
XML_FILE_PATH = os.path.join(os.path.dirname(__file__), '../db/db.xml')
"""
later gonna replace it with the env variable
"""
SECRET_KEY = 'your_secret_key'  # Replace with a stronger key in production 



# xpath_injection/views.py

import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os

# Path to the XML file
XML_FILE_PATH = os.path.join(os.path.dirname(__file__), '../db/db.xml')
SECRET_KEY = 'your_secret_key'  # Replace with a stronger key in production

@csrf_exempt
def xpath_login_view(request):
    if request.method == "POST":
        # Extract username and password from JSON request
        data = request.json()
        username_input = data.get("username")
        password_input = data.get("password")

        # Parse XML and find the user using vulnerable XPath query
        tree = ET.parse(XML_FILE_PATH)
        root = tree.getroot()

        # Vulnerable XPath Query - directly uses user input without sanitization
        xpath_query = f".//user[username/text()='{username_input}' and password/text()='{password_input}']"
        user = root.find(xpath_query)
        
        if user is not None:
            user_id = user.find("id").text
            username = user.find("username").text
            role = user.find("role").text
            
            # Generate JWT payload
            payload = {
                "userID": user_id,
                "username": username,
                "isAdmin": role == "admin",
                "exp": datetime.utcnow() + timedelta(hours=1)
            }

            # Create JWT token
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            # Set token as HttpOnly cookie
            response = JsonResponse({"message": "Login successful"})
            response.set_cookie("jwt", token, httponly=True, max_age=3600)
            return response

        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def xpath_profile_view(request):
    # Retrieve JWT from cookies
    token = request.COOKIES.get("jwt")
    
    if not token:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        # Decode the JWT token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        user_id = decoded.get("userID")
        username = decoded.get("username")
        is_admin = decoded.get("isAdmin")

        # Parse XML to find user details
        tree = ET.parse(XML_FILE_PATH)
        root = tree.getroot()
        
        user = root.find(f".//user[id='{user_id}']")
        if user:
            password = user.find("password").text
            flag = user.find("flag").text if is_admin else "N/A"  # Only admin has a flag

            return JsonResponse({
                "username": username,
                "password": password,
                "role": "admin" if is_admin else "normal",
                "flag": flag
            })
            
        return JsonResponse({"error": "User not found"}, status=404)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token has expired"}, status=401)
    except jwt.DecodeError:
        return JsonResponse({"error": "Invalid token"}, status=401)
