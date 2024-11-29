import csv
import os
import sys

def create_mapping(master_csv, prenom_col, nom_col):
    """
    Crée un fichier de correspondance `name_mapping.csv` à partir du fichier maître.

    Args:
        master_csv (str): Chemin vers le fichier maître contenant les prénoms et noms.
        prenom_col (str): Nom de la colonne contenant les prénoms.
        nom_col (str): Nom de la colonne contenant les noms.
    """
    mapping_file = "name_mapping.csv"
    name_mapping = {}

    if os.path.exists(mapping_file):
        print(f"Un fichier de correspondance '{mapping_file}' existe déjà. Supprimez-le si nécessaire.")
        return

    # Lire les données en conservant l'ordre
    with open(master_csv, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            prenom = row[prenom_col].strip()
            nom = row[nom_col].strip()
            full_name = f"{prenom} {nom}"

            if full_name not in name_mapping:
                # Générer un identifiant unique basé sur le nombre d'entrées
                identifiant = f"{len(name_mapping) + 1:03d}"
                prenom_anonymise = f"prenomEtudiant_{identifiant}"
                nom_anonymise = f"nomEtudiant_{identifiant}"
                name_mapping[full_name] = {
                    "prenom": prenom,
                    "nom": nom,
                    "prenom_anonymise": prenom_anonymise,
                    "nom_anonymise": nom_anonymise,
                }

    # Sauvegarder le fichier de correspondance
    with open(mapping_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["prenom", "nom", "prenom_anonymise", "nom_anonymise"])
        writer.writeheader()
        for data in name_mapping.values():
            writer.writerow(data)

    print(f"Fichier de correspondance créé : {mapping_file}")


def anonymize_csv(input_csv, output_csv):
    """
    Anonymise un fichier CSV en utilisant le fichier de correspondance existant.

    Args:
        input_csv (str): Chemin vers le fichier CSV à anonymiser.
        output_csv (str): Chemin pour sauvegarder le fichier anonymisé.
    """
    mapping_file = "name_mapping.csv"
    if not os.path.exists(mapping_file):
        print(f"Fichier de correspondance '{mapping_file}' introuvable. Veuillez créer le mapping d'abord.")
        return

    # Charger le mapping
    with open(mapping_file, "r") as f:
        reader = csv.DictReader(f)
        name_mapping = {f"{row['prenom']} {row['nom']}": (row["prenom_anonymise"], row["nom_anonymise"]) for row in reader}

    # Anonymiser le fichier d'entrée
    with open(input_csv, "r") as infile, open(output_csv, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            prenom = row.get("prenom", "").strip()
            nom = row.get("nom", "").strip()
            full_name = f"{prenom} {nom}"

            if full_name in name_mapping:
                # Remplacer prénom et nom par les valeurs anonymisées
                row["prenom"], row["nom"] = name_mapping[full_name]
            writer.writerow(row)

    print(f"Fichier anonymisé sauvegardé : {output_csv}")


if __name__ == "__main__":
    # Phase 1 : Créer le mapping
    master_csv = "00_reponses_etudiants.csv"
    prenom_col = "prenom"
    nom_col = "nom"

    # Créer le mapping si nécessaire
    if not os.path.exists("name_mapping.csv"):
        create_mapping(master_csv, prenom_col, nom_col)

    # Phase 2 : Anonymiser les fichiers fournis
    if len(sys.argv) < 2:
        print("Usage : python anonymizer.py <fichier1.csv> <fichier2.csv> ...")
        sys.exit(1)

    files_to_anonymize = sys.argv[1:]
    for input_file in files_to_anonymize:
        output_file = f"anonymized_{os.path.basename(input_file)}"
        anonymize_csv(input_file, output_file)
