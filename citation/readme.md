Application de Gestion de Citations
Description

Cette application permet aux utilisateurs de découvrir, partager et interagir avec des citations inspirantes, humoristiques, philosophiques, et bien d'autres. Les utilisateurs peuvent explorer des citations par catégories, ajouter des commentaires, noter les citations, les marquer comme favorites, et signaler des contenus inappropriés.
Fonctionnalités Principales
1. Gestion des Citations

    Ajout de citations : Les utilisateurs peuvent ajouter des citations avec un texte, un auteur et une catégorie.

    Catégories : Les citations sont organisées par catégories (ex: Inspiration, Humour, Philosophie).

    Tags : Les citations peuvent être associées à des tags pour une recherche plus flexible.

    Recherche : Les utilisateurs peuvent rechercher des citations par texte, auteur, catégorie ou tag.

2. Interaction Utilisateur

    Commentaires : Les utilisateurs peuvent laisser des commentaires sur les citations et répondre aux commentaires existants.

    Évaluations : Les utilisateurs peuvent noter les citations sur une échelle de 1 à 5.

    Favoris : Les utilisateurs peuvent enregistrer leurs citations préférées dans une liste de favoris pour un accès rapide.

    Signalements : Les utilisateurs peuvent signaler des citations inappropriées pour modération.

3. Gestion des Utilisateurs

    Authentification : Les utilisateurs doivent être connectés pour ajouter des citations, commenter, noter, ou marquer des favoris.

    Profil Utilisateur : Les utilisateurs peuvent voir leurs citations, commentaires, favoris et activités récentes.

4. Administration

    Modération : Les administrateurs peuvent gérer les signalements, supprimer des citations inappropriées, et gérer les utilisateurs.

    Gestion des Catégories et Tags : Les administrateurs peuvent ajouter, modifier ou supprimer des catégories et des tags.

Modèles Principaux
1. Citation (Quote)

    Texte : Le texte de la citation.

    Auteur : L'auteur de la citation (optionnel).

    Catégorie : La catégorie à laquelle la citation appartient.

    Tags : Les tags associés à la citation.

    Utilisateur : L'utilisateur qui a ajouté la citation.

2. Catégorie (Category)

    Nom : Le nom de la catégorie (ex: Inspiration, Humour).

    Description : Une description de la catégorie (optionnelle).

3. Tag (Tag)

    Nom : Le nom du tag (ex: Motivation, Succès).

4. Commentaire (Comment)

    Citation : La citation à laquelle le commentaire est associé.

    Utilisateur : L'utilisateur qui a posté le commentaire.

    Texte : Le texte du commentaire.

    Commentaire Parent : Permet de créer des réponses imbriquées à d'autres commentaires.

5. Évaluation (Rating)

    Citation : La citation notée.

    Utilisateur : L'utilisateur qui a donné la note.

    Score : La note attribuée (de 1 à 5).

6. Favori (Favorite)

    Utilisateur : L'utilisateur qui a ajouté la citation aux favoris.

    Citation : La citation marquée comme favorite.

7. Signalement (Report)

    Citation : La citation signalée.

    Utilisateur : L'utilisateur qui a signalé la citation.

    Raison : La raison du signalement.

    Résolu : Indique si le signalement a été traité.

Exemples d'Utilisation
Ajouter une Citation
python
Copy

category = Category.objects.create(name="Inspiration", description="Citations inspirantes")
quote = Quote.objects.create(text="The only limit is your imagination.", author="Anonymous", category=category)

Ajouter un Commentaire
python
Copy

comment = Comment.objects.create(quote=quote, user=user, text="Great quote!")

Noter une Citation
python
Copy

rating = Rating.objects.create(quote=quote, user=user, score=5)

Ajouter une Citation aux Favoris
python
Copy

favorite = Favorite.objects.create(user=user, quote=quote)

Signaler une Citation
python
Copy

report = Report.objects.create(quote=quote, user=user, reason="Inappropriate content")

Installation

    Cloner le dépôt :
    bash
    Copy

    git clone https://github.com/votre-utilisateur/votre-repo.git
    cd votre-repo

    Installer les dépendances :
    bash
    Copy

    pip install -r requirements.txt

    Configurer la base de données :

        Modifier les paramètres de la base de données dans settings.py.

        Appliquer les migrations :
        bash
        Copy

        python manage.py migrate

    Lancer le serveur de développement :
    bash
    Copy

    python manage.py runserver

    Accéder à l'application :

        Ouvrez votre navigateur et accédez à http://127.0.0.1:8000.

Contribution

Les contributions sont les bienvenues ! Si vous souhaitez contribuer, veuillez suivre les étapes suivantes :

    Forker le projet.

    Créer une branche pour votre fonctionnalité (git checkout -b feature/NouvelleFonctionnalité).

    Committer vos changements (git commit -m 'Ajouter une nouvelle fonctionnalité').

    Pousser vers la branche (git push origin feature/NouvelleFonctionnalité).

    Ouvrir une Pull Request.
