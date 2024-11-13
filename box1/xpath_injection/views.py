import jwt
from jwt import decode, ExpiredSignatureError, DecodeError
import json
from lxml import etree
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, timezone
import os

# Path to the XML file
XML_FILE_PATH = os.path.join(os.path.dirname(__file__), './db/db.xml')
SECRET_KEY = 'your_secret_key'  # Replace with a stronger key in production

@csrf_exempt
def xpath_login_view(request):
    if request.method == "POST":
        # Parse JSON data from the request
        data = json.loads(request.body)
        username_input = data.get("username")
        password_input = data.get("password")

        # Load and parse the XML file using lxml
        with open(XML_FILE_PATH, "r") as file:
            xml_content = file.read()
        root = etree.fromstring(xml_content)

        # Vulnerable XPath query that directly uses unfiltered input
        xpath_query = f".//user[username/text()='{username_input}' and password/text()='{password_input}']"
        print(f"[+] Executing XPath query: {xpath_query}")

        try:
            user = root.xpath(xpath_query)
        except etree.XPathError as e:
            return JsonResponse({"error": f"Invalid XPath query syntax: {str(e)}"}, status=400)

        if user:
            user = user[0]  # Get the first matching user node
            user_id = user.find("id").text
            username = user.find("username").text
            role = user.find("role").text

            # Generate JWT payload
            payload = {
                "userID": user_id,
                "username": username,
                "isAdmin": role == "admin",
                "exp": datetime.now(timezone.utc) + timedelta(hours=1)
            }

            # Create JWT token
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            # Return the token in the response
            return JsonResponse({"message": "Login successful", "token": token})

        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)




@csrf_exempt
@csrf_exempt
def xpath_profile_view(request):
    if request.method == "GET":
        # Retrieve JWT token from the HTTP header
        token = request.headers.get("xpath-auth")
        if not token:
            return JsonResponse({"error": "Unauthorized: Token is missing"}, status=401)

        try:
            # Decode the JWT token
            decoded = decode(token, SECRET_KEY, algorithms=["HS256"])

            user_id = decoded.get("userID")
            username = decoded.get("username")
            is_admin = decoded.get("isAdmin")

            # Load and parse the XML file
            with open(XML_FILE_PATH, "r") as file:
                xml_content = file.read()
            root = etree.fromstring(xml_content)

            # Find the user based on the userID in the token
            user = root.xpath(f".//user[id='{user_id}']")
            if user:
                user = user[0]  # Get the first matching user node
                password = user.find("password").text
                flag = user.find("flag").text if is_admin else "N/A"  # Only admin users have a flag

                # Return user details
                return JsonResponse({
                    "username": username,
                    "password": password,
                    "role": "admin" if is_admin else "normal",
                    "flag": flag
                })

            return JsonResponse({"error": "User not found"}, status=404)

        except ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired. Please log in again."}, status=401)
        except DecodeError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Only GET requests are allowed"}, status=405)
