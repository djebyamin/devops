from flask import Flask, request, jsonify
import joblib
import librosa
import numpy as np
import os
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Restrict origins in production

# List of genres used in the model (ensure it matches your model's training data)
genres = ["rock", "jazz", "classical", "hiphop", "pop", "blues", "reggae", "metal", "disco", "country"]

# Ensure upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the model
MODEL_PATH = 'genre_model.pkl'
model = None
try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as model_file:
            model = joblib.load(model_file)
        print("Model loaded successfully!")
    else:
        print(f"Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {str(e)}")

def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)  # Increased MFCC to 20
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    combined_features = np.concatenate([mfcc.flatten(), chroma.flatten(), spectral_contrast.flatten()])
    if len(combined_features) > 1280:
        combined_features = combined_features[:1280]
    elif len(combined_features) < 1280:
        combined_features = np.pad(combined_features, (0, 1280 - len(combined_features)), 'constant')
    return combined_features

@app.route('/svm', methods=['POST'])
def predict():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        if not file.filename.endswith(('.wav', '.mp3', '.flac', '.ogg')):
            return jsonify({"error": "Invalid file type"}), 400

        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)

        features = extract_features(file_path).reshape(1, -1)
        predicted_genre_output = model.predict(features)[0]
        predicted_genre = genres[predicted_genre_output] if isinstance(predicted_genre_output, int) else predicted_genre_output

        return jsonify({"genre": predicted_genre})

    except Exception as e:
        return jsonify({"error": "Prediction failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
