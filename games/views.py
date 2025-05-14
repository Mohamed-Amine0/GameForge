from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Game, Favorite
from .forms import GameForm, GameFilterForm

def home_view(request):
    """
    View for the home page.
    Shows all public games.
    """
    filter_form = GameFilterForm(request.GET or None)
    games = Game.objects.filter(is_public=True)

    if filter_form.is_valid():
        genre = filter_form.cleaned_data.get('genre')
        ambiance = filter_form.cleaned_data.get('ambiance')
        search_query = filter_form.cleaned_data.get('search_query')

        if genre:
            games = games.filter(genre=genre)
        if ambiance:
            games = games.filter(ambiance=ambiance)
        if search_query:
            games = games.filter(
                Q(title__icontains=search_query) |
                Q(theme_keywords__icontains=search_query) |
                Q(cultural_references__icontains=search_query)
            )

    context = {
        'games': games,
        'filter_form': filter_form,
    }
    return render(request, 'games/home.html', context)

@login_required
def dashboard_view(request):
    """
    View for the user dashboard.
    Shows all games created by the user.
    """
    games = Game.objects.filter(user=request.user)
    context = {
        'games': games,
    }
    return render(request, 'games/dashboard.html', context)

def game_detail_view(request, game_id):
    """
    View for the game detail page.
    Shows all details of a specific game.
    """
    game = get_object_or_404(Game, id=game_id)

    # Check if the game is private and the user is not the owner
    if not game.is_public and (not request.user.is_authenticated or request.user != game.user):
        messages.error(request, "You don't have permission to view this game.")
        return redirect('games:home')

    # Check if the game is in the user's favorites
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, game=game).exists()

    context = {
        'game': game,
        'is_favorite': is_favorite,
    }
    return render(request, 'games/game_detail.html', context)

@login_required
def favorites_view(request):
    """
    View for the favorites page.
    Shows all games favorited by the user.
    """
    favorites = Favorite.objects.filter(user=request.user).select_related('game')
    games = [favorite.game for favorite in favorites]

    context = {
        'games': games,
    }
    return render(request, 'games/favorites.html', context)

@login_required
def create_game_view(request):
    """
    View for creating a new game.
    """
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()

            # Increment the user's API usage count
            request.user.api_usage_count += 1
            request.user.save()

            messages.success(request, f"Game '{game.title}' created successfully!")
            return redirect('games:game_detail', game_id=game.id)
    else:
        form = GameForm()

    context = {
        'form': form,
    }
    return render(request, 'games/create_game.html', context)

@login_required
def random_game_view(request):
    """
    View for creating a random game.
    """
    # This will be implemented with AI integration
    messages.info(request, "Random game generation is coming soon!")
    return redirect('games:home')

@login_required
def toggle_favorite(request, game_id):
    """
    View for toggling a game as favorite.
    """
    game = get_object_or_404(Game, id=game_id)

    # Check if the game is private and the user is not the owner
    if not game.is_public and request.user != game.user:
        messages.error(request, "You don't have permission to favorite this game.")
        return redirect('games:home')

    favorite, created = Favorite.objects.get_or_create(user=request.user, game=game)

    if not created:
        favorite.delete()
        messages.success(request, f"Removed '{game.title}' from favorites.")
    else:
        messages.success(request, f"Added '{game.title}' to favorites.")

    return redirect('games:game_detail', game_id=game.id)

@login_required
def toggle_public(request, game_id):
    """
    View for toggling a game as public/private.
    """
    game = get_object_or_404(Game, id=game_id, user=request.user)
    game.is_public = not game.is_public
    game.save()

    status = "public" if game.is_public else "private"
    messages.success(request, f"Game '{game.title}' is now {status}.")

    return redirect('games:game_detail', game_id=game.id)
