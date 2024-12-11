// Importation du framework Express
const express = require('express');

// Création de l'application Express
const app = express();

// Définition du port d'écoute
const PORT = process.env.PORT || 3000;

// Route par défaut
app.get('/', (req, res) => {
    res.send('Bienvenue sur votre application Node.js avec Docker!');
});

// Démarrage du serveur
app.listen(PORT, () => {
    console.log(`Le serveur est en cours d'exécution sur le port ${PORT}`);
});
