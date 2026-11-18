# Fiche d'Expérience — DistilBERT (Phase 3)

**Responsable :** Ayoub El Kharraf  
**Date :** 18 novembre 2026  
**Modèle de départ :** `distilbert-base-uncased` (Hugging Face)  
**Tâche :** Classification binaire (Bénin = `0`, Malveillant = `1`)

---

## 1. Données Utilisées
- **Dataset source :** `neuralchemy/Prompt-injection-dataset` (configuration `full`)
- **Fichiers d'entraînement :** `data_processed/full/train.parquet` (13 934 exemples après suppression des 102 doublons exacts)
- **Validation :** `data_processed/full/validation.parquet` (941 exemples)
- **Test :** `data_processed/full/test.parquet` (942 exemples)

---

## 2. Configuration Technique & Hyperparamètres
- **Longueur maximale (`max_length`) :** 512 tokens (avec padding et troncature).
- **Architecture :** DistilBERT avec tête de classification binaire (`num_labels=2`).
- **Époques :** 3
- **Batch size :** 16
- **Taux d'apprentissage (`learning_rate`) :** `2e-5` (optimiseur AdamW, weight decay = 0.01).
- **Stratégie de sélection :** Évaluation à chaque fin d'époque, conservation du meilleur modèle selon le **F1-score** sur le jeu de validation.
- **Graine aléatoire (`seed`) :** 42.

---

## 3. Résultats & Métriques de Test (À remplir lors de l'exécution)

*Note : Les métriques seront automatiquement générées et exportées par `train_distilbert.py` dans `distilbert_metrics.json`.*

| Métrique | Score Test |
|---|---|
| **Accuracy** | *(à mesurer à l'exécution)* |
| **Precision (Malveillant)** | *(à mesurer à l'exécution)* |
| **Recall (Malveillant)** | *(à mesurer à l'exécution)* |
| **F1-Score (Malveillant)** | *(à mesurer à l'exécution)* |
| **Macro F1** | *(à mesurer à l'exécution)* |
| **ROC-AUC** | *(à mesurer à l'exécution)* |

### Matrice de Confusion
- **Vrais Négatifs (Bénins corrects) :** *(à mesurer)*
- **Faux Positifs (Bénins classés malveillants) :** *(à mesurer)*
- **Faux Négatifs (Attaques manquées) :** *(à mesurer)*
- **Vrais Positifs (Attaques détectées) :** *(à mesurer)*

---

## 4. Analyse et Discussion des Erreurs
*(À compléter après inspection des prédictions)*
- **Taux de troncature observé :** %(mesuré automatiquement sur le dataset)
- **Analyse des faux négatifs critiques :** Quelles familles d'attaques (jailbreak complexe, multi-shot, encoding) échappent au filtre ?

