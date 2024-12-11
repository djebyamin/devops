// Importation des modules nécessaires
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 5000; // Le backend écoute sur le port 5000

// Middleware pour parser le JSON
app.use(bodyParser.json());
app.use(cors()); // Pour permettre les requêtes cross-origin

// Simuler un modèle de classification (ici, simplement une réponse statique)
const classifyUsingSVM = (base64Audio) => "Rock";  // Exemple pour le modèle SVM
const classifyUsingVGG19 = (base64Audio) => "Jazz";  // Exemple pour le modèle VGG19

// Route pour classifier la musique
app.post('/api/classify/:model', (req, res) => {
  const { model } = req.params;
  const { wav_music } = req.body;

  if (!wav_music) {
    return res.status(400).json({ error: 'Fichier audio non fourni' });
  }

  try {
    let genre;
    if (model === 'svm') {
      genre = classifyUsingSVM(wav_music);  // Classification via SVM
    } else if (model === 'vgg19') {
      genre = classifyUsingVGG19(wav_music);  // Classification via VGG19
    } else {
      return res.status(400).json({ error: 'Modèle non supporté' });
    }

    res.status(200).json({ genre });  // Retourne le genre classifié
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Erreur interne du serveur' });
  }
});

// Lancement du serveur
app.listen(PORT, () => {
  console.log(`Backend en cours d'exécution sur http://localhost:${PORT}`);
});
