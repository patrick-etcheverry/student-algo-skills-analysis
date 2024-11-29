import pandas as pd
import sys

# Vérification des paramètres
if len(sys.argv) != 3:
    print("Utilisation : python script.py <file_reponses_profs> <output_file>")
    sys.exit(1)

# Récupération des paramètres
file_reponses_profs = sys.argv[1]
output_file = sys.argv[2]

# Chargement du fichier des réponses des profs
reponses_profs_df = pd.read_csv(file_reponses_profs)

# Définir les qualificatifs en fonction de la note
qualificatifs = {
    6: "Très bien",
    5: "Bien",
    4: "Assez bien",
    3: "Correct",
    2: "Insuffisant",
    1: "Très insuffisant",
    0: "À revoir complètement"
}

# Correspondance des noms des colonnes avec des descriptions précises des critères
noms_criteres = {
    "01-justification-modele-algo": "Justification du modèle algorithmique",
    "02-codage-modele-algo": "Codage du modèle algorithmique",
    "03-qualite-nommage-variable": "Qualité du nommage des variables",
    "04-precision-typage-variables": "Précision du typage des variables",
    "05-respect-conventions-nommage": "Respect des conventions de nommage",
    "06-pertinence-commentaires": "Pertinence des commentaires",
    "07-choix-structures-controle": "Choix des structures de contrôle",
    "08-indentation": "Indentation"
}

# Création des appréciations pour chaque groupe
with open(output_file, 'w') as f:
    for _, row in reponses_profs_df.iterrows():
        groupe = row['groupeEval']
        f.write(f"=========================\n")
        f.write(f"Groupe {groupe}\n")
        f.write(f"=========================\n")

        # Générer une appréciation pour chaque critère
        for col in reponses_profs_df.columns[1:-1]:  # Exclure 'groupeEval' et 'remarques'
            note = row[col]
            critere = noms_criteres.get(col, col)  # Obtenir le nom complet ou laisser tel quel si non trouvé
            appreciation = qualificatifs.get(note, "Non évalué")
            f.write(f"- {critere} : {appreciation}.\n")

        # Ajouter les remarques s'il y en a
        remarques = row['remarques']
        if pd.notna(remarques):
            f.write(f"Remarques : {remarques}\n")

        # Séparation entre les groupes
        f.write("\n")

print(f"Fichier d'appréciations généré : {output_file}")
