# Instructions pour publier le projet sur GitHub

## Étape 1: Créer un dépôt GitHub (si ce n'est pas déjà fait)

1. Connectez-vous à votre compte GitHub sur [github.com](https://github.com)
2. Cliquez sur le bouton "+" en haut à droite, puis sélectionnez "New repository"
3. Nommez le dépôt "GameForge" (comme indiqué dans l'URL cible: https://github.com/Mohamed-Amine0/GameForge)
4. Laissez la description vide ou ajoutez une brève description du projet
5. Choisissez "Public" pour la visibilité du dépôt
6. Ne cochez PAS "Initialize this repository with a README" car nous avons déjà un fichier README
7. Cliquez sur "Create repository"

## Étape 2: Connecter votre dépôt local au dépôt GitHub

Après avoir créé le dépôt GitHub, vous verrez une page avec des instructions. Suivez les instructions pour "push an existing repository from the command line":

```bash
git remote add origin https://github.com/Mohamed-Amine0/GameForge.git
git branch -M main
git push -u origin main
```

Ces commandes vont:
1. Ajouter le dépôt GitHub comme "remote" nommé "origin"
2. Renommer votre branche principale en "main" (si ce n'est pas déjà le cas)
3. Pousser votre code vers GitHub

## Étape 3: Vérifier que tout a bien été publié

1. Rafraîchissez la page de votre dépôt GitHub
2. Vous devriez voir tous vos fichiers et dossiers listés
3. Vérifiez que le fichier README.md s'affiche correctement en bas de la page

## Étape 4: Configuration supplémentaire (optionnel)

Vous pouvez également:

1. Ajouter des tags pour les versions de votre projet:
   ```bash
   git tag -a v1.0 -m "Version initiale"
   git push origin v1.0
   ```

2. Configurer GitHub Pages si vous souhaitez avoir une page de présentation pour votre projet

3. Ajouter des collaborateurs si vous travaillez en équipe:
   - Allez dans "Settings" > "Manage access"
   - Cliquez sur "Invite a collaborator"
   - Entrez le nom d'utilisateur ou l'email de la personne à inviter

## Remarques importantes

- N'oubliez pas que le fichier `.gitignore` a été configuré pour exclure la base de données SQLite (`db.sqlite3`), les fichiers média et les informations sensibles. Si vous avez besoin de partager ces fichiers avec d'autres développeurs, vous devrez le faire par d'autres moyens.
- Si vous modifiez votre code localement, n'oubliez pas de faire un commit et un push pour mettre à jour le dépôt GitHub:
  ```bash
  git add .
  git commit -m "Description des modifications"
  git push
  ```