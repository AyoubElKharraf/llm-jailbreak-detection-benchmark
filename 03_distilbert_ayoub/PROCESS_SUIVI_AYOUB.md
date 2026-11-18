# Guide de Suivi et Protocole d'Exécution — Phase 3 (Ayoub)

Ce document sert de **feuille de route opérationnelle** pour Ayoub (fine-tuning de DistilBERT) afin d'assurer une exécution rigoureuse, reproductible et directement alignée avec la Baseline de Taoufik.

---

## 1. Contexte & Données d'Entrée
- **Responsable :** Ayoub El Kharraf
- **Modèle cible :** `distilbert-base-uncased` (Hugging Face Transformers)
- **Données d'entraînement :** `data_processed/full/train.parquet` (13 934 exemples nets après déduplication)
- **Données de validation :** `data_processed/full/validation.parquet` (941 exemples)
- **Données de test :** `data_processed/full/test.parquet` (942 exemples)
- **Mapping binaire :**
  - `0` : Bénin
  - `1` : Malveillant (Injection / Jailbreak) — **Classe positive**

---

## 2. Feuille de Route Détaillée

### Étape 1 : Script d'entraînement `train_distilbert.py`
Le script doit réaliser les opérations suivantes :
1. **Chargement des données :** Lire les Parquets depuis `data_processed/full/`.
2. **Attribution d'`example_id` :** Utiliser un identifiant stable pour le split test (index `0` à `941` ou hash de `text + label`) identique à la baseline.
3. **Tokenisation :**
   - Modèle : `distilbert-base-uncased`
   - Longueur maximale : `max_length = 512`
   - Padding & Troncature : `truncation=True, padding=True`
   - Calculer et consigner le pourcentage de textes tronqués dans le dataset (d'après l'EDA, seule une infime minorité dépasse 512 tokens).
4. **Configuration du Fine-Tuning :**
   - Architecture : `AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)`
   - Hyperparamètres recommandés pour démarrer :
     - Époques : 3
     - Batch size : 16 (ou 8 avec gradient accumulation si contrainte VRAM GPU / CPU)
     - Learning rate : `2e-5` avec scheduler linéaire et warmup
     - Optimiseur : AdamW (weight decay = 0.01)
     - Métrique d'évaluation principale : **F1-score (classe 1)** ou Macro-F1 sur le jeu de validation.
     - Sauvegarde du meilleur modèle : `load_best_model_at_end=True`, `metric_for_best_model="f1"`.

### Étape 2 : Évaluation sur le jeu de Test
Une fois l'entraînement terminé et le meilleur checkpoint restauré :
1. Prédire sur `data_processed/full/test.parquet`.
2. Calculer les probabilités avec Softmax pour extraire `score_malicious` (probabilité de la classe 1).
3. Générer les métriques finales : Accuracy, Precision, Recall, F1-score, ROC-AUC, support par classe.

### Étape 3 : Export des Livrables
1. **Prédictions :** `03_distilbert_ayoub/distilbert_test_predictions.csv`
   - Colonnes : `example_id`, `y_true`, `y_pred`, `score_malicious`
2. **Métriques :** `03_distilbert_ayoub/distilbert_metrics.json`
3. **Matrice de confusion :** `03_distilbert_ayoub/distilbert_confusion_matrix.png`
4. **Fiche d'expérience :** `03_distilbert_ayoub/distilbert_experiment.md`
5. **Modèle entraîné & tokenizer :** sauvegardés localement dans `03_distilbert_ayoub/artifacts/distilbert_saved_model/` (ignoré par Git pour éviter d'alourdir le dépôt).

---

## 3. Checklist de Validation pour Ayoub

- [ ] Données lues depuis `data_processed/full/`.
- [ ] Tokenizer configuré avec `distilbert-base-uncased` (`max_length=512`).
- [ ] Taux de troncature mesuré et documenté.
- [ ] Meilleur checkpoint sélectionné sur `validation.parquet`.
- [ ] Jeu de test évalué une seule fois à la fin.
- [ ] Export de `distilbert_test_predictions.csv` parfaitement alignable avec celui de Taoufik.
- [ ] Rapport d'expérience `distilbert_experiment.md` rempli.

