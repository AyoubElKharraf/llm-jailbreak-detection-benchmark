# Validation de la source NeurAlchemy — Ayoub

**Source :** [`neuralchemy/Prompt-injection-dataset`](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset)  
**Révision vérifiée via l’API Hugging Face :** `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75`  
**Dernière mise à jour indiquée par l’API :** 23 avril 2026  
**Statut :** validation de la source, des splits, du schéma, des labels, des groupes et de la comparabilité `core`/`full` effectuée. L’EDA détaillée et ses figures restent à produire par Taoufik.

## 1. Résultat de la vérification des splits

La route officielle Hugging Face `datasets-server` confirme six splits disponibles : `train`, `validation` et `test` pour chacune des configurations `core` et `full`. Aucun split n'est indiqué en attente ou en échec.

| Configuration | Split | Nombre de lignes confirmé par l’API | Taille Parquet indiquée |
|---|---|---:|---:|
| `core` | train | 4 391 | 387 456 octets |
| `core` | validation | 941 | 92 943 octets |
| `core` | test | 942 | 94 145 octets |
| `full` | train | 14 036 | 1 409 838 octets |
| `full` | validation | 941 | 92 943 octets |
| `full` | test | 942 | 94 145 octets |

Les textes et labels de validation/test ont été récupérés par pages via l’API `rows` puis comparés comme multisets (l’ordre n'intervient donc pas). Les deux configs contiennent les mêmes textes et labels pour chaque split. C'est suffisant pour confirmer que les modèles peuvent être évalués sur les mêmes exemples, sous réserve que la préparation des textes et le mapping des labels restent identiques.

Empreintes SHA-256 agrégées des lignes `text + label` (elles permettent de refaire le contrôle sans sauvegarder ni publier les prompts) :

| Split | Lignes par config | Empreinte `core` | Empreinte `full` | Résultat |
|---|---:|---|---|---|
| validation | 941 | `60f0719e5e0ef244556052f01ef517163a957e3101a03b27870f657f0c9cac09` | `60f0719e5e0ef244556052f01ef517163a957e3101a03b27870f657f0c9cac09` | Identiques |
| test | 942 | `5fc12509da45faac594a3f5c6fa90671c7e1a688525c9ae787d8ba82318572bb` | `5fc12509da45faac594a3f5c6fa90671c7e1a688525c9ae787d8ba82318572bb` | Identiques |

## 2. Schéma et tâche annoncés

L’API de prévisualisation de la configuration `core` confirme les colonnes suivantes :

| Colonne | Type observé par l’API | Interprétation à confirmer |
|---|---|---|
| `text` | string | Prompt à classifier |
| `label` | int32 | Carte : `0` bénin, `1` malveillant |
| `category` | string | Catégorie d’attaque ou `benign` |
| `source` | string | Provenance déclarée par le dataset |
| `severity` | string | Niveau de sévérité, parfois vide selon les exemples |
| `group_id` | string | Identifiant de groupe pour relier des variantes |
| `augmented` | bool | Indique si la ligne est augmentée |
| `tags` | liste | Métadonnées de recherche/catégorisation |

La carte décrit `core` comme le train original sans augmentation et `full` comme un train augmenté ; les deux configs sont prévues respectivement pour ML classique et transformers. La classe cible retenue par le binôme est binaire : bénin versus malveillant (injection ou jailbreak). La carte indique une provenance intégrant notamment HackAPrompt, WildGuard/JudgeComparison et HarmBench ; ces attributions sont celles du fournisseur.

## 3. Contrôles qui restent à effectuer sur le contenu

- [x] Charger les fichiers Parquet avec un lecteur compatible dans l’environnement local.
- [x] Confirmer que `full` expose le même schéma que `core` pour chaque split.
- [x] Parcourir toutes les valeurs de `label` et confirmer leur sémantique ; aucune valeur manquante.
- [x] Comparer textes et labels validation/test de `core` et `full` via l’API : multisets identiques.
- [x] Vérifier `group_id` sur les splits : aucun groupe commun entre deux partitions.
- [x] Vérifier le lien entre exemples originaux et augmentés dans `full` : les 4 391 lignes originales sont complétées par 9 645 lignes augmentées dans le train ; validation/test ne contiennent aucune ligne augmentée.
- [ ] Produire l’EDA détaillée, les figures et l’analyse interprétative des catégories, sources, sévérités et longueurs (travail de Taoufik).

La carte affirme que le split est fait par groupe et annonce zéro fuite selon ses contrôles. Taoufik doit refaire le contrôle utile pour notre protocole et distinguer les résultats de notre audit de ceux rapportés par le fournisseur.

## 4. Résultats de l’audit local

Les Parquet ont finalement été inspectés avec un lecteur DuckDB indépendant de NumPy/Pandas, après le blocage des extensions natives de l’environnement `datasets`.

Le 16 novembre 2026, `download_dataset.py --config both` a été relancé depuis la racine du dépôt. Les six fichiers locaux (`core`/`full`, `train`/`validation`/`test`) existent et leurs tailles et empreintes SHA-256 correspondent à la révision attendue. Pandas et PyArrow restent indisponibles dans l’environnement initial car leurs extensions natives sont bloquées par Windows ; l’audit de contenu a donc été réalisé avec DuckDB.

L’audit DuckDB a ensuite confirmé les éléments suivants :

| Configuration / split | Lignes | Label 0 | Label 1 | Texte vide | Doublons exacts de texte | `augmented` |
|---|---:|---:|---:|---:|---:|---|
| `core` / train | 4 391 | 1 741 | 2 650 | 0 | 0 | 4 391 `false` |
| `core` / validation | 941 | 407 | 534 | 0 | 0 | 941 `false` |
| `core` / test | 942 | 390 | 552 | 0 | 0 | 942 `false` |
| `full` / train | 14 036 | 5 208 | 8 828 | 0 | 102 lignes répétées | 4 391 `false`, 9 645 `true` |
| `full` / validation | 941 | 407 | 534 | 0 | 0 | 941 `false` |
| `full` / test | 942 | 390 | 552 | 0 | 0 | 942 `false` |

Les six splits ont un schéma identique entre configurations, aucune valeur manquante dans les champs contrôlés et aucun recouvrement de `group_id` entre train, validation et test. Les textes et labels des validations/tests `core` et `full` ont aussi le même multiensemble.

## 5. Passage de relais à Taoufik

### Travail réalisé par Ayoub

- Source, révision, licence déclarée et périmètre validés.
- Téléchargement reproductible vérifié par taille et SHA-256.
- Configurations `core` et `full`, schéma et tailles confirmés localement.
- Mapping confirmé : `0` bénin, `1` malveillant.
- Absence de textes vides et de valeurs manquantes contrôlées.
- Absence de recouvrement de `group_id` entre les partitions contrôlée.
- Augmentations limitées au train `full` et comparabilité validation/test confirmée.

### Travail restant pour Taoufik

- Produire le rapport EDA et les figures.
- Détailler les distributions par `category`, `source`, `severity` et `augmented`.
- Analyser les longueurs de texte et le déséquilibre des classes.
- Examiner les 102 lignes répétées de texte dans le train `full` et préciser leur relation avec les variantes augmentées.
- Refaire les contrôles essentiels indépendamment et décider le « go » pour les entraînements.
- Transmettre les conclusions EDA et les limites à Ayoub avant la baseline et DistilBERT.

Ne pas ajouter de copies du dataset ou de prompts bruts au dépôt Git.
