import pandas as pd
import sys

# Vérification des paramètres
if len(sys.argv) != 5:
    print("Utilisation : python 07_calculer_notes_defense_collective.py <file_autre_exo> <file_dernier_exo> <file_coefficients> <output_file>")
    sys.exit(1)

# Récupération des paramètres
file_autre_exo = sys.argv[1]
file_dernier_exo = sys.argv[2]
file_coefficients = sys.argv[3]
output_file = sys.argv[4]

# Chargement des fichiers
df_autre_exo = pd.read_csv(file_autre_exo)
df_dernier_exo = pd.read_csv(file_dernier_exo)
df_coefficients = pd.read_csv(file_coefficients)

# Préparation des coefficients
coefficients = df_coefficients.iloc[0].to_dict()
sum_of_weights = sum(coefficients.values())

# Fonction pour calculer la note avec la formule
def calculate_weighted_score(row, exercise_df):
    formula_parts = []
    weighted_sum = 0
    for critere, weight in coefficients.items():
        score = exercise_df.loc[row.name, critere]
        weighted_score = score * weight
        formula_parts.append(f"{score}*{weight}")
        weighted_sum += weighted_score
    formula = " + ".join(formula_parts) + f" / {sum_of_weights}"
    final_score = round(weighted_sum / sum_of_weights, 2)
    return formula.replace('.', ','), f"{final_score}".replace('.', ',')

# Calcul des notes pour Exo1
df_autre_exo['Calcul_Note_Exo1'], df_autre_exo['Note_Exo1_sur_6'] = zip(*df_autre_exo.apply(calculate_weighted_score, axis=1, exercise_df=df_autre_exo))
df_autre_exo['Note_Exo1_sur_20'] = (df_autre_exo['Note_Exo1_sur_6'].str.replace(',', '.').astype(float) * 20 / 6).round(2).astype(str).str.replace('.', ',')

# Calcul des notes pour Exo2
df_dernier_exo['Calcul_Note_Exo2'], df_dernier_exo['Note_Exo2_sur_6'] = zip(*df_dernier_exo.apply(calculate_weighted_score, axis=1, exercise_df=df_dernier_exo))
df_dernier_exo['Note_Exo2_sur_20'] = (df_dernier_exo['Note_Exo2_sur_6'].str.replace(',', '.').astype(float) * 20 / 6).round(2).astype(str).str.replace('.', ',')

# Fusionner les deux DataFrames sur le groupe évalué
result = pd.DataFrame()
result['groupeEval'] = df_autre_exo['groupeEval']
result['Calcul_Note_Exo1'] = df_autre_exo['Calcul_Note_Exo1']
result['Note_Exo1_sur_6'] = df_autre_exo['Note_Exo1_sur_6']
result['Note_Exo1_sur_20'] = df_autre_exo['Note_Exo1_sur_20']
result['Calcul_Note_Exo2'] = df_dernier_exo['Calcul_Note_Exo2']
result['Note_Exo2_sur_6'] = df_dernier_exo['Note_Exo2_sur_6']
result['Note_Exo2_sur_20'] = df_dernier_exo['Note_Exo2_sur_20']

# Sauvegarde du résultat final
result.to_csv(output_file, index=False)
print(f"Fichier généré avec les notes finales : {output_file}")
