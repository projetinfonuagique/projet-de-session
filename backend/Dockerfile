# Utilisation de l'image Python légère
FROM python:3.11-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers nécessaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port de l'API
EXPOSE 8000

# Commande pour démarrer l'API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
