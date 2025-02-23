from django.urls import path
from .views import vulnerable_view

urlpatterns = [
    path('demo', vulnerable_view, name='vulnerable_view'),
]
