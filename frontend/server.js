const classifyMusic = async () => {
    if (!file) {
      setError('Veuillez télécharger un fichier audio ou enregistrer un son');
      return;
    }
  
    try {
      const response = await fetch('http://localhost:5000/api/classify/' + classificationModel, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ wav_music: file })
      });
  
      if (!response.ok) {
        throw new Error('Erreur lors de la classification');
      }
  
      const data = await response.json();
      setResult(data.genre); // Affiche le genre détecté
      setError(null);
    } catch (err) {
      setError(err.message);
      setResult(null);
    }
  };
  