# Projet : détection de prompt injection et de jailbreak

**Groupe 7 — Ayoub El Kharraf et Mansouri Taoufik**  
**Date limite : 28 novembre 2026**

## À quoi sert ce dépôt ?

Ce dépôt est le **carnet de route du projet**. Il explique quoi faire, dans quel ordre, avec quelles données, quels contrôles effectuer et quels livrables laisser au collègue. Il contient un petit script pour sauvegarder localement les données de phase 1 ; les scripts d'entraînement seront créés pendant les phases concernées.

Le projet compare deux détecteurs binaires de prompts bénins et malveillants (prompt injection ou jailbreak) à partir de `neuralchemy/Prompt-injection-dataset`. Le binôme ne prévoit pas de fusionner manuellement d'autres datasets. La baseline utilise la configuration `core` et DistilBERT la configuration `full`, conformément au protocole initial.

- une baseline **TF-IDF + régression logistique** ;
- un modèle **DistilBERT fine-tuné**.

La carte annonce les mêmes validations et tests pour `core` et `full`, tandis que `full` ajoute des exemples augmentés à l'entraînement. Vérifier ces éléments sur les données réellement chargées avant la comparaison.

La comparaison porte sur la précision, le rappel, le F1-score et les matrices de confusion. Le rapport doit discuter les limites du dataset et rappeler qu'un classifieur ne garantit pas la sécurité d'un système LLM en production.

## Qui fait quoi ?

| Responsable | Travail | Dossiers à suivre |
|---|---|---|
| **Ayoub** | Validation de la source et des configurations, fine-tuning DistilBERT sur `full`, rapport final | `01_exploration_eda/` (validation de source), `03_distilbert_ayoub/`, `05_rapport_final_ayoub/` |
| **Taoufik** | EDA des configs, baseline TF-IDF + régression logistique sur `core`, tableau de bord comparatif | `01_exploration_eda/` (audit EDA), `02_baseline_taoufik/`, `04_dashboard_comparaison_taoufik/` |

## Par où commencer ?

1. Lire ce README pour comprendre le projet et son ordre de réalisation.
2. **Ayoub valide la source et les configs dans `01_exploration_eda/GUIDE_EDA.md`**, sans créer de corpus fusionné.
3. **Taoufik réalise ensuite l'EDA**. Ensemble, vous vérifiez labels, groupes et comparabilité des tests `core`/`full`.
4. Réaliser la baseline sur `core` et DistilBERT sur `full`. Vérifier que le jeu de test est commun avant comparaison.
5. Construire le tableau de bord, puis terminer le rapport avec les mesures réellement obtenues et leurs limites.

## Ordre du travail et passage de relais

| Phase | Dossier / guide | À la fin, on doit avoir… | Passage de relais |
|---|---|---|---|
| 1a. Valider la source | `01_exploration_eda/GUIDE_EDA.md` — Ayoub | Configs, schéma, labels et splits vérifiés | Ayoub transmet ses constats à Taoufik |
| 1b. Auditer les données | `01_exploration_eda/GUIDE_EDA.md` — Taoufik | EDA, contrôle des groupes/fuites et décision de passage | Ensemble, validation de la comparabilité `core`/`full` |
| 2. Établir la baseline | `02_baseline_taoufik/GUIDE_BASELINE.md` | Baseline sur `core`, paramètres et prédictions de test exportés | Taoufik transmet prédictions et identifiants de test |
| 3. Fine-tuner le transformer | `03_distilbert_ayoub/GUIDE_DISTILBERT.md` | Modèle sur `full`, paramètres et prédictions de test exportés | Ayoub transmet les prédictions alignables avec la baseline |
| 4. Comparer | `04_dashboard_comparaison_taoufik/GUIDE_DASHBOARD.md` | Métriques, matrices de confusion et tableau de bord fondés sur des tests comparables | Taoufik fournit les résultats consolidés à Ayoub |
| 5. Rédiger | `05_rapport_final_ayoub/GUIDE_RAPPORT.md` et `rapport_template.md` | Rapport complet, chiffres vérifiés, limites et conclusion | Ayoub vérifie que les résultats correspondent aux artefacts et décisions des phases précédentes |

## Ce qu'il faut préparer et consigner

- Un environnement Python et les dépendances listées dans `requirements.txt` ; PyTorch doit être installé dans une version adaptée au matériel disponible (CPU ou GPU).
- L'accès au dataset Hugging Face et, pour DistilBERT, au modèle pré-entraîné. Le premier téléchargement nécessite une connexion Internet.
- Les décisions communes : colonnes utilisées, correspondance entre labels d'origine et classes binaires, splits, stratégie liée à `group_id`, graine aléatoire et identifiant stable des exemples.
- Pour chaque expérience : versions des bibliothèques, paramètres, durée/matériel utile, métriques, date et emplacement des sorties.
- Des dossiers de sortie locaux pour modèles, caches, figures et exports. Ne pas déposer de données téléchargées, gros modèles ou caches dans Git sans nécessité.

## Règles communes pour un résultat fiable

1. Vérifier les schémas, labels et splits réellement chargés, même si la carte du dataset les décrit.
2. Garder le jeu de test à l'écart de l'entraînement et du choix des paramètres.
3. Si `group_id` existe et représente des exemples liés, un même groupe ne doit pas apparaître dans plusieurs partitions. Vérifier aussi les doublons et documenter les limites de ces contrôles.
4. Pour comparer les modèles, aligner leurs prédictions par identifiant d'exemple et confirmer que les labels réels concordent. Si les configurations ne donnent pas les mêmes exemples, le dire clairement et éviter une comparaison directe trompeuse.
5. Définir explicitement la classe positive (« malveillant ») et l'ordre des classes dans les matrices de confusion.
6. Ne jamais inventer de résultats : écrire « à mesurer » tant que les évaluations ne sont pas terminées.

## Contenu des dossiers

- `01_exploration_eda/` : validation de la source NeurAlchemy par Ayoub et audit EDA par Taoufik.
- `02_baseline_taoufik/` : guide de réalisation de la baseline classique.
- `03_distilbert_ayoub/` : guide de fine-tuning et d'export des prédictions.
- `04_dashboard_comparaison_taoufik/` : guide de comparaison et de visualisation.
- `05_rapport_final_ayoub/` : guide de rédaction et trame du rapport.

Chaque dossier contient son propre guide détaillé : le README donne la vue d'ensemble, tandis que le guide du dossier décrit le travail à effectuer à cette étape.
