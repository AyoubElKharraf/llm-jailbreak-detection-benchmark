# Base de Connaissances et Données Consolidées pour le Rapport Final (Phase 5)

Ce document centralise **l'ensemble des détails techniques, définitions, protocoles, outils, métriques et résultats réels** de toutes les phases du projet.
Il sert de **source unique de vérité** pour la rédaction finale du rapport par Ayoub.

---

## 📌 FICHE D'IDENTITÉ DU PROJET
- **Formation :** Master M2I — Semestre 3 — Module 4 : Cybersécurité CEH
- **Groupe :** Groupe 7 (Ayoub El Kharraf & Mansouri Taoufik)
- **Sujet :** Benchmark de Détection de Prompt Injection et de Jailbreak pour la Sécurisation des LLM
- **Architecture de Défense visée :** Couche de détection pré-inférence (*Security Detection Layer* / Pare-feu de prompts filtrant en amont du LLM)
- **Date limite :** 28 novembre 2026

---

## 📁 PHASE 1 : ANALYSE DU DATASET & AUDIT EDA (Terminée — Ayoub & Taoufik)

### 1.1 Source et Versionnage Figé
- **Dataset :** `neuralchemy/Prompt-injection-dataset` (hébergé sur Hugging Face)
- **Commit / Révision figée :** `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75`
- **Tâche :** Classification binaire
  - Classe `0` : **Bénin** (requêtes utilisateurs régulières)
  - Classe `1` : **Malveillant** (attaques de type Prompt Injection ou Jailbreak)
- **Intégrité :** Vérifiée par empreintes SHA-256 sur les fichiers Parquet téléchargés.

### 1.2 Nettoyage et Contribution Méthodologique (Les 102 doublons)
- **Constat :** Dans `full/train`, 102 lignes marquées comme « augmentées » (`augmented=True`) contenaient exactement le même texte, le même label et le même `group_id` qu'un exemple original (`augmented=False`).
- **Action appliquée :** Suppression stricte de ces 102 doublons dans `prepare_dataset.py` pour éviter le surapprentissage artificiel.
- **Effectifs après nettoyage (`data_processed/`) :
  - `core/train` : **4 391** exemples (originaux uniquement, sans augmentation)
  - `full/train` : **13 934** exemples (originaux + augmentations nettoyées)
  - `validation` (commun à core et full) : **941** exemples (407 bénins, 534 malveillants)
  - `test` (commun à core et full) : **942** exemples (390 bénins, 552 malveillants)

### 1.3 Audit Anti-Fuite (*Data Leakage*)
- Contrôle de la variable `group_id` : **Zéro fuite** entre train, validation et test.
- Aucun texte vide (longueur min : 10 caractères, médiane : ~56-59 caractères, max : 7 009 caractères).
- Répartition des classes : ~40 % Bénin, ~60 % Malveillant (léger déséquilibre stable sur tous les splits).
- Diversité des attaques : `direct_injection` (31,8 %), `adversarial` (8,7 %), `jailbreak` (6,6 %), `encoding` (4,0 %), `training_extraction` (1,5 %), etc.

---

## 📁 PHASE 2 : BASELINE TF-IDF + RÉGRESSION LOGISTIQUE (Taoufik)
*(À compléter par Taoufik à la fin de la Phase 2)*

### 2.1 Outils & Configuration
- **Bibliothèques :** `scikit-learn`, `pandas`, `numpy`
- **Données d'entraînement :** `data_processed/core/train.parquet` (4 391 exemples originaux)
- **Représentation textuelle :** `TfidfVectorizer` (n-grammes, vocabulaire ajusté **uniquement sur le train**)
- **Modèle :** `LogisticRegression` (optimisation des hyperparamètres `C`, `penalty`, `solver` sur `core/validation.parquet`)
- **Graine aléatoire :** 42

### 2.2 Résultats Réels sur le Jeu de Test (942 exemples)
- **Accuracy :** `[À insérer par Taoufik]`
- **Precision (Malveillant) :** `[À insérer par Taoufik]`
- **Recall (Malveillant) :** `[À insérer par Taoufik]`
- **F1-Score (Malveillant) :** `[À insérer par Taoufik]`
- **Macro F1 :** `[À insérer par Taoufik]`
- **ROC-AUC :** `[À insérer par Taoufik]`
- **Matrice de Confusion :**
  - Vrais Négatifs (Bénins acceptés) : `[À insérer]`
  - Faux Positifs (Bénins bloqués) : `[À insérer]`
  - Faux Négatifs (Attaques manquées) : `[À insérer]`
  - Vrais Positifs (Attaques détectées) : `[À insérer]`
- **Temps d'inférence moyen :** `[À insérer]` ms / requête

---

## 📁 PHASE 3 : MODÈLE TRANSFORMER DISTILBERT (Terminée — Ayoub)

### 3.1 Outils & Configuration
- **Architecture :** `distilbert-base-uncased` (6 couches Transformer, 66M paramètres)
- **Frameworks :** PyTorch, Hugging Face `transformers`, `datasets`, `accelerate`
- **Données d'entraînement :** `data_processed/full/train.parquet` (13 934 exemples)
- **Environnement matériel :** Google Colab (GPU NVIDIA T4 15 Go VRAM)
- **Hyperparamètres :**
  - Longueur max (`max_length`) : 512 tokens (padding dynamique et troncature)
  - Époques : 3
  - Batch size : 16 (train) / 32 (eval)
  - Optimiseur : AdamW, Learning rate : `2e-5`, weight decay : 0.01
  - Sélection du meilleur modèle : `load_best_model_at_end=True` sur le F1-score de validation
  - Temps d'entraînement : 16,8 minutes

### 3.2 Résultats Réels sur le Jeu de Test (942 exemples)
- **Accuracy :** **96,28 %** (0.9628)
- **Precision (Malveillant) :** **96,58 %** (0.9658)
- **Recall (Malveillant) :** **97,10 %** (0.9710) — *536 attaques détectées sur 552*
- **F1-Score (Malveillant) :** **96,84 %** (0.9684)
- **Macro F1 :** **96,17 %** (0.9617)
- **ROC-AUC :** **99,55 %** (0.9955)
- **Matrice de Confusion :**
  - Vrais Négatifs (VN) : **371** (sur 390 bénins réels)
  - Faux Positifs (FP) : **19** (taux d'erreur : 4,87 %)
  - Faux Négatifs (FN) : **16** (taux d'évasion : 2,90 %)
  - Vrais Positifs (VP) : **536**
- **Artefacts produits :**
  - `distilbert_test_predictions.csv` (aligné avec `example_id`)
  - `distilbert_metrics.json`
  - `distilbert_confusion_matrix.png`
  - `phase03_distilbert_colab_training.ipynb`

---

## 📁 PHASE 4 : BENCHMARK COMPARATIF & APPLICATION WEB STREAMLIT (Taoufik)
*(À compléter par Taoufik à la fin de la Phase 4)*

### 4.1 Outils & Alignement
- **Script de comparaison :** `04_dashboard_comparaison_taoufik/compare_models.py`
- **Méthode d'alignement :** Jointure stricte sur `example_id` (de `test_0000` à `test_0941`)
- **Fichier de synthèse :** `comparison_results.csv`
- **Graphique comparatif :** `comparison_summary.png`

### 4.2 Tableau Comparatif Consolidé (Baseline vs DistilBERT)

| Métrique | Baseline (TF-IDF + LR) | DistilBERT (`full`) | Écart / Gain |
|---|---|---|---|
| **Accuracy** | `[À insérer]` | **96,28 %** | `[À calculer]` |
| **Precision (Malveillant)**| `[À insérer]` | **96,58 %** | `[À calculer]` |
| **Recall (Malveillant)** | `[À insérer]` | **97,10 %** | `[À calculer]` |
| **F1-Score (Malveillant)** | `[À insérer]` | **96,84 %** | `[À calculer]` |
| **ROC-AUC** | `[À insérer]` | **99,55 %** | `[À calculer]` |
| **Latence d'inférence** | `[À insérer]` ms | ~15-30 ms | Compromis Vitesse vs Puissance |

### 4.3 Interface Web Interactive (Streamlit)
- **Fichier de l'application :** `04_dashboard_comparaison_taoufik/app.py`
- **Fonctionnalités intégrées :**
  1. Vue d'ensemble du projet & Schéma d'architecture de défense.
  2. Comparaison graphique interactive des métriques & Matrices de confusion côte à côte.
  3. Analyse forensique des erreurs (Faux Négatifs / Évasions classées par typologie d'attaque).
  4. Démonstrateur interactif en direct (Playground de test de prompts avec jauge de risque).
- **Captures d'écran produites pour le rapport :**
  - `dashboard_overview.png`
  - `dashboard_metrics_comparison.png`
  - `dashboard_error_analysis.png`
  - `dashboard_live_test.png`

---

## 📁 PHASE 5 : ANALYSE CRITIQUE & RECOMMANDATIONS POUR LA SÉCURITÉ LLM

### Points clés à développer dans le rapport :
1. **Compromis Performance vs Latence :**
   - La Baseline classique est ultra-légère (idéale pour du filtrage préliminaire à haute fréquence).
   - DistilBERT offre une compréhension sémantique bien supérieure des attaques obfusquées ou indirectes, justifiant son déploiement en cascade.
2. **Architecture de Défense en Profondeur recommandée :**
   - *Niveau 1 :* Filtre rapide heuristique / TF-IDF pour écarter les injections évidentes à coût zéro.
   - *Niveau 2 :* Modèle Transformer (DistilBERT) pour analyser les nuances sémantiques.
   - *Niveau 3 :* Guardrails post-génération sur la sortie du LLM.
3. **Limites du classifieur :**
   - Un classifieur statistique ne garantit jamais 100 % d'invulnérabilité (attaques adaptatives, encodages non vus).

