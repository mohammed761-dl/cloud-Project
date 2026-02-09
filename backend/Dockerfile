# Utiliser une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code (main.py)
COPY . .

# Exposer le port 80 (Standard pour K8s Internal Service)
EXPOSE 80

# Commande pour lancer l'API sur le port 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]