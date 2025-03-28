from flask import Flask, request, jsonify, render_template, send_file
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        # Récupérer les valeurs des champs de texte
        start_location = request.form['start-location']
        arrival_location = request.form['arrival-location']

        print(f"Start Location: {start_location}")
        print(f"Arrival Location: {arrival_location}")

        # Créer un dictionnaire avec les gares et leurs coordonnées
        gares = {
            "Départ": (49.8448, 2.3730),  # Exemple de coordonnées
            "Arrivée": (48.8742, 2.3320)  # Exemple de coordonnées
        }

        # Convertir le dictionnaire en JSON
        gares_json = json.dumps(gares)

        # Chemin du fichier de sortie
        output_file = "static/carte_trajet.html"

        # Exécuter le script Python avec les arguments
        result = subprocess.run(
            ['python', 'carte.py', gares_json, output_file],
            capture_output=True,
            text=True,
            timeout=5
        )

        print(f"Subprocess Output: {result.stdout}")
        print(f"Subprocess Error: {result.stderr}")

        # Renvoyer le chemin du fichier HTML généré
        return jsonify(map_url=output_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify(output='', error=str(e))

@app.route('/map')
def get_map():
    return send_file('static/carte_trajet.html')

if __name__ == '__main__':
    app.run(debug=True)
