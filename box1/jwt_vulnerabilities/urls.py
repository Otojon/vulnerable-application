# jwt_vulnerabilities/urls.py
from django.urls import path
from .views import login_view , home_view,admins, profile_view, admin2

urlpatterns = [
    path('',home_view,name='home'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('admins/', admins, name='admins'),
    path('admin2/', admin2, name='admin2'),
]

