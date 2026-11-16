# Projet : détection de prompt injection et de jailbreak

**Groupe 7 — Ayoub El Kharraf et Mansouri Taoufik**  
**Date limite : 28 novembre 2026**

## À quoi sert ce dépôt ?

Ce dépôt est le **carnet de route du projet**. Il explique quoi faire, dans quel ordre, avec quelles données, quels contrôles effectuer et quels livrables laisser au collègue. Il ne contient pas de scripts Python : le code sera créé au moment de réaliser chaque étape, dans les dossiers correspondants.

Le projet consiste à étudier et comparer deux détecteurs de prompts bénins ou malveillants à partir de `neuralchemy/Prompt-injection-dataset` :

- une baseline **TF-IDF + régression logistique**, avec la configuration `core` ;
- un modèle **DistilBERT fine-tuné**, avec la configuration `full`.

La comparaison porte sur la précision, le rappel, le F1-score et les matrices de confusion. Le rapport doit discuter les limites du dataset et rappeler qu'un classifieur ne garantit pas la sécurité d'un système LLM en production.

## Qui fait quoi ?

| Responsable | Travail | Dossiers à suivre |
|---|---|---|
| **Taoufik** | Exploration des données, baseline TF-IDF + régression logistique, tableau de bord comparatif | `01_exploration_eda/`, `02_baseline_taoufik/`, `04_dashboard_comparaison_taoufik/` |
| **Ayoub** | Fine-tuning de DistilBERT, rédaction et analyse critique du rapport final | `03_distilbert_ayoub/`, `05_rapport_final_ayoub/` |

## Par où commencer ?

1. Lire ce README pour comprendre le projet et son ordre de réalisation.
2. **Taoufik commence par `01_exploration_eda/GUIDE_EDA.md`**. Ayoub peut lire les guides de son périmètre, mais doit reprendre les décisions communes sur les labels, groupes et données après l'EDA.
3. Avant d'entraîner les modèles, se mettre d'accord sur les noms des colonnes, le mapping bénin/malveillant, les règles de séparation et la façon d'identifier les exemples. Consigner ces décisions dans les résultats de l'EDA.
4. Réaliser la baseline et DistilBERT selon leurs guides respectifs. Chaque responsable transmet les prédictions du même jeu de test, ou explique précisément pourquoi les jeux de test diffèrent.
5. Construire le tableau de bord, puis terminer le rapport avec les mesures réellement obtenues et leurs limites.

## Ordre du travail et passage de relais

| Phase | Dossier / guide | À la fin, on doit avoir… | Passage de relais |
|---|---|---|---|
| 1. Comprendre les données | `01_exploration_eda/GUIDE_EDA.md` | Schéma vérifié, distribution des classes, analyse des groupes et décision documentée sur le split | Taoufik communique à Ayoub les colonnes, labels, splits et contrôles anti-fuite retenus |
| 2. Établir la baseline | `02_baseline_taoufik/GUIDE_BASELINE.md` | Pipeline entraîné, paramètres consignés et prédictions du test exportées | Taoufik transmet les prédictions et l'identifiant de chaque exemple |
| 3. Fine-tuner le transformer | `03_distilbert_ayoub/GUIDE_DISTILBERT.md` | Modèle et tokenizer sauvegardés, paramètres consignés et prédictions du test exportées | Ayoub transmet les prédictions dans un format alignable avec la baseline |
| 4. Comparer | `04_dashboard_comparaison_taoufik/GUIDE_DASHBOARD.md` | Métriques, matrices de confusion et tableau de bord fondés sur des tests comparables | Taoufik fournit les résultats consolidés à Ayoub |
| 5. Rédiger | `05_rapport_final_ayoub/GUIDE_RAPPORT.md` et `rapport_template.md` | Rapport complet, chiffres vérifiés, limites et conclusion | Ayoub vérifie que les résultats correspondent aux artefacts et décisions des phases précédentes |

## Ce qu'il faut préparer et consigner

- Un environnement Python et les dépendances listées dans `requirements.txt` ; PyTorch doit être installé dans une version adaptée au matériel disponible (CPU ou GPU).
- L'accès au dataset Hugging Face et, pour DistilBERT, au modèle pré-entraîné. Le premier téléchargement nécessite une connexion Internet.
- Les décisions communes : colonnes utilisées, correspondance entre labels d'origine et classes binaires, splits, stratégie liée à `group_id`, graine aléatoire et identifiant stable des exemples.
- Pour chaque expérience : versions des bibliothèques, paramètres, durée/matériel utile, métriques, date et emplacement des sorties.
- Des dossiers de sortie locaux pour modèles, caches, figures et exports. Ne pas déposer de données téléchargées, gros modèles ou caches dans Git sans nécessité.

## Règles communes pour un résultat fiable

1. Vérifier les données réellement chargées : les colonnes et les splits peuvent différer selon `core` et `full`.
2. Garder le jeu de test à l'écart de l'entraînement et du choix des paramètres.
3. Si `group_id` existe et représente des exemples liés, un même groupe ne doit pas apparaître dans plusieurs partitions. Vérifier aussi les doublons et documenter les limites de ces contrôles.
4. Pour comparer les modèles, aligner leurs prédictions par identifiant d'exemple et confirmer que les labels réels concordent. Si les configurations ne donnent pas les mêmes exemples, le dire clairement et éviter une comparaison directe trompeuse.
5. Définir explicitement la classe positive (« malveillant ») et l'ordre des classes dans les matrices de confusion.
6. Ne jamais inventer de résultats : écrire « à mesurer » tant que les évaluations ne sont pas terminées.

## Contenu des dossiers

- `01_exploration_eda/` : guide pour comprendre les données et décider du protocole.
- `02_baseline_taoufik/` : guide de réalisation de la baseline classique.
- `03_distilbert_ayoub/` : guide de fine-tuning et d'export des prédictions.
- `04_dashboard_comparaison_taoufik/` : guide de comparaison et de visualisation.
- `05_rapport_final_ayoub/` : guide de rédaction et trame du rapport.

Chaque dossier contient son propre guide détaillé : le README donne la vue d'ensemble, tandis que le guide du dossier décrit le travail à effectuer à cette étape.
