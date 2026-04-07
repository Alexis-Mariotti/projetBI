Ce projet uttilise la bibliotheque `python-dotenv` pour gérer les fichier .env
Ce format est uttiliser pour stocker les informations de connexion à Boursorama.

Pour instaler le package, uttiliser la commande `pip install python-dotenv`.

**/!\ Pensez à renseigner vos identifiants dans le fichier `.env` pour que le scrapper fonctionne**

## Liste des dépendances 

- python-dotenv (fichiers .env)
  - `pip install python-dotenv`
- pandas (fichiers csv)
  - `pip install pandas`
- sqlalchemy (ORM sql)
  - `pip install sqlalchemy mariadb`

## Liste des conteneurs Docker

- mariaDB : système de gestion de base de donnée de l'application
  - Utilisation du DATABASE_URL dans le fichier ``.env`` pour se connecter à la base
- phpmyadmin : application web de gestion d'SGBD 
  - Accessible depuis : `http://localhost:8080/`

## Lancement des conteneur docker 

- Utilisation de la commande ``docker compose up``