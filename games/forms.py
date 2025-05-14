from django import forms
from .models import Game, Character, Location, GameImage

class GameForm(forms.ModelForm):
    """
    Form for creating and editing games.
    """
    class Meta:
        model = Game
        fields = ['title', 'genre', 'ambiance', 'theme_keywords', 'cultural_references', 'is_public']
        widgets = {
            'theme_keywords': forms.TextInput(attrs={'placeholder': 'e.g., time travel, revenge, AI rebellion'}),
            'cultural_references': forms.TextInput(attrs={'placeholder': 'e.g., Zelda, Hollow Knight, Disco Elysium'}),
        }

class CharacterForm(forms.ModelForm):
    """
    Form for creating and editing characters.
    """
    class Meta:
        model = Character
        fields = ['name', 'role', 'background', 'abilities', 'motivation']

class LocationForm(forms.ModelForm):
    """
    Form for creating and editing locations.
    """
    class Meta:
        model = Location
        fields = ['name', 'description']

class GameImageForm(forms.ModelForm):
    """
    Form for uploading game images.
    """
    class Meta:
        model = GameImage
        fields = ['image', 'image_type', 'description']

class GameFilterForm(forms.Form):
    """
    Form for filtering games.
    """
    genre = forms.ChoiceField(choices=[('', 'All Genres')] + Game.GENRE_CHOICES, required=False)
    ambiance = forms.ChoiceField(choices=[('', 'All Ambiances')] + Game.AMBIANCE_CHOICES, required=False)
    search_query = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search games...'}))