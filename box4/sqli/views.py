from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

def vulnerable_view(request):
    p = request.GET.get('p', '')
    query = f"SELECT * FROM sqli_product WHERE name LIKE '%{p}%'"
        
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    
    return JsonResponse({"results": rows})

"""
http://test.uz/product&p=otkan_kunlar
"""