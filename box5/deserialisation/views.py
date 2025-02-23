import jsonpickle
from django.http import JsonResponse, HttpResponseBadRequest
from . models import UserPreference  
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_preferences(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")
    try:
        payload = jsonpickle.decode(request.body.decode('utf-8'))
        name = payload.get("name")
        age = payload.get("age")
        width = payload.get("width")
        height = payload.get("height")
        counrty = payload.get("counrty")  
        if None in (name, age, width, height, counrty):
            return HttpResponseBadRequest("Missing required fields.")
        pref = UserPreference(
            name=name,
            age=age,
            width=width,
            height=height,
            counrty=counrty
        )
        pref.save()
        return JsonResponse({"status": "success", "id": pref.id})
    except Exception as e:
        return HttpResponseBadRequest(f"Error processing request: {str(e)}")

def get_preferences(request, user_id):
    if request.method != "GET":
        return HttpResponseBadRequest("Invalid request method.")
    try:
        pref = UserPreference.objects.get(pk=user_id)
    except UserPreference.DoesNotExist:
        return JsonResponse({"error": "UserPreference not found."}, status=404)

    return JsonResponse({
        "id": pref.id,
        "name": pref.name,
        "age": pref.age,
        "width": pref.width,
        "height": pref.height,
        "counrty": pref.counrty,
    })