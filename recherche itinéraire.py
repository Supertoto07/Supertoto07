import requests
import sqlite3
from datetime import datetime

# Configuration API SNCF
API_KEY = "d753cf68-e596-41a5-8ef4-a08531236ae4"  # Remplacez par votre clé SNCF
URL_BASE = "https://api.sncf.com/v1/coverage/sncf"

# Connexion à la base de données SQLite
conn = sqlite3.connect("trajets.db")
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS trajets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    depart TEXT,
    arrivee TEXT,
    heure_depart TEXT,
    heure_arrivee TEXT,
    prix REAL
);
""")
conn.commit()

# Fonction pour récupérer le code UIC d'une gare à partir de son nom
def get_uic_code(nom_gare):
    response = requests.get(f"{URL_BASE}/places?q={nom_gare}", auth=(API_KEY, ""))
    data = response.json()
    
    for place in data.get("places", []):
        if place.get("embedded_type") == "stop_area":
            return place["id"].split(":")[-1]  # Extraire le code UIC
    return None

# Fonction pour rechercher les trajets en fonction des codes UIC
def rechercher_trajets(depart, arrivee, datetime_depart):
    print("\n Recherche des trajets en cours...")

    response = requests.get(
        f"{URL_BASE}/journeys?from=stop_area:SNCF:{depart}&to=stop_area:SNCF:{arrivee}&datetime={datetime_depart}",
        auth=(API_KEY, "")
    )

    if response.status_code == 200:
        data = response.json()
        trajets = []

        for journey in data.get("journeys", []):
            heure_depart = journey["departure_date_time"]
            heure_arrivee = journey["arrival_date_time"]
            prix = journey.get("fare", {}).get("total", None)

            # Vérification et conversion du prix
            if isinstance(prix, dict) and "value" in prix:
                prix = float(prix["value"])
            elif isinstance(prix, (str, int, float)):
                try:
                    prix = float(prix)
                except ValueError:
                    prix = None
            
            # Formatage des heures
            heure_depart = datetime.strptime(heure_depart, "%Y%m%dT%H%M%S").strftime("%d/%m/%Y %H:%M")
            heure_arrivee = datetime.strptime(heure_arrivee, "%Y%m%dT%H%M%S").strftime("%d/%m/%Y %H:%M")

            print(f" Départ: {heure_depart}, Arrivée: {heure_arrivee}, Prix: {prix}€")

            trajets.append((nom_depart, nom_arrivee, heure_depart, heure_arrivee, prix))

        # Sauvegarde dans la base de données
        cursor.executemany("INSERT INTO trajets (depart, arrivee, heure_depart, heure_arrivee, prix) VALUES (?, ?, ?, ?, ?)", trajets)
        conn.commit()
        print(" Trajets enregistrés dans la base de données.")

    else:
        print("Erreur API SNCF:", response.status_code, response.text)

# Fonction principale
if __name__ == "__main__":
    while True:
        print(" SNCF Recherche de trajets")

        # Demande de la gare de départ et d'arrivée
        nom_depart = input("️ Entrez la ville de départ (précisé la gare) : ").strip()
        nom_arrivee = input("️Entrez la ville d'arrivée (précisé la gare) : ").strip()

        # Récupération des codes UIC
        code_depart = get_uic_code(nom_depart)
        code_arrivee = get_uic_code(nom_arrivee)

        if not code_depart or not code_arrivee:
            print(" Impossible de trouver l'une des gares. Vérifiez les noms.")
            continue

        # Demande de la date et heure de départ
        date_depart = input(" Entrez la date de départ (format JJ/MM/AAAA) : ").strip()
        heure_depart = input(" Entrez l'heure de départ (format HH:MM) : ").strip()

        try:
            # Formatage en ISO 8601 pour l'API SNCF
            datetime_depart = datetime.strptime(f"{date_depart} {heure_depart}", "%d/%m/%Y %H:%M").strftime("%Y%m%dT%H%M%S")
        except ValueError:
            print(" Format de date ou d'heure invalide.")
            continue

        # Lancer la recherche
        rechercher_trajets(code_depart, code_arrivee, datetime_depart)
