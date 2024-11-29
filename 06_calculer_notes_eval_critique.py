import pandas as pd
import sys

# Vérification des paramètres
if len(sys.argv) != 3:
    print("Utilisation : python script.py <file_notes_etudiants> <output_file>")
    sys.exit(1)

# Récupération des paramètres
file_notes_etudiants = sys.argv[1]
output_file = sys.argv[2]

# Chargement du fichier des notes des étudiants
notes_etudiants_df = pd.read_csv(file_notes_etudiants)

# Fonction pour extraire le groupe et la note de chaque évaluation
def extract_evaluation(row):
    if row['groupeEval'] == 'NR' or row['Statut'] == 'ABS':  # Garder vide si absent
        return ('', '')
    return (f"Groupe {row['groupeEval']}", f"{row['note_sur_20']}".replace('.', ','))

# Ajouter les colonnes pour le groupe et la note de chaque évaluation
notes_etudiants_df[['Groupe', 'Note']] = notes_etudiants_df.apply(extract_evaluation, axis=1, result_type='expand')

# Grouper par étudiant et organiser les évaluations dans des colonnes séparées
summary = notes_etudiants_df.groupby(['nom', 'prenom', 'Statut', 'groupeTD', 'groupeTP']).agg(
    Evaluation1=('Groupe', lambda x: x.iloc[0] if len(x) > 0 else ''),
    Note_Evaluation1=('Note', lambda x: x.iloc[0] if len(x) > 0 else ''),
    Evaluation2=('Groupe', lambda x: x.iloc[1] if len(x) > 1 else ''),
    Note_Evaluation2=('Note', lambda x: x.iloc[1] if len(x) > 1 else ''),
    Evaluation3=('Groupe', lambda x: x.iloc[2] if len(x) > 2 else ''),
    Note_Evaluation3=('Note', lambda x: x.iloc[2] if len(x) > 2 else '')
).reset_index()

# Calcul de la moyenne pour la note finale avec deux décimales
def calculate_final_note(row):
    # Vérifier si l'étudiant est absent et ne rien afficher dans ce cas
    if row['Statut'] == 'ABS':
        return ""
    notes = [float(note.replace(',', '.')) for note in [row['Note_Evaluation1'], row['Note_Evaluation2'], row['Note_Evaluation3']] if note]
    average = round(sum(notes) / len(notes), 2) if notes else 0
    return f"{average:.2f}".replace('.', ',')

# Ajouter la colonne de note finale
summary['Note finale'] = summary.apply(calculate_final_note, axis=1)

# Ajouter la colonne Remarques
def add_remark(row):
    count = sum([1 for note in [row['Note_Evaluation1'], row['Note_Evaluation2'], row['Note_Evaluation3']] if note])
    if count == 1:
        return "Moyenne calculée sur une évaluation"
    elif count == 2:
        return "Moyenne calculée sur deux évaluations"
    return ""

summary['Remarques'] = summary.apply(add_remark, axis=1)

# Sauvegarde du fichier résumé avec les évaluations et la note finale
summary.to_csv(output_file, index=False)
print(f"Fichier généré avec les notes finales : {output_file}")
