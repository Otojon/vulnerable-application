# access_control/urls.py

from django.urls import path
from .views import login_user, make_me_admin

urlpatterns = [
    path('sandbox1/login/', login_user, name='login-user'),
    path('sandbox1/make-me/', make_me_admin, name='make-me-admin'),
]
