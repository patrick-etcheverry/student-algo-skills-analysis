# Indicateurs de Compétences Algorithmiques

Ce dépôt contient un ensemble de scripts et de fichiers permettant d'analyser des compétences algorithmiques mobilisées par des étudiants. Ces indicateurs sont calculés à partir des résultats obtenus dans le cadre d’un projet pédagogique visant à développer leur pensée algorithmique.

Dans ce projet, les étudiants ont résolu une série de défis algorithmiques présentés sous forme de katas. Ces défis les ont conduits à concevoir et mettre en œuvre des solutions qu'ils ont ensuite dû défendre face à des enseignants. En parallèle, les autres groupes d’étudiants étaient chargés d’évaluer la pertinence des solutions proposées par leurs camarades. Cette capacité d’évaluation a également été mesurée par les scripts disponibles dans ce dépôt.

Les scripts sont organisés pour anonymiser les données, effectuer des analyses approfondies, et produire des indicateurs précis permettant de suivre la progression des étudiants et de mesurer leur taux de réussite.

## Objectifs principaux

1. **Analyser les résultats algorithmiques :**
   - Traiter les réponses des étudiants issues des katas et des évaluations croisées.
   - Mesurer sous forme d'écarts (deltas) les évaluations qu'ils attribuent à leurs camarades avec les évaluations données par les enseignants sur ces mêmes camarades.

2. **Produire des indicateurs clés :**
   - Mesurer le taux de réussite global et par critère algorithmique.
   - Générer des rapports pour suivre la progression des étudiants.
   - Évaluer la qualité des évaluations réalisées par les étudiants eux-mêmes.

3. **Assurer l'anonymisation des données :**
   - Protéger l’identité des étudiants tout en permettant une analyse fiable des données.

## Contenu du dépôt

### 1. Données sources anonymisées
- `00_reponses_etudiants.csv` : Données initiales des réponses des étudiants (anonymisées) récupérées via l'outil AMC.
- `01_reponses_etudiants.csv` : Données prétraitées pour lecture simplifée.
- `03_reponses_etudiants_avec_deltas.csv` : Deltas entre les évaluations des étudiants et celles des enseignants.
- `05_notes_etudiants_par_fiche.csv` : Notes des étudiants pour chaque groupe qu'ils ont évalué.
- `06_notes_etudiants_eval_critique.csv` : Capacité d'un étudiant à évaluer correctement une production algorithmique (par rapport à un enseignant).
- `07_notes_defense_collective.csv` : Capacité d'un groupe d'étudiants à défendre des choix algorithmiques  pour résoudre deux exercices spécifiques.
- `08_niveau_atteint_niveau_valide.csv` : Données indiquant les niveaux visés par chaque groupe d'étudiants et le niveau réellement atteint.

### 2. Scripts Python
Ces scripts réalisent les analyses suivantes  :

- `anonymizer.py` : Anonymise les noms et prénoms dans les fichiers CSV.
- `01_clarifier_reponses.py` : Simplifie la lecture des réponses des étudiants.
- `02_generer_appreciations_groupes.py` : Génère des appréciations pour les groupes d'étudiants.
- `03_calculer_deltas.py` : Calcule les écarts (deltas) entre les évaluations des étudiants et celles des enseignants.
- `04_generer_tableau_correspondance_delta_note.py` : Génère une correspondance entre les écarts calculés et une note reflétant la capacité à évaluer une production réalisée par un pair .
- `05_calculer_notes_par_fiches.py` : Pour un étudiant donné calcule les notes qu'on lui attribue pour chaque groupe qu'il a évalué (en fonction de sa proximité avec les notes des enseignants).
- `06_calculer_notes_eval_critique.py` : Compile les notes obtenues par un étudiant pour la qualité de l'évaluation qu'il a attribuée à chaque groupe qu'il a jugé.
- `07_calculer_notes_defense_collective.py` : Calcule lanote obtenue par un groupe lors de la séance visant à défendre les choix algorithmiques réalisés lors de l'atelier de katas.

### 3. Scripts Bash
Ces scripts servent de wrappers pour exécuter les scripts Python et automatiser les tâches.

- `01_clarifier_reponses.sh` : Simplification  de la lecture des réponses données par les étudiants.
- `02_generer_appreciations_groupes.sh` : Automatisation de la génération d’appréciations délivrées à chaque groupe.
- `03_calculer_deltas.sh` : Automatisation du calcul des deltas étudiants <-->  enseignants
- `04_generer_tableau_correspondance_delta_note.sh` : Génération du tableau de correspondance compétence évaluation critique <--> note évaluation critique.
- `05_calculer_notes_par_fiches.sh` : Automatisation du calcul des notes par fiche d'évaluation critique.
- `06_calculer_notes_eval_critique.sh` : Calcul de la note finale sur la compétence "Capacité à évaluer une production par un pair"
- `07_calculer_notes_defense_collective.sh` : Calcul de la note obtenue suite à l'argumentation des choix algorithmiques réalisés lors de l'atelier de katas.

### 4. Fichiers de configuration
- `04_correspondance_delta_note.csv` : Correspondance entre les écarts et les notes à attribuer aux étudiants sur la capacité à évaluer la production d'un pair.
- `poids_criteres_eval_critique.csv` : Poids des critères pour l'évaluation critique.
- `poids_criteres_defense_collective.csv` : Poids des critères pour la défense collective.

## Instructions d'utilisation

### Anonymisation
1. Le script `anonymizer.py` permet d'anonymiser les données :
   - Commande pour générer le fichier de correspondance :
     python anonymizer.py
   - Commande pour anonymiser plusieurs fichiers :
     python anonymizer.py fichier1.csv fichier2.csv ...

### Analyse des compétences algorithmiques
1. Exécuter les scripts Python directement ou via les scripts Bash pour automatiser les tâches.
2. Exemple pour calculer les écarts (deltas) :
   bash 03_calculer_deltas.sh
3. Les rapports générés dans les fichiers CSV permettent de consulter les résultats et les taux de réussite.

## Auteur

Ce projet vise à fournir des outils d'analyse pour évaluer  l'apprentissage des compétences algorithmiques.

## Licence

Ce projet est sous licence libre. Vous êtes libre de l'adapter et de le partager dans le respect des droits d'auteur.
