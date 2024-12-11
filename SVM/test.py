import requests
import base64

def test_server():
    # Test de la route de base
    try:
        base_response = requests.get('http://localhost:5000/')
        print("Test route de base :", base_response.status_code, base_response.text)
    except Exception as e:
        print("Erreur lors du test de la route de base :", e)

    # Test de la classification
    try:
        # Charger un fichier audio à tester
        with open('votre_fichier_audio.wav', 'rb') as audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

        # Envoi de la requête
        response = requests.post('http://localhost:5000/classify', 
                                 data={'audio_data': audio_base64})
        
        print("Statut de la réponse :", response.status_code)
        print("Contenu de la réponse :", response.json())
    
    except requests.exceptions.RequestException as e:
        print("Erreur de requête :", e)
    except Exception as e:
        print("Erreur inattendue :", e)

# Lancer le test
test_server()