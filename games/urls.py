from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('game/<int:game_id>/', views.game_detail_view, name='game_detail'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('create/', views.create_game_view, name='create_game'),
    path('random/', views.random_game_view, name='random_game'),
    path('toggle-favorite/<int:game_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('toggle-public/<int:game_id>/', views.toggle_public, name='toggle_public'),
]
