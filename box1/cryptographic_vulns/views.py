import json
import os
from datetime import datetime, timedelta
from base64 import b64encode, b64decode
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

DB_FILE_PATH = os.path.join(os.path.dirname(__file__), "db.json")


# Load users from db.json
def load_users():
    if os.path.exists(DB_FILE_PATH):
        with open(DB_FILE_PATH, "r") as file:
            return json.load(file)
    return []


# Save users to db.json
def save_users(users):
    with open(DB_FILE_PATH, "w") as file:
        json.dump(users, file, indent=4)


@csrf_exempt
def crypto_login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username_input = data.get("username")
        password_input = data.get("password")

        users = load_users()
        user = next((u for u in users if u["username"] == username_input and u["password"] == password_input), None)

        if user:
            # Generate token
            login_time = int(datetime.now().timestamp())
            token_data = f"{user['id']}+{login_time}+{user['username']}"
            token = b64encode(token_data.encode()).decode()

            # Update the token in db.json
            for u in users:
                if u["username"] == username_input:
                    u["token"] = token
            save_users(users)

            return JsonResponse({"message": "Login successful", "token": token})

        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


@csrf_exempt
def crypto_profile_view(request):
    auth_header = request.headers.get("crypto-auth")
    if not auth_header:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        decoded_token = b64decode(auth_header).decode()
        user_id, timestamp, username = decoded_token.split("+")
        login_time = datetime.fromtimestamp(int(timestamp))

        users = load_users()
        user = next((u for u in users if u["id"] == int(user_id) and u["token"] == auth_header), None)

        if user:
            response = {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
            }

            if user["role"] == "admin":
                response["flag"] = user.get("flag", "N/A")
            else:
                response["message"] = "Normal user logged in"
                response["message"] = f"Admin user last login: {login_time.strftime('%Y-%m-%d %H:%M:%S')}"

            return JsonResponse(response)

        return JsonResponse({"error": "Unauthorized"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=401)
