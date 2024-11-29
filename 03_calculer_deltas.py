import pandas as pd
import sys

# Récupération des paramètres
if len(sys.argv) != 5:
    print("Utilisation : python script.py <MAX_SCORE> <file_etudiants> <file_profs> <output_file>")
    sys.exit(1)

MAX_SCORE = int(sys.argv[1])
file_etudiants = sys.argv[2]
file_profs = sys.argv[3]
output_file = sys.argv[4]

# Liste des colonnes de critères
criteria_columns = [
    "01-justification-modele-algo", "02-codage-modele-algo",
    "03-qualite-nommage-variable", "04-precision-typage-variables",
    "05-respect-conventions-nommage", "06-pertinence-commentaires",
    "07-choix-structures-controle", "08-indentation"
]

# Chargement des fichiers CSV
reponses_etudiants = pd.read_csv(file_etudiants, sep=None, engine='python')
reponses_profs = pd.read_csv(file_profs, sep=None, engine='python')

# Convertir 'groupeEval' en chaîne pour éviter les erreurs de fusion
reponses_etudiants['groupeEval'] = reponses_etudiants['groupeEval'].astype(str)
reponses_profs['groupeEval'] = reponses_profs['groupeEval'].astype(str)

# Fusionner les données des étudiants et des professeurs
merged_data = pd.merge(
    reponses_etudiants,
    reponses_profs,
    on='groupeEval',
    suffixes=('', '-prof'),
    how='left'
)

# Calcul des deltas et application des pénalisations
for criterion in criteria_columns:
    prof_col = f"{criterion}-prof"
    delta_col = f"{criterion}-delta"

    # Calcul du delta avec pénalisation pour 'NR' et 'PRC'
    merged_data[delta_col] = merged_data.apply(
        lambda row: MAX_SCORE if row[criterion] in ['NR', 'PRC'] else
                    abs(int(row[criterion]) - int(row[prof_col])) if pd.notnull(row[criterion]) and pd.notnull(row[prof_col]) and str(row[criterion]).isdigit()
                    else None,
        axis=1
    )

# Pénalisation globale si 'groupeEval' contient 'NR' ou 'PRC'
merged_data.loc[merged_data['groupeEval'].isin(['NR', 'PRC']), [f"{crit}-delta" for crit in criteria_columns]] = MAX_SCORE

# Réorganiser les colonnes pour chaque critère dans l'ordre souhaité : étudiant, prof, delta
ordered_columns = ['nom', 'prenom', 'Statut', 'idCopie', 'groupeTD', 'groupeTP', 'groupeEval']
for criterion in criteria_columns:
    ordered_columns.extend([criterion, f"{criterion}-prof", f"{criterion}-delta"])

# Reorder the DataFrame columns
merged_data = merged_data[ordered_columns]

# Convert numeric columns to integers where possible, skip non-numeric values like 'NR' or 'PRC'
for column in ordered_columns[7:]:  # Skip non-numeric columns
    if merged_data[column].dtype == 'float64':
        merged_data[column] = merged_data[column].fillna(0).astype(int)

# Sauvegarder le fichier de sortie
merged_data.to_csv(output_file, index=False)
print(f"Fichier généré : {output_file}")
