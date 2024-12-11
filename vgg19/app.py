from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import base64
import io
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Charger le modèle VGG19 pré-entraîné
model = VGG19(weights='imagenet')

def audio_to_spectrogram(audio_file):
    """
    Convertit un fichier audio en un spectrogramme.
    """
    y, sr = librosa.load(audio_file, sr=None)  # Charger l'audio
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)  # Spectrogramme
    return D

@app.route('/vgg', methods=['POST'])
def classify_genre():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier audio fourni"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Aucun fichier audio sélectionné"}), 400

    try:
        # Convertir l'audio en un spectrogramme
        spectrogram = audio_to_spectrogram(file)

        # Sauvegarder le spectrogramme comme image temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            plt.figure(figsize=(10, 10))
            librosa.display.specshow(spectrogram, x_axis='time', y_axis='log')
            plt.colorbar(format='%+2.0f dB')
            plt.savefig(temp_file.name)
            plt.close()

            # Charger l'image du spectrogramme
            img = image.load_img(temp_file.name, target_size=(224, 224))  # Taille d'entrée de VGG19
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            # Faire la prédiction avec VGG19
            preds = model.predict(img_array)

            # Retourner la classification du genre musical (pour le test, en utilisant les classes ImageNet)
            decoded_preds = tf.keras.applications.vgg19.decode_predictions(preds, top=3)[0]
            genre = decoded_preds[0][1]  # Prendre la première prédiction comme genre

            # Convertir les prédictions en types sérialisables
            decoded_preds_serializable = [(label, description, float(prob)) for (label, description, prob) in decoded_preds]

        return jsonify({"genre": genre, "prediction": decoded_preds_serializable})

    except Exception as e:
        return jsonify({"error": f"Erreur lors du traitement de l'audio: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
