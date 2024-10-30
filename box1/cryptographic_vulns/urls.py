from django.urls import path
from .views import login_view, profile_view, password_reset_view

urlpatterns = [
    path('sandbox1/login3/', login_view, name='login'),
    path('sandbox1/profile3/', profile_view, name='profile'),
    path('sandbox1/password-reset3/', password_reset_view, name='password-reset'),
]
