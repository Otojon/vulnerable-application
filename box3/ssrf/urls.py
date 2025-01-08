from django.urls import path
from . import views

urlpatterns = [
    path('sandbox3/send/', views.fetch_url, name='fetch_url'),
    path('sandbox3/internal/', views.internal_api, name='internal_api'),
]
