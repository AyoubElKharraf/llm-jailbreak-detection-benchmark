# Fiche d'Expérience — DistilBERT (Phase 3)

**Responsable :** Ayoub El Kharraf  
**Date :** 18 novembre 2026  
**Modèle de départ :** `distilbert-base-uncased` (Hugging Face)  
**Tâche :** Classification binaire (Bénin = `0`, Malveillant = `1`)  
**Environnement d'entraînement :** Google Colab (GPU NVIDIA T4)  
**Notebook d'exécution :** `03_distilbert_ayoub/phase03_distilbert_colab_training.ipynb`

---

## 1. Données Utilisées
- **Dataset source :** `neuralchemy/Prompt-injection-dataset` (configuration `full`)
- **Révision :** `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75`
- **Fichiers d'entraînement :** 13 934 exemples nets (après suppression des 102 doublons exacts identifiés en Phase 1)
- **Validation :** 941 exemples
- **Test :** 942 exemples (avec identifiant stable `test_0000` à `test_0941`)

---

## 2. Configuration Technique & Hyperparamètres
- **Longueur maximale (`max_length`) :** 512 tokens (avec padding dynamique et troncature).
- **Architecture :** DistilBERT avec tête de classification binaire (`num_labels=2`).
- **Époques :** 3
- **Batch size :** 16 (train) / 32 (eval)
- **Taux d'apprentissage (`learning_rate`) :** `2e-5` (optimiseur AdamW, weight decay = 0.01).
- **Stratégie de sélection :** Évaluation à chaque fin d'époque, conservation du meilleur modèle selon le **F1-score** sur le jeu de validation (`load_best_model_at_end=True`).
- **Graine aléatoire (`seed`) :** 42.
- **Temps d'entraînement effectif :** 16,8 minutes sur GPU T4.

---

## 3. Résultats & Métriques de Test Réelles

Évaluation effectuée **une seule fois sur les 942 exemples du jeu de test officiel** :

| Métrique | Score Test Obtenu |
|---|---|
| **Accuracy** | **96,28 %** (0.9628) |
| **Precision (Malveillant)** | **96,58 %** (0.9658) |
| **Recall (Malveillant)** | **97,10 %** (0.9710) |
| **F1-Score (Malveillant)** | **96,84 %** (0.9684) |
| **Macro F1** | **96,17 %** (0.9617) |
| **ROC-AUC** | **99,55 %** (0.9955) |

### Matrice de Confusion (sur 942 exemples de test)

| | Prédit Bénin (0) | Prédit Malveillant (1) | Total Réel |
|---|---:|---:|---:|
| **Réel Bénin (0)** | **371** (VN) | **19** (FP) | 390 |
| **Réel Malveillant (1)** | **16** (FN) | **536** (VP) | 552 |
| **Total Prédit** | 387 | 555 | **942** |

*Figure sauvegardée dans : `03_distilbert_ayoub/distilbert_confusion_matrix.png`.*

---

## 4. Analyse et Discussion des Résultats

1. **Excellente performance globale :**
   - DistilBERT atteint un **F1-score de 96,84 %** et un **ROC-AUC exceptionnel de 99,55 %**, montrant une capacité de discrimination très fine entre requêtes bénignes et tentatives d'injection/jailbreak.
2. **Détection des attaques (Rappel) :**
   - Sur les 552 attaques présentes dans le jeu de test, **536 ont été correctement interceptées** (Rappel de 97,10 %).
   - Seules **16 attaques (faux négatifs)** ont échappé au modèle (2,9 % d'évasion).
3. **Faux Positifs (Usabilité) :**
   - 19 requêtes légitimes sur 390 ont été bloquées par erreur (taux de faux positifs de 4,87 %), ce qui reste très modéré pour un système de sécurité en amont d'un LLM.
4. **Alignement pour la Phase 4 (Dashboard de comparaison) :**
   - Le fichier `distilbert_test_predictions.csv` est correctement structuré avec `example_id`, `y_true`, `y_pred` et `score_malicious`, prêt pour la confrontation avec la Baseline de Taoufik.
