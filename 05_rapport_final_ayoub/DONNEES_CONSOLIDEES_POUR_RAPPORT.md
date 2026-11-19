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

## 📁 PHASE 2 : BASELINE TF-IDF + RÉGRESSION LOGISTIQUE (Terminée — Taoufik)

### 2.1 Outils & Configuration
- **Bibliothèques :** `scikit-learn`, `pandas`, `numpy`
- **Données d'entraînement :** `data_processed/core/train.parquet` (4 391 exemples originaux)
- **Représentation textuelle :** `TfidfVectorizer` (ngram_range=(1,2), min_df=2, lowercase=True) ajusté **uniquement sur le train**
- **Modèle :** `LogisticRegression` (C=10.0, class_weight='balanced', solver='liblinear') optimisé sur `core/validation.parquet`
- **Graine aléatoire :** 42
- **Temps d'inférence total (test 942 ex.) :** 0,113 s (soit **0,120 ms par requête**)

### 2.2 Résultats Réels sur le Jeu de Test (942 exemples)
- **Accuracy :** **95,75 %** (0.9575)
- **Precision (Malveillant) :** **95,23 %** (0.9523)
- **Recall (Malveillant) :** **97,64 %** (0.9764) — *539 attaques interceptées sur 552*
- **F1-Score (Malveillant) :** **96,42 %** (0.9642)
- **Macro F1 :** **95,60 %** (0.9560)
- **ROC-AUC :** **99,55 %** (0.9955)
- **Matrice de Confusion :**
  - Vrais Négatifs (Bénins acceptés) : **363** (sur 390 réels)
  - Faux Positifs (Fausses alertes) : **27** (taux d'erreur : 6,92 %)
  - Faux Négatifs (Attaques manquées) : **13** (taux d'évasion : 2,36 %)
  - Vrais Positifs (Attaques détectées) : **539**

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

## 📁 PHASE 4 : BENCHMARK COMPARATIF & APPLICATION WEB STREAMLIT (Terminée — Taoufik & Ayoub)

### 4.1 Outils & Alignement
- **Script de comparaison :** `04_dashboard_comparaison_taoufik/compare_models.py`
- **Méthode d'alignement :** Jointure stricte sur `example_id` (de `test_0000` à `test_0941`)
- **Taux de concordance des prédictions :** **97,35 %** (917 décisions identiques sur 942)
- **Fichier de synthèse :** `comparison_results.csv`
- **Protocole d'analyse :** `comparison_protocol.md`

### 4.2 Tableau Comparatif Consolidé (Baseline vs DistilBERT)

| Métrique d'Évaluation | Baseline (TF-IDF + LR) | DistilBERT (`full`) | Écart / Gain |
|---|:---:|:---:|---|
| **Accuracy** | 95,75 % | **96,28 %** | **+0,53 %** |
| **Precision (Malveillant)**| 95,23 % | **96,58 %** | **+1,35 %** |
| **Recall (Malveillant)** | **97,64 %** | 97,10 % | -0,54 % |
| **F1-Score (Malveillant)** | 96,42 % | **96,84 %** | **+0,42 %** |
| **Macro F1** | 95,60 % | **96,17 %** | **+0,57 %** |
| **ROC-AUC** | 99,55 % | 99,55 % | Identique (0.9955) |
| **Fausses Alertes (FP / 390)** | 27 (6,92 %) | **19 (4,87 %)** | **-8 erreurs (-30 %)** |
| **Attaques Manquées (FN / 552)** | **13 (2,36 %)** | 16 (2,90 %) | +3 |
| **Latence moyenne d'inférence** | **0,12 ms** | ~15 - 25 ms | Baseline ~150x plus rapide |

### 4.3 Interface Web Interactive (Streamlit)
- **Fichier de l'application :** `04_dashboard_comparaison_taoufik/app.py`
- **État :** 100 % opérationnelle avec 5 pages dynamiques, graphiques interactifs et comparateur en direct.

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

