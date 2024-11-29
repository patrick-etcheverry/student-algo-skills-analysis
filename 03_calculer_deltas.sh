#!/bin/bash

# Définir les fichiers d'entrée et de sortie
file_etudiants="01_reponses_etudiants.csv"
file_profs="01_reponses_profs_autre_exo.csv"
output_file="03_reponses_etudiants_avec_deltas.csv"
max_score=6

# Exécuter le script Python pour calculer les deltas
python3 03_calculer_deltas.py "$max_score" "$file_etudiants" "$file_profs" "$output_file"


# Définir les couleurs (par exemple, bleu ou rouge  pour le nom du fichier prof)
BLUE='\033[1;34m'
RED='\033[1;31m'
NC='\033[0m' # Pas de couleur

# Afficher le message indiquant le fichier des professeurs utilisé
echo -e "Le calcul des deltas a été fait en utilisant comme référence les réponses enseignants stockées dans le fichier : ${RED}$file_profs${NC}"
echo "Editer le fichier 03_calculer_deltas.sh pour prendre un autre fichier de réponse en référence."

