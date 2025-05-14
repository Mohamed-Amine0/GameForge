from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Game(models.Model):
    """
    Model for game concepts.
    """
    GENRE_CHOICES = [
        ('RPG', 'Role-Playing Game'),
        ('FPS', 'First-Person Shooter'),
        ('METROIDVANIA', 'Metroidvania'),
        ('VISUAL_NOVEL', 'Visual Novel'),
        ('PLATFORMER', 'Platformer'),
        ('STRATEGY', 'Strategy'),
        ('SIMULATION', 'Simulation'),
        ('PUZZLE', 'Puzzle'),
        ('OTHER', 'Other'),
    ]

    AMBIANCE_CHOICES = [
        ('POST_APOCALYPTIC', 'Post-Apocalyptic'),
        ('CYBERPUNK', 'Cyberpunk'),
        ('FANTASY', 'Fantasy'),
        ('DARK_FANTASY', 'Dark Fantasy'),
        ('SCI_FI', 'Science Fiction'),
        ('HORROR', 'Horror'),
        ('MYSTERY', 'Mystery'),
        ('HISTORICAL', 'Historical'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='games')
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    ambiance = models.CharField(max_length=20, choices=AMBIANCE_CHOICES)
    theme_keywords = models.CharField(max_length=200, help_text=_("Comma-separated keywords"))
    cultural_references = models.CharField(max_length=200, blank=True, help_text=_("Comma-separated references"))

    # Game universe
    universe_description = models.TextField()

    # Story
    story_description = models.TextField()

    # Additional fields
    is_public = models.BooleanField(default=True, help_text=_("Whether the game is visible to other users"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Character(models.Model):
    """
    Model for game characters.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    background = models.TextField()
    abilities = models.TextField()
    motivation = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.game.title})"

class Location(models.Model):
    """
    Model for game locations.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.game.title})"

class GameImage(models.Model):
    """
    Model for game images.
    """
    IMAGE_TYPE_CHOICES = [
        ('CHARACTER', 'Character'),
        ('ENVIRONMENT', 'Environment'),
        ('CONCEPT', 'Concept Art'),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='game_images/')
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_image_type_display()} for {self.game.title}"

class Favorite(models.Model):
    """
    Model for user favorites.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} favorited {self.game.title}"
