# Utilisez l'image PostgreSQL comme image de base
FROM postgres:latest

# Définition des variables d'environnement
ENV POSTGRES_DB=northwind
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Copiez le fichier SQL d'initialisation dans le conteneur
COPY ./northwind.sql /docker-entrypoint-initdb.d/northwind.sql

# Exposez le port PostgreSQL (5432)
EXPOSE 5432
