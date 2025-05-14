from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('generate-text/', views.generate_text, name='generate_text'),
    path('generate-image/', views.generate_image, name='generate_image'),
]