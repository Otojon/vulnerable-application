from django.urls import path
from cryptographic_vulns.views import crypto_login_view, crypto_profile_view

urlpatterns = [
    path('sandbox1/crypto-login/', crypto_login_view, name='crypto-login'),
    path('sandbox1/crypto-profile/', crypto_profile_view, name='crypto-profile'),
]
