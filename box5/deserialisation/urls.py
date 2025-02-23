from django.urls import path
from . import views

urlpatterns = [
    path('sandbox3/update-preferences/', views.update_preferences, name='update-preferences'),
    path('sandbox3/get-preferences/<int:user_id>/', views.get_preferences, name='get-preferences'),
]
