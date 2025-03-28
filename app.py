from flask import Flask, request, jsonify, render_template
import subprocess
import json

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

        # Créer un dictionnaire avec les gares et leurs coordonnées
        gares = {
            "Départ": (49.8448, 2.3730),  # Exemple de coordonnées
            "Arrivée": (48.8742, 2.3320)  # Exemple de coordonnées
        }

        # Convertir le dictionnaire en JSON
        gares_json = json.dumps(gares)

        # Exécuter le script Python avec les arguments
        result = subprocess.run(
            ['python', 'carte.py', gares_json],
            capture_output=True,
            text=True,
            timeout=5
        )
        return jsonify(output=result.stdout, error=result.stderr)
    except Exception as e:
        return jsonify(output='', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
