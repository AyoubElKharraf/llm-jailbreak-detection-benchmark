# Guide de Suivi et Protocole d'Exécution — Phase 2 (Taoufik)

Ce document sert de **feuille de route opérationnelle** pour Taoufik (ou tout agent d'assistance qui l'accompagne) afin de réaliser la Phase 2 de manière autonome, rigoureuse et parfaitement alignée avec le reste du projet.

---

## 1. Contexte & Données d'Entrée
- **Responsable :** Mansouri Taoufik
- **Données d'entrée (déjà prêtes et validées) :**
  - Train : `data_processed/core/train.parquet` (4 391 exemples)
  - Validation : `data_processed/core/validation.parquet` (941 exemples)
  - Test : `data_processed/core/test.parquet` (942 exemples)
- **Tâche :** Classification binaire
  - Label `0` : Bénin (Safe)
  - Label `1` : Malveillant (Injection / Jailbreak) — **Classe positive cible**

---

## 2. Feuille de Route Détaillée (Étapes à Réaliser)

### Étape 1 : Créer le script d'entraînement `train_baseline.py`
Le script doit :
1. Charger les partitions Parquet depuis `data_processed/core/`.
2. Gérer un identifiant stable par exemple : créer `example_id` (soit l'index de ligne soit un hachage/index stable de 0 à N-1) pour permettre l'alignement exact avec DistilBERT.
3. Construire un `Pipeline` scikit-learn :
   - `TfidfVectorizer` : ajusté **uniquement** sur `train` (tester n-grammes (1, 1) ou (1, 2), `min_df`, suppression/conservation de la casse).
   - `LogisticRegression` : paramètres à explorer (ex: `C=0.1, 1.0, 10.0`, `solver='liblinear'` ou `'lbfgs'`, `class_weight='balanced'` ou `None`).
4. Évaluer sur `validation.parquet` pour sélectionner le meilleur jeu d'hyperparamètres (critère : **F1-score sur la classe 1 / Macro F1**).
5. Ré-entraîner ou figer le meilleur modèle et l'évaluer **une seule fois sur `test.parquet`**.

### Étape 2 : Exporter les artefacts et métriques
À la fin de l'évaluation sur le jeu de test :
1. Exporter les prédictions dans `02_baseline_taoufik/baseline_test_predictions.csv` avec les colonnes :
   - `example_id`
   - `y_true`
   - `y_pred`
   - `score_malicious` (probabilité prédite pour la classe 1 via `predict_proba`)
2. Sauvegarder les métriques globales dans `02_baseline_taoufik/baseline_metrics.json` :
   - Accuracy, Precision, Recall, F1-score (classe 1 et macro), ROC-AUC.
3. Sauvegarder la matrice de confusion dans `02_baseline_taoufik/baseline_confusion_matrix.png`.
4. Sauvegarder le modèle entraîné dans `02_baseline_taoufik/artifacts/baseline_model.joblib`.

### Étape 3 : Compléter la fiche d'expérience
Renseigner le fichier `02_baseline_taoufik/baseline_experiment.md` :
- Paramètres testés et choix retenu.
- Métriques obtenues sur le test.
- Analyse concise des erreurs (notamment les faux négatifs : injections non détectées).

---

## 3. Checklist de Validation pour Taoufik

- [ ] Données lues depuis `data_processed/core/` (et non `data_local/`).
- [ ] Vectoriseur TF-IDF ajusté exclusivement sur l'ensemble `train`.
- [ ] Hyperparamètres sélectionnés uniquement sur `validation`.
- [ ] Jeu de test (`test.parquet`) évalué une seule fois sans fuite.
- [ ] Export de `baseline_test_predictions.csv` contenant `example_id`, `y_true`, `y_pred`, `score_malicious`.
- [ ] Matrice de confusion et métriques JSON enregistrées.
- [ ] Fiche `baseline_experiment.md` rédigée.

---

## 4. Prompt d'Accueil pour l'Agent (À copier-coller par Taoufik)

Quand Taoufik ouvre une nouvelle session ou veut travailler sur cette phase avec un agent, il peut fournir ce prompt :

```text
Bonjour ! Je suis Mansouri Taoufik et je commence à travailler sur la Phase 2 de notre projet de détection de jailbreak/injection LLM (dossier `02_baseline_taoufik/`).
La Phase 1 (EDA et préparation des données dans data_processed/) est déjà validée et close.
Mon objectif dans cette phase est :
1. Développer le script d'entraînement `train_baseline.py` (TF-IDF + Logistic Regression).
2. Utiliser `data_processed/core/train.parquet` et optimiser les hyperparamètres sur `validation.parquet`.
3. Évaluer le modèle final sur `data_processed/core/test.parquet`.
4. Exporter les prédictions test (`baseline_test_predictions.csv`), les métriques (`baseline_metrics.json`), la matrice de confusion (`baseline_confusion_matrix.png`) et rédiger `baseline_experiment.md`.
Consulte le fichier `02_baseline_taoufik/PROCESS_SUIVI_TAOUFIK.md` et `GUIDE_BASELINE.md` pour respecter exactement le protocole établi sans conflit.
```

