import pandas as pd
import numpy as np
import sys

# Vérification des paramètres
if len(sys.argv) != 3:
    print("Utilisation : python script.py <delta_max> <output_file>")
    sys.exit(1)

# Récupération des paramètres
delta_max = float(sys.argv[1])  # Delta maximal pour définir l'intervalle de la moyenne_delta_ponderee
output_file = sys.argv[2]       # Nom du fichier de sortie

# Définir les notes de 20 à 0, par quart de point
note_max = 20
note_min = 0
notes = np.arange(note_max, note_min - 0.25, -0.25)

# Calculer les intervalles pour moyenne_delta_ponderee, en les arrondissant à 2 chiffres
delta_intervals = np.round(np.linspace(0, delta_max, len(notes) + 1), 2)

# Construire le DataFrame de correspondance
correspondance_df = pd.DataFrame({
    'moyenne_delta_ponderee_min': delta_intervals[:-1],
    'moyenne_delta_ponderee_max': delta_intervals[1:],
    'note_sur_20': notes
})

# Sauvegarder le tableau en CSV
correspondance_df.to_csv(output_file, index=False)
print(f"Table de correspondance générée : {output_file}")
