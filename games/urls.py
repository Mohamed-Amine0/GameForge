from django.urls import path
from .views import create_game, dashboard_view, explore_public_games, export_game_pdf, export_gdd_pdf, favorites_view, game_detail_view, generate_images_view, generate_interactive_story, generate_random_game, play_interactive_story, public_games_view, toggle_favorite, toggle_visibility
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('create/', create_game, name='create-game'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('<int:game_id>/', game_detail_view, name='game-detail'),
    path('<int:game_id>/toggle/', toggle_visibility, name='toggle-visibility'),
    path('<int:game_id>/images/', generate_images_view, name='generate-images'),
    path('<int:game_id>/pdf/', export_game_pdf, name='export-pdf'),
    path('<int:game_id>/favorite/', toggle_favorite, name='toggle-favorite'),
    path('favorites/', favorites_view, name='favorites'),
    path('random/', generate_random_game, name='random-game'),
    path('<int:game_id>/story/', generate_interactive_story, name='generate-interactive'),
    path('<int:game_id>/play/', play_interactive_story, name='play-interactive'),
    path('<int:game_id>/gdd/', export_gdd_pdf, name='export-gdd'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('public/', public_games_view, name='public-dashboard'),
    path('explore/', explore_public_games, name='explore-public'),


]
