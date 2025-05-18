import replicate
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Récupérer le token depuis la variable
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

replicate.Client(api_token=REPLICATE_API_TOKEN)

def generate_image(prompt):
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("a9758cb3e1e7ae30")  # version stable SD 1.5
    output = version.predict(prompt=prompt)
    return output[0] if output else None
