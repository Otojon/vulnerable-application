from django.urls import path
from .views import login_user, change_user_role, admin_panel, update_profile, fetch_user_details

urlpatterns = [
    # Login and Change User Role endpoints
    path('sandbox1/login/', login_user, name='login-user'),
    path('sandbox1/change-user-role/', change_user_role, name='change-user-role'),  # Updated URL
    
    # Admin panel and IDOR endpoints
    path('sandbox1/admin-panel/', admin_panel, name='admin-panel'),
    path('sandbox1/update-profile/', update_profile, name='update-profile'),
    path('sandbox1/fetch-user-details/', fetch_user_details, name='fetch-user-details'),
]
