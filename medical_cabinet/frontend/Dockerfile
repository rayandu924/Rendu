# frontend/Dockerfile

# Utiliser une image officielle Nginx comme image de base
FROM nginx:alpine

# Supprimer le fichier de configuration par défaut de Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copier le fichier de configuration personnalisé
COPY nginx.conf /etc/nginx/conf.d

# Copier les fichiers frontend dans le dossier de Nginx
COPY . /usr/share/nginx/html

# Exposer le port 80
EXPOSE 80

# Démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]
