# Dictionnaire des données — NeurAlchemy

**Source :** `neuralchemy/Prompt-injection-dataset`  
**Révision :** `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75`  
**Tâche du projet :** classification binaire injection + jailbreak.

## Cible et configurations

| Valeur | Signification projet | Confirmation |
|---:|---|---|
| `0` | Bénin / normal | Valeur observée dans les six splits et confirmée par les exemples/catégories bénignes |
| `1` | Malveillant : injection ou jailbreak | Valeur observée dans les six splits et confirmée par les catégories d’attaque |

| Configuration | Modèle associé | Description du fournisseur | Splits et tailles reçus par l’API |
|---|---|---|---|
| `core` | Baseline TF-IDF + Logistic Regression | Entraînement sans augmentation, exemples originaux | train 4 391, validation 941, test 942 (confirmé localement) |
| `full` | DistilBERT | Entraînement avec exemples augmentés | train 14 036, validation 941, test 942 (confirmé localement) |

Les tailles et splits ci-dessus sont vérifiés via l’API Hugging Face et les fichiers locaux. Les textes et labels des exemples de validation/test sont identiques entre les deux configurations ; l’alignement final des prédictions devra toutefois utiliser un identifiant stable plutôt que l’ordre des lignes.

## Colonnes

| Colonne | Type API / carte | Utilisation dans le projet | Contrôle restant |
|---|---|---|---|
| `text` | string | Texte d'entrée donné au classifieur | Aucun texte vide observé ; analyse des longueurs à détailler par l’EDA |
| `label` | int32 | Cible binaire (`0` bénin, `1` malveillant) | Valeurs observées uniquement : `0` et `1` ; distributions à détailler par l’EDA |
| `category` | string | Sous-type d'attaque ou catégorie bénigne | Effectifs contrôlés ; conserver pour analyse, pas comme cible du classifieur binaire |
| `source` | string | Provenance déclarée par NeurAlchemy | Valeurs et distributions à détailler par l’EDA ; rechercher un éventuel raccourci de source |
| `severity` | string | Sévérité associée, potentiellement vide | Aucune valeur manquante observée ; distribution à détailler ; ne pas utiliser comme cible |
| `group_id` | string | Groupe d'exemples apparentés/original-augmentations | Aucun groupe ne traverse train, validation et test |
| `augmented` | bool | Indique si un exemple est augmenté | `full` train : 4 391 `false` et 9 645 `true` ; validation/test : uniquement `false` |
| `tags` | liste de chaînes | Métadonnées descriptives/recherche | Examiner les valeurs ; ne pas les utiliser comme entrée par défaut |

Les noms/types de colonnes ont été confirmés dans les six fichiers locaux. Les champs contrôlés ne contiennent aucune valeur manquante. Les longueurs, sources et sévérités doivent encore être détaillées dans le rapport EDA.

## Catégories et analyse

La carte présente notamment `direct_injection`, `indirect_injection`, `jailbreak`, `encoding_obfuscation`, `many_shot`, `crescendo`, `prompt_leaking` et `benign`. La liste finale et les effectifs seront confirmés par l'EDA de Taoufik. Pour une analyse secondaire, les catégories pourront être regroupées en grandes familles, mais le regroupement devra être défini explicitement et ne remplacera pas `label`.

## Règles d'utilisation

1. Utiliser `text` comme entrée et `label` comme cible.
2. Ne pas fournir `category`, `source`, `severity`, `group_id`, `augmented` ou `tags` au modèle comme caractéristiques sans protocole séparé ; ces champs servent à tracer et analyser les données.
3. Garder `group_id` et `augmented` dans les métadonnées pour contrôler les fuites et les variantes.
4. Garder les splits officiels : `core` pour la baseline, `full` pour DistilBERT.
5. Ne pas fusionner les configs : elles ont des ensembles d'entraînement différents et des tests annoncés communs.
