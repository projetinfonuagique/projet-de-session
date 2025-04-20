# Utilisation de l'image Node.js pour build
FROM node:20 AS builder

# Définition du répertoire de travail
WORKDIR /app

# Copie et installation des dépendances
COPY package.json package-lock.json ./
RUN npm install

# Copie du code source et build
COPY . .
RUN npm run build

# Utilisation de Nginx pour servir le frontend#178
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html

# Exposition du port 80
EXPOSE   80

CMD ["nginx", "-g", "daemon off;"]
