# Phase 2 — Baseline TF-IDF + régression logistique

**Responsable : Taoufik**

**Données nécessaires :** configuration `core` de `neuralchemy/Prompt-injection-dataset`, validée dans `01_exploration_eda/`.

## Objectif

Créer une première référence de classification avec une méthode classique sur `core`. Elle sera comparée à DistilBERT, entraîné sur `full`.

## Ce qu'il faut avoir avant de commencer

- La configuration `core` accessible et sa validation de source ;
- le compte rendu EDA et la décision « go » pour l'entraînement ;
- la définition des classes, le mapping vers les valeurs utilisées par les modèles et la classe positive ;
- les partitions train, validation et test déjà décidées, avec les groupes liés conservés ensemble ;
- un identifiant stable par exemple et un emplacement local pour les artefacts ;
- Python et les dépendances installées depuis `requirements.txt`.

La carte annonce que validation et test sont partagés avec `full`. Vérifier ce point en EDA avant comparaison. Si les exemples de test ne correspondent pas, prévenir Ayoub et documenter la limite.

## Suivi pas à pas

### 1. Vérifier les données d'entrée

Confirmer les tailles de splits et colonnes de `core`. Vérifier que les textes sont non vides, que les labels sont reconnus et que les identifiants sont uniques. Comparer ces informations au compte rendu EDA.

### 2. Définir le protocole de baseline

Écrire avant l'entraînement les choix à tester : représentation TF-IDF, paramètres du vocabulaire, n-grammes, régularisation de la régression logistique, gestion éventuelle du déséquilibre, graine et métrique de sélection. Garder le jeu de test fermé pendant tous les réglages.

### 3. Construire le pipeline

Le pipeline transforme le texte en caractéristiques TF-IDF puis entraîne une `LogisticRegression`. Le vectoriseur doit être ajusté sur train seulement. Les mêmes règles de préparation du texte s'appliquent à toutes les partitions ; préserver les formulations, marqueurs et ponctuations qui peuvent être des indices d'attaque.

### 4. Choisir les paramètres

Entraîner une variante de référence. Si plusieurs paramètres sont comparés, utiliser validation et une règle de choix annoncée à l'avance. Noter chaque variante et son résultat validation pour que le choix soit explicable. Ne pas choisir le meilleur modèle d'après le test.

### 5. Évaluer une fois sur test

Une fois les choix figés, calculer précision, rappel et F1 pour la classe malveillante, les supports par classe et la matrice de confusion. Conserver les scores/probabilités malveillants si disponibles. Examiner des erreurs représentatives, surtout les faux négatifs.

### 6. Exporter et transmettre

Exporter une ligne par exemple test avec `example_id`, `y_true`, `y_pred` et si possible `score_malicious`. Garder la même clé d'exemple et le même mapping que pour DistilBERT. Ajouter un petit fichier de métadonnées indiquant date, corpus/version, split, paramètres, graine et versions des bibliothèques.

## Livrables à déposer ou transmettre

1. Fiche d'expérience : protocole, paramètres essayés, choix final, graine, versions et matériel utile.
2. Résultats test : métriques, supports, matrice de confusion et commentaire sur les erreurs.
3. Export CSV des prédictions, conservant `example_id`, vérité terrain et prédiction.
4. Pipeline entraîné sauvegardé localement si le poids le permet ; ne pas ajouter un artefact volumineux au dépôt sans décision du binôme.
5. Message de passage à Ayoub et au responsable du dashboard confirmant corpus, split et format de l'export.

## Fichiers à produire dans ce dossier

| Fichier | Contenu attendu | À versionner ? |
|---|---|---|
| `baseline_experiment.md` | Corpus/version, split, transformations, paramètres essayés, critère de sélection, graine, versions logicielles et matériel. | Oui |
| `baseline_metrics.json` ou `baseline_metrics.csv` | Métriques finales et supports, classe positive, ordre des labels et référence au test utilisé. | Oui, chiffres uniquement |
| `baseline_test_predictions.csv` | Une ligne par exemple test : `example_id`, `y_true`, `y_pred`, `score_malicious` si disponible. | Selon les conditions des données ; ne pas inclure de texte source sans autorisation |
| `baseline_confusion_matrix.png` | Matrice de confusion annotée avec classes et axes. | Oui |
| `artifacts/` (local) | Pipeline entraîné complet et journaux utiles. | Non si lourd ; garder localement et ignorer par Git |

L'export conserve les identifiants stables du corpus. Si les prédictions ou exemples ne peuvent pas être partagés, les garder localement et transmettre les métriques autorisées.

## Checklist avant de remettre le travail

- [ ] Le corpus et les partitions correspondent à la version validée en phase 1.
- [ ] TF-IDF a été ajusté uniquement sur train.
- [ ] La validation, et non le test, a servi aux choix de paramètres.
- [ ] La classe positive et l'ordre des labels sont explicités.
- [ ] Les métriques incluent le support et la matrice de confusion.
- [ ] L'export contient un identifiant stable et s'aligne avec le futur export DistilBERT.
- [ ] Les erreurs et les limites de la baseline sont consignées.
