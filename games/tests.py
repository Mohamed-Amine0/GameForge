from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Game, Character, Location, Favorite
from .forms import GameForm

User = get_user_model()

class GameModelTest(TestCase):
    """
    Tests for the Game model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.game = Game.objects.create(
            user=self.user,
            title='Test Game',
            genre='RPG',
            ambiance='FANTASY',
            theme_keywords='adventure, magic, quest',
            cultural_references='Zelda, Final Fantasy',
            universe_description='A magical world with floating islands.',
            story_description='A hero must save the world from darkness.',
            is_public=True
        )

    def test_game_creation(self):
        """Test that a game can be created."""
        self.assertEqual(self.game.title, 'Test Game')
        self.assertEqual(self.game.genre, 'RPG')
        self.assertEqual(self.game.ambiance, 'FANTASY')
        self.assertEqual(self.game.theme_keywords, 'adventure, magic, quest')
        self.assertEqual(self.game.cultural_references, 'Zelda, Final Fantasy')
        self.assertEqual(self.game.universe_description, 'A magical world with floating islands.')
        self.assertEqual(self.game.story_description, 'A hero must save the world from darkness.')
        self.assertTrue(self.game.is_public)
        self.assertEqual(self.game.user, self.user)

    def test_game_string_representation(self):
        """Test the string representation of a game."""
        self.assertEqual(str(self.game), 'Test Game')

class CharacterModelTest(TestCase):
    """
    Tests for the Character model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.game = Game.objects.create(
            user=self.user,
            title='Test Game',
            genre='RPG',
            ambiance='FANTASY',
            theme_keywords='adventure, magic, quest',
            universe_description='A magical world with floating islands.',
            story_description='A hero must save the world from darkness.',
        )
        self.character = Character.objects.create(
            game=self.game,
            name='Test Character',
            role='Protagonist',
            background='A young warrior from a small village.',
            abilities='Sword fighting, magic spells',
            motivation='To save their family from the darkness.'
        )

    def test_character_creation(self):
        """Test that a character can be created."""
        self.assertEqual(self.character.name, 'Test Character')
        self.assertEqual(self.character.role, 'Protagonist')
        self.assertEqual(self.character.background, 'A young warrior from a small village.')
        self.assertEqual(self.character.abilities, 'Sword fighting, magic spells')
        self.assertEqual(self.character.motivation, 'To save their family from the darkness.')
        self.assertEqual(self.character.game, self.game)

    def test_character_string_representation(self):
        """Test the string representation of a character."""
        self.assertEqual(str(self.character), 'Test Character (Test Game)')

class GameViewsTest(TestCase):
    """
    Tests for the game views.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.game = Game.objects.create(
            user=self.user,
            title='Test Game',
            genre='RPG',
            ambiance='FANTASY',
            theme_keywords='adventure, magic, quest',
            universe_description='A magical world with floating islands.',
            story_description='A hero must save the world from darkness.',
            is_public=True
        )
        self.private_game = Game.objects.create(
            user=self.user,
            title='Private Game',
            genre='FPS',
            ambiance='SCI_FI',
            theme_keywords='space, aliens, war',
            universe_description='A distant galaxy at war.',
            story_description='A space marine fights against alien invaders.',
            is_public=False
        )
        self.home_url = reverse('games:home')
        self.dashboard_url = reverse('games:dashboard')
        self.game_detail_url = reverse('games:game_detail', args=[self.game.id])
        self.private_game_detail_url = reverse('games:game_detail', args=[self.private_game.id])
        self.create_game_url = reverse('games:create_game')
        self.favorites_url = reverse('games:favorites')

    def test_home_view(self):
        """Test that the home page loads correctly and shows only public games."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/home.html')
        self.assertIn(self.game, response.context['games'])
        self.assertNotIn(self.private_game, response.context['games'])

    def test_dashboard_view_authenticated(self):
        """Test that the dashboard page loads correctly for authenticated users."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/dashboard.html')
        self.assertIn(self.game, response.context['games'])
        self.assertIn(self.private_game, response.context['games'])

    def test_dashboard_view_unauthenticated(self):
        """Test that unauthenticated users are redirected from the dashboard."""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_game_detail_view_public(self):
        """Test that the game detail page loads correctly for public games."""
        response = self.client.get(self.game_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_detail.html')
        self.assertEqual(response.context['game'], self.game)

    def test_game_detail_view_private_owner(self):
        """Test that the game detail page loads correctly for private games when the user is the owner."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.private_game_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_detail.html')
        self.assertEqual(response.context['game'], self.private_game)

    def test_game_detail_view_private_non_owner(self):
        """Test that users cannot view private games they don't own."""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword123'
        )
        self.client.login(username='otheruser', password='otherpassword123')
        response = self.client.get(self.private_game_detail_url)
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_create_game_view_get(self):
        """Test that the create game page loads correctly."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.create_game_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/create_game.html')
        self.assertIsInstance(response.context['form'], GameForm)

    def test_create_game_view_post_valid(self):
        """Test that a game can be created with valid data."""
        self.client.login(username='testuser', password='testpassword123')
        data = {
            'title': 'New Game',
            'genre': 'RPG',
            'ambiance': 'FANTASY',
            'theme_keywords': 'adventure, magic, quest',
            'cultural_references': 'Zelda, Final Fantasy',
            'is_public': True,
        }
        response = self.client.post(self.create_game_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Game.objects.filter(title='New Game').exists())

class FavoriteTest(TestCase):
    """
    Tests for the favorites functionality.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword123'
        )
        self.game = Game.objects.create(
            user=self.other_user,
            title='Test Game',
            genre='RPG',
            ambiance='FANTASY',
            theme_keywords='adventure, magic, quest',
            universe_description='A magical world with floating islands.',
            story_description='A hero must save the world from darkness.',
            is_public=True
        )
        self.private_game = Game.objects.create(
            user=self.other_user,
            title='Private Game',
            genre='FPS',
            ambiance='SCI_FI',
            theme_keywords='space, aliens, war',
            universe_description='A distant galaxy at war.',
            story_description='A space marine fights against alien invaders.',
            is_public=False
        )
        self.toggle_favorite_url = reverse('games:toggle_favorite', args=[self.game.id])
        self.toggle_private_favorite_url = reverse('games:toggle_favorite', args=[self.private_game.id])
        self.favorites_url = reverse('games:favorites')

    def test_toggle_favorite(self):
        """Test that a user can toggle a game as favorite."""
        self.client.login(username='testuser', password='testpassword123')

        # Add to favorites
        response = self.client.get(self.toggle_favorite_url)
        self.assertEqual(response.status_code, 302)  # Redirect after toggling
        self.assertTrue(Favorite.objects.filter(user=self.user, game=self.game).exists())

        # Remove from favorites
        response = self.client.get(self.toggle_favorite_url)
        self.assertEqual(response.status_code, 302)  # Redirect after toggling
        self.assertFalse(Favorite.objects.filter(user=self.user, game=self.game).exists())

    def test_toggle_private_favorite(self):
        """Test that a user cannot favorite a private game they don't own."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.toggle_private_favorite_url)
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertFalse(Favorite.objects.filter(user=self.user, game=self.private_game).exists())

    def test_favorites_view(self):
        """Test that the favorites page loads correctly."""
        self.client.login(username='testuser', password='testpassword123')

        # Add a game to favorites
        Favorite.objects.create(user=self.user, game=self.game)

        response = self.client.get(self.favorites_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/favorites.html')
        self.assertIn(self.game, response.context['games'])
