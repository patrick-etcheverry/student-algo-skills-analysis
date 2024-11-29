import pandas as pd
import sys

# Vérification des paramètres
if len(sys.argv) != 5:
    print("Utilisation : python script.py <file_etudiants_deltas> <file_poids_criteres> <file_correspondance> <output_file>")
    sys.exit(1)

# Récupération des paramètres
file_etudiants_deltas = sys.argv[1]
file_poids_criteres = sys.argv[2]
file_correspondance = sys.argv[3]
output_file = sys.argv[4]

# Chargement des fichiers CSV
etudiants_deltas = pd.read_csv(file_etudiants_deltas)
poids_criteres = pd.read_csv(file_poids_criteres)
correspondance_delta_note = pd.read_csv(file_correspondance)

# Extraire les critères et leurs poids
criteria_columns = poids_criteres.columns.tolist()
poids = poids_criteres.iloc[0].tolist()

# Calcul du delta global pondéré pour chaque étudiant
delta_columns = [f"{crit}-delta" for crit in criteria_columns]
etudiants_deltas['moyenne_delta_ponderee'] = etudiants_deltas[delta_columns].apply(
    lambda row: sum(row[crit] * poids[i] for i, crit in enumerate(delta_columns)) / sum(poids),
    axis=1
)

# Assigner une note sur 20 basée sur moyenne_delta_ponderee en utilisant la correspondance
def assign_note(moyenne_delta):
    # Trouver la note correspondante selon l'intervalle de moyenne_delta_ponderee
    row = correspondance_delta_note[
        (moyenne_delta >= correspondance_delta_note['moyenne_delta_ponderee_min']) &
        (moyenne_delta < correspondance_delta_note['moyenne_delta_ponderee_max'])
    ]
    return row['note_sur_20'].values[0] if not row.empty else 0  # Valeur par défaut 0 si aucun intervalle trouvé

etudiants_deltas['note_sur_20'] = etudiants_deltas['moyenne_delta_ponderee'].apply(assign_note)

# Sélectionner les colonnes finales pour l'export
output_columns = ['nom', 'prenom', 'Statut', 'idCopie', 'groupeTD', 'groupeTP', 'groupeEval', 'moyenne_delta_ponderee', 'note_sur_20']
etudiants_notes_finales = etudiants_deltas[output_columns]

# Sauvegarder le fichier de sortie
etudiants_notes_finales.to_csv(output_file, index=False)
print(f"Fichier généré avec les notes finales : {output_file}")
