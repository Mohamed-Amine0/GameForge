import os
import re
import requests
from dotenv import load_dotenv
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def query_mistral(prompt):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-medium",  # ou mistral-small, selon ton accès
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()
        return output["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERREUR]: {str(e)}"


def generate_interactive_story_prompt(game):
    return f"""
    Tu es un générateur de narration interactive pour un jeu vidéo.

    Voici les infos :
    - Genre : {game.genre}
    - Ambiance : {game.mood}
    - Thèmes : {game.keywords}

    Génère une **histoire à choix** en 3 scènes.
    À chaque scène, propose 2 choix (A ou B) avec leurs conséquences.

    Réponds au format JSON :
    {{
      "scenes": [
        {{
          "title": "Titre de la scène",
          "text": "Texte narratif",
          "choices": [
            {{"label": "A", "text": "Choix A", "outcome": "Conséquence A"}},
            {{"label": "B", "text": "Choix B", "outcome": "Conséquence B"}}
          ]
        }},
        ...
      ]
    }}
    """

def parse_generated_content(raw_text):
    try:
        # Séparer les différentes parties via des regex
        universe_match = re.search(r"1\. ?[^\n]*[:\n](.*?)(2\.|$)", raw_text, re.DOTALL)
        story_match = re.search(r"2\. ?[^\n]*[:\n](.*?)(3\.|$)", raw_text, re.DOTALL)
        characters_match = re.search(r"3\. ?[^\n]*[:\n](.*?)(4\.|$)", raw_text, re.DOTALL)
        locations_match = re.search(r"4\. ?[^\n]*[:\n](.*)", raw_text, re.DOTALL)

        def clean(text): return text.strip().replace("\n", " ").strip()

        universe = clean(universe_match.group(1)) if universe_match else ""
        story = clean(story_match.group(1)) if story_match else ""

        def parse_bullets(text_block):
            lines = text_block.strip().split("-")
            return [line.strip() for line in lines if line.strip()]

        characters = parse_bullets(characters_match.group(1)) if characters_match else []
        locations = parse_bullets(locations_match.group(1)) if locations_match else []

        return {
            "universe": universe,
            "story": story,
            "characters": characters,
            "locations": locations
        }

    except Exception as e:
        return {"error": str(e)}