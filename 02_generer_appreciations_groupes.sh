#!/bin/bash

# Définir les fichiers d'entrée et de sortie pour chaque exercice
file_reponses_profs_1="01_reponses_profs_dernier_exo.csv"
file_reponses_profs_2="01_reponses_profs_autre_exo.csv"

output_file_1="appreciations_groupes_dernier_exo.txt"
output_file_2="appreciations_groupes_autre_exo.txt"
output_file_combined="appreciations_groupes_synthese.txt"

# Variables pour les titres des sections d'appréciations
titre_exo_1="Appréciations sur le dernier exercice déposé sur Elearn :"
titre_exo_2="Appréciations sur l'exercice choisi par l'enseignant :"


# Vérifier si les fichiers d'entrée existent
if [ ! -f "$file_reponses_profs_1" ] || [ ! -f "$file_reponses_profs_2" ]; then
    echo "Erreur : Un ou plusieurs fichiers de réponses des professeurs sont manquants."
    exit 1
fi

# Générer les appréciations pour chaque fichier de réponses des profs
python3 02_generer_appreciations_groupes.py "$file_reponses_profs_1" "$output_file_1"
python3 02_generer_appreciations_groupes.py "$file_reponses_profs_2" "$output_file_2"

# Vérifier la génération des fichiers d'appréciations
if [ ! -f "$output_file_1" ] || [ ! -f "$output_file_2" ]; then
    echo "Erreur : Un ou plusieurs fichiers d'appréciations n'ont pas été générés."
    exit 1
fi

# Créer le fichier de synthèse combinant les appréciations des deux fichiers
> "$output_file_combined"  # Effacer le fichier de sortie s'il existe déjà

# Fonction pour lire et organiser les appréciations par groupe
organiser_appreciations_par_groupe() {
    local input_file="$1"
    local title="$2"
    local -n appreciations_map="$3"

    local current_group=""
    local current_appreciation=""

    while IFS= read -r line; do
        # Identifier le début d'un nouveau groupe
        if [[ "$line" =~ ^Groupe\ ([0-9]+) ]]; then
            # Ajouter l'appréciation précédente dans le dictionnaire
            if [ -n "$current_group" ]; then
                appreciations_map["$current_group"]+="${title}\n***********************************************************\n${current_appreciation}\n"
            fi
            # Initialiser pour le nouveau groupe
            current_group="${BASH_REMATCH[1]}"
            current_appreciation=""
        else
            # Ajouter les lignes d'appréciation
            current_appreciation+="$line\n"
        fi
    done < "$input_file"

    # Ajouter la dernière appréciation du fichier
    if [ -n "$current_group" ]; then
        appreciations_map["$current_group"]+="${title}\n***********************************************************\n${current_appreciation}\n"
    fi
}

# Créer un dictionnaire associatif pour stocker les appréciations par groupe
declare -A appreciations

# Lire et organiser les appréciations des deux fichiers
organiser_appreciations_par_groupe "$output_file_1" "$titre_exo_1" appreciations
organiser_appreciations_par_groupe "$output_file_2" "$titre_exo_2" appreciations

# Trier les groupes par numéro et écrire les appréciations combinées dans le fichier de synthèse
for group in $(printf "%s\n" "${!appreciations[@]}" | sort -n); do
    echo "=========================" >> "$output_file_combined"
    echo "Groupe $group" >> "$output_file_combined"
    echo "=========================" >> "$output_file_combined"
    echo -e "${appreciations[$group]}" >> "$output_file_combined"
    echo "" >> "$output_file_combined"
done

echo "Fichier combiné généré : $output_file_combined"
