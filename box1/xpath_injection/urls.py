from django.urls import path
from .views import xpath_login_view, xpath_profile_view

urlpatterns = [
    path('sandbox1/xpath-login', xpath_login_view, name='xpath_login'),
    path('sandbox1/xpath-profile', xpath_profile_view, name='xpath_profile'),
]
