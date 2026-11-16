# Inventaire et validation de la source — Phase 1

**Responsable de la vérification de la source : Ayoub**  
**Dataset retenu :** [`neuralchemy/Prompt-injection-dataset`](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset)  
**Statut :** source unique retenue ; aucun dataset supplémentaire ne sera fusionné.
**Révision vérifiée via l'API Hugging Face :** `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75`.

## 1. Périmètre validé

Le projet réalise une classification binaire combinée :

- `0` = bénin / normal ;
- `1` = malveillant, incluant prompt injection et jailbreak.

Les métadonnées telles que `category`, `source`, `severity`, `group_id`, `augmented` et `tags` seront conservées pour l'analyse. Les modèles apprennent la cible binaire `label` ; les catégories serviront à examiner les résultats par type d'attaque.

**Aucune fusion manuelle avec d'autres datasets n'est prévue pour le corpus principal.** `JailbreakBench`, HarmBench, deepset ou S-Labs ne sont pas à télécharger/ajouter à ce stade. Une éventuelle évaluation externe avec ces sources devra faire l'objet d'une décision ultérieure et d'un jeu distinct.

## 2. Configurations documentées par la carte Hugging Face

Les nombres ci-dessous sont ceux affichés dans la carte du dataset à la date de vérification ; ils doivent être confirmés lors du chargement réel.

| Configuration | Usage annoncé | Train annoncé | Validation annoncée | Test annoncé | Remarque |
|---|---|---:|---:|---:|---|
| `core` | ML classique, notamment Logistic Regression | 4 391 | 941 | 942 | Train décrit comme exemples originaux sans augmentation. |
| `full` | Transformers, dont DistilBERT | 14 036 | 941 | 942 | Train décrit comme augmenté ; validation/test annoncés identiques à `core`. |

La carte attribue à `label` les valeurs `1` malveillant et `0` bénin. Elle indique également un partage par `group_id` et l'absence de variantes augmentées en validation/test. Ces indications sont celles du fournisseur : Taoufik doit les vérifier dans l'EDA, et le rapport doit présenter ce contrôle comme une vérification de notre projet plutôt qu'une simple répétition de la carte.

## 3. Métadonnées du dataset à enregistrer

| Élément | Valeur préliminaire | À confirmer par Ayoub |
|---|---|---|
| Identifiant | `neuralchemy/Prompt-injection-dataset` | Oui, au chargement |
| Configurations | `core`, `full` | Oui |
| Colonnes visibles | `text`, `label`, `category`, `source`, `severity`, `group_id`, `augmented`, `tags` | Oui pour chaque configuration/split |
| Mapping de label annoncé | `0` bénin, `1` malveillant | Vérifier les valeurs réelles et exemples |
| Tâche | Injection + jailbreak, classification binaire | Décision du binôme validée |
| Licence annoncée | Apache-2.0 pour le dataset, avec provenance des sources détaillée par la carte | Vérifier les conditions et attributions liées aux sources incorporées avant redistribution |
| Révision/date précise | `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75` (mise à jour API : 2026-04-23) | Confirmée via l'API |
| Tailles effectives et distribution | À mesurer | Oui |

## 4. Travail d'Ayoub dans cette phase

Ton travail n'est pas de fabriquer un corpus en fusionnant plusieurs sources. Il consiste à **valider la source retenue et préparer son usage reproductible** :

1. Vérifier le dépôt et sa carte Hugging Face ; noter la date de consultation, l'identifiant, la licence et les configurations prévues.
2. Charger séparément `core` et `full` lors de la mise en œuvre, puis noter les splits, tailles, colonnes et types réellement obtenus.
3. Vérifier dans les exemples que `text` est bien le texte à classifier et que `label` suit le mapping bénin/malveillant annoncé.
4. Comparer les identifiants ou contenus des partitions validation/test de `core` et `full`. Ayoub a vérifié via l'API les multisets de textes et labels ; ils sont identiques (voir `source_validation.md`).
5. Vérifier que les groupes et augmentations sont cohérents : les variantes d'un même groupe ne doivent pas traverser les partitions. Noter les contrôles que Taoufik devra refaire dans l'EDA.
6. Garder la structure et les splits officiels ; ne pas réunir train, validation et test, et ne pas créer un split aléatoire indépendant sans décision commune.
7. Transmettre à Taoufik les informations confirmées et les questions restantes. Il réalise ensuite l'EDA détaillée des labels, catégories, longueurs, sources et groupes.

## 5. Sources supplémentaires écartées du corpus principal

| Source | Décision actuelle |
|---|---|
| `JailbreakBench` | Non ajoutée : le dataset de NeurAlchemy contient déjà des exemples de jailbreak selon sa carte. Éventuel benchmark externe séparé, à décider plus tard. |
| HarmBench | Non ajouté : le dataset de NeurAlchemy indique déjà incorporer des comportements HarmBench et leurs contreparties bénignes. Éviter de recompter des exemples ; une évaluation externe demanderait une vérification d'overlap. |
| `deepset/prompt-injections` | Non ajouté : source distincte mais redondance éventuelle à contrôler ; aucune fusion manuelle nécessaire pour le corpus retenu. |
| « Prompt Injection Detection Dataset » / S-Labs | Non ajouté : NeurAlchemy est le dépôt précis choisi par le binôme. |

La carte de NeurAlchemy cite HackAPrompt, WildGuard/JudgeComparison et HarmBench parmi ses sources. Garder ces informations comme provenance déclarée par le fournisseur ; ne pas présenter l'ensemble comme un dataset que le binôme a lui-même collecté ou annoté.

## 6. Fichiers de phase 1

| Fichier | Responsable | Contenu |
|---|---|---|
| `sources_inventory.md` | Ayoub | Ce document : source choisie, périmètre, configurations et vérifications restantes. |
| `data_dictionary.md` | Ayoub + Taoufik | Définitions des colonnes, classes et catégories après inspection réelle. |
| `source_validation.md` | Ayoub | Date/révision, versions d'outils, tailles/splits réellement chargés, contrôle des configs `core`/`full` et conclusions transmises à Taoufik. |
| `eda_report.md` | Taoufik | Distributions, analyses, figures et contrôle indépendant de la qualité/fuite. |

Le dépôt de données demeure sur Hugging Face ; ne pas ajouter de copie du corpus ni de cache volumineux au dépôt Git. Les fichiers de validation doivent contenir les métadonnées et résultats de contrôle, pas les prompts bruts.

## 7. Suivi

- [x] Tâche combinée injection + jailbreak validée.
- [x] Source de référence NeurAlchemy confirmée.
- [x] Décision de ne pas fusionner manuellement d'autres datasets.
- [x] Les six splits et leurs tailles vérifiés via l'API Hugging Face.
- [ ] Colonnes/labels et groupes entièrement vérifiés par inspection locale.
- [x] Textes et labels des validations/tests `core` et `full` comparés via l'API : multisets identiques.
- [ ] Contrôle des groupes/augmentations documenté par Ayoub et vérifié par Taoufik.
- [ ] Passage de relais à Taoufik pour l'EDA.
