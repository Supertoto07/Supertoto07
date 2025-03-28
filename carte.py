import folium
import webbrowser
import os
import sys
import json

def tracer_trajet(gares):
    """
    Trace un trajet sur une carte et l'ouvre dans le navigateur.
    :param gares: Dictionnaire contenant le nom des gares et leurs coordonnées (latitude, longitude).
    """
    if not gares:
        print("Le dictionnaire des gares est vide.")
        return

    # Créer une carte centrée sur la première gare
    first_station = next(iter(gares.values()))
    m = folium.Map(location=first_station, zoom_start=12)

    # Ajouter les points de trajet à la carte
    for nom, coord in gares.items():
        folium.Marker(location=coord, popup=nom).add_to(m)

    # Tracer le trajet
    folium.PolyLine(locations=list(gares.values()), color='blue', weight=5, opacity=0.7).add_to(m)

    # Créer une fenêtre d'information pour le trajet
    trajet_info = "<h4>Trajet :</h4><ul>"
    for nom in gares.keys():
        trajet_info += f"<li>{nom}</li>"
    trajet_info += "</ul>"

    # Ajouter la fenêtre d'information à la carte en haut à droite
    folium.Marker(
        location=first_station,
        icon=folium.DivIcon(
            html=f"""<div style="position: fixed; top: 10px; right: 10px; font-size: 16px; color: black; background-color: white; border: 2px solid black; padding: 10px; border-radius: 5px; z-index: 1000;">
                        {trajet_info}
                    </div>""",
            class_name='trajet-info'
        )
    ).add_to(m)

    # Sauvegarder la carte dans un fichier HTML
    file_path = "carte_trajet.html"
    m.save(file_path)

    # Ouvrir la carte dans le navigateur
    webbrowser.open('file://' + os.path.realpath(file_path))

def main():
    if len(sys.argv) < 2:
        print("Usage: python carte.py '<gares_json>'")
        return

    # Récupérer le JSON des gares depuis les arguments
    gares_json = sys.argv[1]
    gares = json.loads(gares_json)

    # Appeler la fonction pour tracer le trajet
    tracer_trajet(gares)

if __name__ == "__main__":
    main()