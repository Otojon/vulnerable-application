# server_side_template_injection/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('sandbox2/name', views.name_view, name='name-view'),
]
