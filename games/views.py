import io
import json
import tempfile
from django.db.models import Q
import random
from .models import GameProject
from xhtml2pdf import pisa
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string, get_template
from games.image_gen import generate_image
from .forms import GameProjectForm
from .ia import generate_interactive_story_prompt, parse_generated_content, query_mistral
from .models import Favorite, GameProject
from django.views.decorators.http import require_POST


def generate_prompt(game):
    return f"""
Tu es un assistant IA spécialisé dans la création de jeux vidéo.

Voici un nouveau jeu à générer :
- Genre : {game.genre}
- Ambiance : {game.mood}
- Mots-clés : {game.keywords}
- Références : {game.references or "Aucune"}

Génère les sections suivantes :
1. 🌌 Une description d'univers cohérente
2. 📖 Un scénario en 3 actes
3. 🧍 Trois personnages : nom, classe, rôle, motivation
4. 🗺️ Deux lieux emblématiques : nom, description immersive
"""


@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameProjectForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()

            # Génération IA
            prompt = generate_prompt(game)
            #result = query_model(prompt)
            result = query_mistral(prompt)

            # Stocke tout le contenu dans un champ pour l’instant
            parsed = parse_generated_content(result)
            print("Prompt envoyé à l'IA:")
            print(prompt)
            print("Réponse IA brute:")
            print(result)
            game.universe_description = parsed.get("universe", "")
            game.main_story = parsed.get("story", "")
            game.characters = parsed.get("characters", [])
            game.locations = parsed.get("locations", [])

            game.save()

            return redirect('dashboard')
    else:
        form = GameProjectForm()
    return render(request, 'games/create_game.html', {'form': form})


@login_required
def dashboard_view(request):
    filter_type = request.GET.get('filter', 'all')  # default = all
    projects = GameProject.objects.filter(user=request.user)

    if filter_type == 'public':
        projects = projects.filter(is_public=True)
    elif filter_type == 'private':
        projects = projects.filter(is_public=False)

    projects = projects.order_by('-created_at')

    return render(request, 'games/dashboard.html', {
        'projects': projects,
        'filter_type': filter_type
    })


@login_required
def game_detail_view(request, game_id):
    game = get_object_or_404(GameProject, id=game_id)

    if not game.is_public and game.user != request.user:
        return HttpResponseForbidden("Ce jeu est privé.")

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, game=game).exists()

    return render(request, 'games/game_detail.html', {
        'game': game,
        'is_favorite': is_favorite
    })



@require_POST
@login_required
def toggle_visibility(request, game_id):
    game = get_object_or_404(GameProject, id=game_id, user=request.user)
    game.is_public = not game.is_public
    game.save()
    return redirect('game-detail', game_id=game.id)


@login_required
def generate_images_view(request, game_id):
    game = get_object_or_404(GameProject, id=game_id, user=request.user)

    prompt_char = f"Concept art of a character in a {game.mood} {game.genre} world, detailed, fantasy style"
    prompt_env = f"Environment from a {game.mood} {game.genre} game world, beautiful, atmospheric, digital painting"

    image_char_url = generate_image(prompt_char)
    image_env_url = generate_image(prompt_env)
    print("Image personnage : ", image_char_url)
    print("Image environnement : ", image_env_url)

    return render(request, 'games/game_images.html', {
        'game': game,
        'image_char': image_char_url,
        'image_env': image_env_url,
    })

@login_required
def export_game_pdf(request, game_id):
    game = get_object_or_404(GameProject, id=game_id, user=request.user)

    template_path = 'games/game_pdf.html'
    context = {'game': game}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{game.title}.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)

    response.write(result.getvalue())
    return response



@login_required
def toggle_favorite(request, game_id):
    game = get_object_or_404(GameProject, id=game_id, is_public=True)

    favorite, created = Favorite.objects.get_or_create(user=request.user, game=game)
    if not created:
        favorite.delete()

    return redirect('game-detail', game_id=game.id)

@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('game')
    return render(request, 'games/favorites.html', {'favorites': favorites})

@login_required
def generate_random_game(request):
    genres = [c[0] for c in GameProject.GENRE_CHOICES]
    moods = [c[0] for c in GameProject.MOOD_CHOICES]
    keywords_list = [
        "voyage temporel", "cyborg", "quête vengeresse", "royaume déchu",
        "IA rebelle", "société secrète", "pouvoir mystique", "fantaisie noire"
    ]

    genre = random.choice(genres)
    mood = random.choice(moods)
    keywords = ", ".join(random.sample(keywords_list, 3))
    title = f"Jeu Mystère #{random.randint(1000, 9999)}"

    game = GameProject.objects.create(
        user=request.user,
        title=title,
        genre=genre,
        mood=mood,
        keywords=keywords,
        is_public=False
    )

    prompt = generate_prompt(game)
   # result = query_model(prompt)
    result = query_mistral(prompt)
    parsed = parse_generated_content(result)

    game.universe_description = parsed.get("universe", "")
    game.main_story = parsed.get("story", "")
    game.characters = parsed.get("characters", [])
    game.locations = parsed.get("locations", [])
    game.save()

    return redirect('game-detail', game_id=game.id)

@login_required
def dashboard_view(request):
    query = request.GET.get('q', '')
    projects = GameProject.objects.filter(user=request.user)

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(genre__icontains=query) |
            Q(mood__icontains=query)
        )

    return render(request, 'games/dashboard.html', {
        'projects': projects,
        'query': query
    })


def generate_interactive_story(request, game_id):
    game = get_object_or_404(GameProject, id=game_id, user=request.user)
    prompt = generate_interactive_story_prompt(game)
   # result = query_model(prompt)
    result = query_mistral(prompt)

    parsed = parse_generated_content(result)

    try:
        story_json = json.loads(result)
        game.interactive_story = story_json
        game.save()
        return redirect('play-interactive', game_id=game.id)
    except Exception:
        return HttpResponse("Erreur IA ou parsing JSON")


def play_interactive_story(request, game_id):
    game = get_object_or_404(GameProject, id=game_id, user=request.user)

    story = game.interactive_story
    step = int(request.GET.get("step", 0))
    choice = request.GET.get("choice")

    if story and 0 <= step < len(story["scenes"]):
        scene = story["scenes"][step]
        outcome = ""
        if choice:
            selected = next((c for c in scene["choices"] if c["label"] == choice), None)
            if selected:
                outcome = selected["outcome"]

        return render(request, 'games/interactive_story.html', {
            'scene': scene,
            'step': step,
            'next_step': step + 1,
            'outcome': outcome,
            'game': game,
        })
    return HttpResponse("Fin ou histoire indisponible")


def export_gdd_pdf(request, game_id):
    game = get_object_or_404(GameProject, id=game_id, user=request.user)

    template_path = 'games/gdd_pdf.html'
    context = {'game': game}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="GDD_{game.title}.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du GDD PDF', status=500)

    response.write(result.getvalue())
    return response

@login_required
def dashboard_view(request):
    projects = GameProject.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'games/dashboard.html', {'projects': projects})

def public_games_view(request):
    public_projects = GameProject.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'games/public_dashboard.html', {'projects': public_projects})

@login_required
def explore_public_games(request):
    query = request.GET.get('q', '')
    public_games = GameProject.objects.filter(is_public=True)

    if query:
        public_games = public_games.filter(title__icontains=query)

    public_games = public_games.order_by('-created_at')

    return render(request, 'games/public_games.html', {
        'projects': public_games,
        'query': query
    })
