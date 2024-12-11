import json
import pickle
import os

# Charger le fichier JSON
with open('./data.json', 'r') as f:
    data = json.load(f)

# Créer un répertoire pour stocker le fichier si nécessaire
output_dir = './SVM'
os.makedirs(output_dir, exist_ok=True)  # Crée le répertoire SVM si il n'existe pas

# Sauvegarder les données sous forme de fichier pickle dans le répertoire SVM
output_file = os.path.join(output_dir, 'data.pkl')
with open(output_file, 'wb') as f:
    pickle.dump(data, f)

print(f"Le fichier a été converti en .pkl et sauvegardé sous {output_file}")
