import pandas as pd
import sys

def transformer_reponses(input_file, output_file):
    # Lire le fichier CSV d'origine
    df = pd.read_csv(input_file)

    # Conserver les colonnes nécessaires existantes dans le fichier
    columns_to_keep = [col for col in ['nom', 'prenom', 'idCopie', 'groupeTD', 'groupeTP', 'groupe.eval', 'Note'] if col in df.columns]
    ticked_columns = [col for col in df.columns if col.startswith("TICKED:")]

    # Éliminer explicitement `groupe.eval[1]` et `groupe.eval[2]` pour éviter les erreurs
    if 'groupe.eval[1]' in df.columns:
        df = df.drop(columns=['groupe.eval[1]'])
    if 'groupe.eval[2]' in df.columns:
        df = df.drop(columns=['groupe.eval[2]'])

    # Renommer les colonnes TICKED pour enlever le préfixe 'TICKED:'
    renamed_ticked_columns = {col: col.replace("TICKED:", "") for col in ticked_columns}
    df = df[columns_to_keep + ticked_columns].rename(columns=renamed_ticked_columns)

    # Transformer la colonne 'Note' en 'Statut', avec "ABS" pour les absents et "PRES" pour les présents
    if 'Note' in df.columns:
        df['Statut'] = df['Note'].apply(lambda x: 'ABS' if x == 'ABS' else 'PRES')
        df = df.drop(columns=['Note'])  # Supprimer l'ancienne colonne 'Note'
    else:
        df['Statut'] = "PRES"  # Si 'Note' n'existe pas, mettre "PRES" par défaut

    # Remplacer les valeurs de `groupe.eval` par "NR" si elles sont vides, et convertir en entiers sinon
    if 'groupe.eval' in df.columns:
        df['groupe.eval'] = df['groupe.eval'].fillna("NR").apply(lambda x: int(float(x)) if x != "NR" else "NR")
        # Renommer `groupe.eval` en `groupeEval`
        df = df.rename(columns={'groupe.eval': 'groupeEval'})

    # Convertir les colonnes de réponses (renommées `TICKED`) : A->0, B->1, etc., et remplacer valeurs manquantes par "NR"
    def convert_ticked_value(value):
        if pd.isna(value):
            return "NR"
        mapping = {'A': '0', 'B': '1', 'C': '2', 'D': '3', 'E': '4', 'F': '5', 'G': '6', 'H': '7'}
        result = ''.join(mapping.get(char, char) for char in str(value) if char in mapping or char == "NR")
        return result if len(result) == 1 else "PRC"  # Retourner "PRC" si plusieurs réponses sont cochées

    # Appliquer la conversion seulement aux colonnes de questions
    for col in renamed_ticked_columns.values():
        if col in df.columns:
            df[col] = df[col].apply(convert_ticked_value)

    # Ne remplacer les valeurs supérieures à 9 par "PRC" que dans les colonnes de questions, pas dans `groupeEval`
    def replace_high_values(val):
        try:
            return "PRC" if int(val) > 9 else val
        except ValueError:
            return val  # Retourner la valeur inchangée si ce n'est pas un entier

    # Appliquer la fonction uniquement aux colonnes de questions
    for col in renamed_ticked_columns.values():
        if col in df.columns:
            df[col] = df[col].apply(replace_high_values)

    # Réorganiser les colonnes pour placer 'Statut' juste après 'prenom'
    columns_order = ['nom', 'prenom', 'Statut', 'idCopie', 'groupeTD', 'groupeTP', 'groupeEval'] + list(renamed_ticked_columns.values())
    df = df[[col for col in columns_order if col in df.columns]]

    # Supprimer les deux dernières colonnes du DataFrame
    df = df.iloc[:, :-2]

    # Sauvegarder le fichier CSV de sortie sans la légende
    df.to_csv(output_file, index=False)
    print(f"Le fichier transformé a été enregistré sous '{output_file}' sans la légende.")

# Vérification des arguments en ligne de commande
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transformer_reponses.py <fichier_entrée> <fichier_sortie>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        transformer_reponses(input_file, output_file)
