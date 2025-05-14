# GameForge - Générateur de Concepts de Jeux Vidéo par IA

GameForge est une application web Django qui permet aux utilisateurs de créer des concepts de jeux vidéo uniques à l'aide de l'IA. La plateforme utilise les modèles de Hugging Face pour générer des univers de jeu, des personnages, des histoires et des illustrations conceptuelles.

## 📝 Aperçu du Projet

GameForge est une plateforme complète qui permet aux utilisateurs de :

- Générer des univers de jeu cohérents avec des genres et ambiances définis
- Créer des scénarios immersifs avec des narrations structurées
- Développer des personnages uniques avec des backgrounds, des capacités et des motivations
- Concevoir des lieux clés avec des descriptions détaillées
- Générer des illustrations conceptuelles pour les personnages et les environnements
- Sauvegarder, partager et explorer les concepts de jeux créés par la communauté

## 🚀 Fonctionnalités

- **Authentification Utilisateur** : S'inscrire, se connecter et gérer votre profil
- **Création de Jeux** : Créer des concepts de jeux avec un formulaire guidé ou une génération aléatoire
- **Intégration IA** : Exploiter les modèles de Hugging Face pour la génération de texte et d'images
- **Tableau de Bord** : Gérer tous vos concepts de jeux créés
- **Favoris** : Sauvegarder et organiser vos concepts de jeux préférés
- **Basculement Public/Privé** : Contrôler la visibilité de vos concepts de jeux
- **Limitation d'Utilisation de l'API** : Politique d'utilisation équitable pour prévenir les abus
- **Design Responsive** : Fonctionne sur ordinateurs et appareils mobiles

## 🛠️ Technologies Utilisées

- **Backend** : Django 5.2
- **Frontend** : Bootstrap 5, JavaScript
- **Base de Données** : SQLite (développement), PostgreSQL (production)
- **Modèles IA** : Modèles de génération de texte et d'images de Hugging Face

## 📋 Prérequis

- Python 3.8+
- pip
- virtualenv (recommandé)

## 🔧 Installation

1. Cloner le dépôt :
   ```
   git clone https://github.com/yourusername/gameforge.git
   cd gameforge
   ```

2. Créer et activer un environnement virtuel :
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Installer les dépendances :
   ```
   pip install -r requirements.txt
   ```

4. Configurer les variables d'environnement :
   Créer un fichier `.env` à la racine du projet et ajouter :
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   HUGGING_FACE_API_KEY=your_hugging_face_api_key
   ```

5. Exécuter les migrations :
   ```
   python manage.py migrate
   ```

6. Créer un superutilisateur :
   ```
   python manage.py createsuperuser
   ```

7. Lancer le serveur de développement :
   ```
   python manage.py runserver
   ```

8. Accéder à l'application sur http://127.0.0.1:8000/

## 🎮 Utilisation

1. **S'inscrire/Se connecter** : Créer un compte ou se connecter pour accéder à toutes les fonctionnalités
2. **Créer un Jeu** : Utiliser le formulaire guidé pour spécifier le genre, l'ambiance et les thèmes
3. **Explorer les Jeux** : Parcourir les jeux créés par la communauté
4. **Jeux Favoris** : Sauvegarder les jeux que vous aimez dans vos favoris
5. **Gérer Vos Jeux** : Utiliser le tableau de bord pour gérer vos jeux créés

## 🧪 Modèles IA Utilisés

- **Génération de Texte** : GPT-2 pour générer des descriptions de jeux, des histoires et des backgrounds de personnages
- **Génération d'Images** : Stable Diffusion pour créer des illustrations conceptuelles

## 🎁 Fonctionnalités Bonus Implémentées

- ✅ Animations de chargement pendant la génération IA
- ✅ Système de favoris
- ✅ Fonctionnalité de recherche et de filtrage
- ✅ Basculement public/privé pour les projets
- ✅ Limitation d'utilisation de l'API

## 🔮 Améliorations Futures

- Export PDF des concepts de jeux
- Génération de personnages plus détaillée
- Suggestions de mécaniques de jeu
- Édition collaborative
- Fonctionnalités de partage social

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## 👥 Contributeurs

- Votre Nom - Travail initial

## 🙏 Remerciements

- Hugging Face pour fournir les modèles d'IA
- La communauté Django pour le framework incroyable
- L'équipe Bootstrap pour les composants frontend
