# jwt_vulnerabilities/urls.py
from django.urls import path
from .views import register_view, login_view, home_view, logout_view, admin_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('admin-page/', admin_view, name='admin_page'),  # Admin-only page
]
