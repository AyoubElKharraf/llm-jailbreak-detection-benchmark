# Phase 1 — Valider la source et auditer les données

**Validation de la source : Ayoub**

**EDA et audit indépendant : Taoufik**

## Décisions du binôme

- Tâche : classification binaire combinée injection + jailbreak.
- Labels : `0` = bénin/normal ; `1` = malveillant (injection ou jailbreak).
- Dataset principal : `neuralchemy/Prompt-injection-dataset`.
- Configurations prévues : `core` pour la baseline classique de Taoufik, `full` pour DistilBERT d'Ayoub.
- Aucune fusion manuelle avec S-Labs, deepset, JailbreakBench ou HarmBench n'est prévue.

Le dépôt NeurAlchemy annonce que `core` contient des exemples originaux sans augmentation, tandis que `full` ajoute des exemples augmentés à l'entraînement. Il annonce également les mêmes exemples de validation et de test pour les deux configurations. Ayoub et Taoufik doivent le vérifier sur les données réellement chargées. Les détails de provenance des sources intégrées seront attribués à NeurAlchemy dans le rapport, et non présentés comme une collecte du binôme.

## A. Travail d'Ayoub — valider la source retenue

### Ce qu'il faut

- Accès à la carte Hugging Face et au dataset `neuralchemy/Prompt-injection-dataset` ;
- Python 3 et un accès Internet pour télécharger les fichiers ;
- le mapping binaire et les configurations convenus ci-dessus ;
- un fichier de notes de validation. Ne pas copier le dataset brut dans le dépôt Git.

### Étapes

1. Consulter la carte officielle et consigner l'identifiant exact, la révision disponible, la licence affichée, les configurations, le schéma et les sources amont déclarées.
2. Depuis la racine du dépôt, télécharger les deux configs : `python 01_exploration_eda/download_dataset.py`. Pour une seule config : ajouter `--config core` ou `--config full`.
3. Le script enregistre les fichiers Parquet sous `data_local/neuralchemy/<revision>/<config>/` et crée `download_manifest.json`. Il vérifie taille et empreinte SHA-256 ; `data_local/` est ignoré par Git.
4. Inspecter séparément `core` et `full`. Noter pour chaque split sa taille, ses colonnes et ses types ; comparer aux nombres annoncés et signaler toute différence.
5. Vérifier les valeurs réelles de `label` et quelques exemples par classe : `0` bénin, `1` malveillant.
6. Examiner `category`, `source`, `severity`, `group_id`, `augmented` et `tags`. Noter les catégories d'injection, de jailbreak et les exemples bénins.
7. Comparer validation et test des configs. Ayoub a déjà comparé via l'API les multisets de textes et labels ; Taoufik peut refaire le contrôle depuis les fichiers locaux.
8. Vérifier que `group_id` ne traverse pas train, validation et test. Dans `full`, vérifier si les variantes augmentées restent dans train.
9. Compléter `source_validation.md` avec les résultats locaux, les écarts et les contrôles restant à faire.
10. Transmettre à Taoufik la même révision, le dictionnaire, les tailles/splits et les contrôles à poursuivre. Il peut télécharger les mêmes fichiers en exécutant le script.

### Livrable d'Ayoub

`source_validation.md` : note courte et vérifiable décrivant la version/source, les configs, tailles, colonnes, mapping des labels, comparaison `core`/`full`, contrôle des groupes et questions ouvertes.

## B. Travail de Taoufik — EDA et audit avant entraînement

### Ce qu'il faut

- `source_validation.md` rempli par Ayoub ;
- les deux configurations `core` et `full` accessibles ;
- un emplacement pour `eda_report.md` et les figures.

### Étapes

1. Refaire les contrôles essentiels d'Ayoub de façon indépendante : splits, colonnes, tailles et labels.
2. Mesurer les effectifs et pourcentages de chaque label pour train, validation et test, séparément pour `core` et `full`.
3. Compter les exemples par `category`, `source`, `severity` et valeur de `augmented`, globalement et par split. Distinguer les catégories d'injection, jailbreak et benign selon les valeurs réellement observées.
4. Analyser les valeurs manquantes, textes vides, doublons exacts et longueurs de texte. Comparer les distributions par classe et par split.
5. Contrôler `group_id`, les recouvrements de texte/ID entre splits et le contenu augmenté de `full`. La déclaration de la carte sur l'absence de fuite est à vérifier, pas à reprendre comme un résultat du projet.
6. Examiner si les deux configs ont les mêmes exemples de validation/test. Si ce n'est pas le cas, documenter la différence et décider avec Ayoub comment rendre l'évaluation comparable.
7. Rédiger les résultats mesurés, figures, limites et décision de passage dans `eda_report.md`.

## Fichiers à produire dans ce dossier

| Fichier | Responsable | Contenu attendu | À versionner ? |
|---|---|---|---|
| `sources_inventory.md` | Ayoub | Source choisie, périmètre et configurations prévues. | Oui |
| `download_dataset.py` | Ayoub | Télécharge les Parquet `core`/`full` à la révision figée et vérifie leurs SHA-256. | Oui |
| `source_validation.md` | Ayoub | Révision/date, tailles et colonnes observées, labels, comparaison des configs et contrôle des groupes. | Oui ; pas de prompts bruts |
| `data_dictionary.md` | Ayoub + Taoufik | Définitions confirmées des champs et des catégories/labels utilisés. | Oui |
| `eda_report.md` | Taoufik | Tableaux, distributions, contrôles qualité/fuite, conclusions et décision de passage. | Oui |
| `figures/` | Taoufik | Graphiques lisibles sur labels, catégories, sources, longueurs et splits. | Oui si légers et dérivés |

Le dataset demeure sur Hugging Face. Ne pas versionner ses copies, ses caches ou ses textes bruts dans ce dépôt.

## Passage à la phase suivante

- [x] Configs `core`/`full`, colonnes, tailles et splits confirmés au chargement.
- [x] Mapping confirmé : `0` bénin, `1` malveillant.
- [x] Catégories et métadonnées nécessaires à l'analyse comprises.
- [x] Textes et labels de validation/test `core`/`full` comparés via l'API officielle ; multisets identiques.
- [x] `group_id` et variantes augmentées contrôlés ; les limites sont consignées.
- [x] Rapport EDA et décision de Taoufik remis à Ayoub.
- [x] Protocole et données retenus identiques pour le passage baseline/DistilBERT, sauf différence documentée.
