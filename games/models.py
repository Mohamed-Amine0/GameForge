from django.db import models
from django.conf import settings

class GameProject(models.Model):
    GENRE_CHOICES = [
        ('RPG', 'RPG'), ('FPS', 'FPS'), ('VN', 'Visual Novel'),
        ('MET', 'Metroidvania'),
    ]
    MOOD_CHOICES = [
        ('CYBERPUNK', 'Cyberpunk'), ('DARK', 'Dark Fantasy'),
        ('DREAMY', 'Onirique'), ('POSTAPO', 'Post-apocalyptique'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    keywords = models.CharField(max_length=200)
    references = models.CharField(max_length=200, blank=True, null=True)

    universe_description = models.TextField(blank=True)
    main_story = models.TextField(blank=True)
    characters = models.JSONField(blank=True, null=True)
    locations = models.JSONField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    interactive_story = models.JSONField(blank=True, null=True)
    def __str__(self):
        return self.title
    

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(GameProject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user} ❤️ {self.game.title}"
