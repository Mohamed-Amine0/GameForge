from django.urls import path
from .views import account_settings_view, change_password_view, login_view, register_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('change-password/', change_password_view, name='change-password'),  
    path('settings/', account_settings_view, name='account-settings'),
    path('login/', login_view, name='login'),
    
]
