# Projet : détection de prompt injection et de jailbreak

**Groupe 7 — Ayoub El Kharraf et Mansouri Taoufik**  
**Date limite : 28 novembre 2026**

## À quoi sert ce dépôt ?

Ce dépôt est le **carnet de route du projet**. Il explique quoi faire, dans quel ordre, avec quelles données, quels contrôles effectuer et quels livrables laisser au collègue. Il ne contient pas de scripts Python : le code sera créé au moment de réaliser chaque étape, dans les dossiers correspondants.

Le projet consiste à étudier et comparer deux détecteurs de prompts bénins ou malveillants. La proposition actuelle est de construire un corpus multi-sources, en étudiant notamment `JailbreakBench`, `deepset/prompt-injections`, HarmBench et un dataset de détection d'injection dont l'identifiant exact reste à confirmer. `neuralchemy/Prompt-injection-dataset` peut faire partie de l'inventaire. Les guides doivent aboutir à une définition de tâche commune avant de fusionner les exemples.

- une baseline **TF-IDF + régression logistique** ;
- un modèle **DistilBERT fine-tuné**.

Les deux modèles devraient utiliser le même corpus harmonisé et le même protocole de split pour permettre une comparaison directe. Les configurations `core`/`full` de neuralchemy ne sont donc plus automatiquement les deux jeux d'entraînement : si le binôme souhaite conserver cette contrainte initiale, il faut la concilier explicitement avec le corpus combiné et documenter tout écart.

La comparaison porte sur la précision, le rappel, le F1-score et les matrices de confusion. Le rapport doit discuter les limites du dataset et rappeler qu'un classifieur ne garantit pas la sécurité d'un système LLM en production.

## Qui fait quoi ?

| Responsable | Travail | Dossiers à suivre |
|---|---|---|
| **Ayoub** | Préparation et harmonisation du corpus multi-sources, fine-tuning de DistilBERT, rédaction et analyse critique du rapport final | `01_exploration_eda/` (collecte/harmonisation), `03_distilbert_ayoub/`, `05_rapport_final_ayoub/` |
| **Taoufik** | Audit EDA du corpus combiné, baseline TF-IDF + régression logistique, tableau de bord comparatif | `01_exploration_eda/` (audit EDA), `02_baseline_taoufik/`, `04_dashboard_comparaison_taoufik/` |

## Par où commencer ?

1. Lire ce README pour comprendre le projet et son ordre de réalisation.
2. **Ayoub commence par la partie collecte/harmonisation de `01_exploration_eda/GUIDE_EDA.md`**, puis transmet à Taoufik un corpus traçable et son manifeste.
3. **Taoufik réalise ensuite l'audit EDA dans le même guide**. Ayoub et Taoufik valident ensemble la définition de la tâche, les labels, groupes, split et identifiant des exemples avant l'entraînement.
4. Réaliser baseline et DistilBERT selon leurs guides respectifs sur le corpus et split convenus. Chaque responsable transmet les prédictions du même jeu de test.
5. Construire le tableau de bord, puis terminer le rapport avec les mesures réellement obtenues et leurs limites.

## Ordre du travail et passage de relais

| Phase | Dossier / guide | À la fin, on doit avoir… | Passage de relais |
|---|---|---|---|
| 1a. Construire le corpus | `01_exploration_eda/GUIDE_EDA.md` — Ayoub | Inventaire des sources, corpus harmonisé, provenance, mapping des labels et manifeste de construction | Ayoub transmet à Taoufik le corpus et les règles utilisées |
| 1b. Auditer le corpus | `01_exploration_eda/GUIDE_EDA.md` — Taoufik | Distributions, contrôle des groupes/fuites, cohérence des labels et décision de split | Les deux valident ensemble la définition de la tâche et le protocole commun |
| 2. Établir la baseline | `02_baseline_taoufik/GUIDE_BASELINE.md` | Baseline entraînée sur le corpus validé, paramètres consignés et prédictions du test exportées | Taoufik transmet les prédictions et l'identifiant de chaque exemple |
| 3. Fine-tuner le transformer | `03_distilbert_ayoub/GUIDE_DISTILBERT.md` | Modèle et tokenizer sauvegardés, paramètres consignés et prédictions du même test exportées | Ayoub transmet les prédictions alignables avec la baseline |
| 4. Comparer | `04_dashboard_comparaison_taoufik/GUIDE_DASHBOARD.md` | Métriques, matrices de confusion et tableau de bord fondés sur des tests comparables | Taoufik fournit les résultats consolidés à Ayoub |
| 5. Rédiger | `05_rapport_final_ayoub/GUIDE_RAPPORT.md` et `rapport_template.md` | Rapport complet, chiffres vérifiés, limites et conclusion | Ayoub vérifie que les résultats correspondent aux artefacts et décisions des phases précédentes |

## Ce qu'il faut préparer et consigner

- Un environnement Python et les dépendances listées dans `requirements.txt` ; PyTorch doit être installé dans une version adaptée au matériel disponible (CPU ou GPU).
- L'accès au dataset Hugging Face et, pour DistilBERT, au modèle pré-entraîné. Le premier téléchargement nécessite une connexion Internet.
- Les décisions communes : colonnes utilisées, correspondance entre labels d'origine et classes binaires, splits, stratégie liée à `group_id`, graine aléatoire et identifiant stable des exemples.
- Pour chaque expérience : versions des bibliothèques, paramètres, durée/matériel utile, métriques, date et emplacement des sorties.
- Des dossiers de sortie locaux pour modèles, caches, figures et exports. Ne pas déposer de données téléchargées, gros modèles ou caches dans Git sans nécessité.

## Règles communes pour un résultat fiable

1. Vérifier les données réellement chargées : les schémas, labels et splits peuvent différer d'une source à l'autre. Si les configurations `core`/`full` de neuralchemy sont conservées, noter où elles interviennent.
2. Garder le jeu de test à l'écart de l'entraînement et du choix des paramètres.
3. Si `group_id` existe et représente des exemples liés, un même groupe ne doit pas apparaître dans plusieurs partitions. Vérifier aussi les doublons et documenter les limites de ces contrôles.
4. Pour comparer les modèles, aligner leurs prédictions par identifiant d'exemple et confirmer que les labels réels concordent. Si les configurations ne donnent pas les mêmes exemples, le dire clairement et éviter une comparaison directe trompeuse.
5. Définir explicitement la classe positive (« malveillant ») et l'ordre des classes dans les matrices de confusion.
6. Ne jamais inventer de résultats : écrire « à mesurer » tant que les évaluations ne sont pas terminées.

## Contenu des dossiers

- `01_exploration_eda/` : guide commun de construction du corpus multi-sources (Ayoub) et d'audit EDA (Taoufik).
- `02_baseline_taoufik/` : guide de réalisation de la baseline classique.
- `03_distilbert_ayoub/` : guide de fine-tuning et d'export des prédictions.
- `04_dashboard_comparaison_taoufik/` : guide de comparaison et de visualisation.
- `05_rapport_final_ayoub/` : guide de rédaction et trame du rapport.

Chaque dossier contient son propre guide détaillé : le README donne la vue d'ensemble, tandis que le guide du dossier décrit le travail à effectuer à cette étape.
