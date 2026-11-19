# Baseline TF-IDF + Logistic Regression

## Dataset
- Source : data_processed/core
- Train initial : 4391
- Validation : 941
- Test : 942
- Classes : 0 = Benign, 1 = Malicious

## Protocole
- TF-IDF ajusté sur train uniquement pendant la sélection.
- Hyperparamètres sélectionnés sur validation.
- Modèle final réentraîné sur train + validation.
- Test utilisé uniquement pour l'évaluation finale.

## Meilleurs paramètres
```json
{
    "ngram_range": [
        1,
        2
    ],
    "min_df": 2,
    "lowercase": true,
    "C": 10.0,
    "class_weight": "balanced",
    "solver": "liblinear"
}
```

## Résultats Test
```json
{
    "model": "TF-IDF + Logistic Regression",
    "positive_class": 1,
    "class_mapping": {
        "0": "Benign",
        "1": "Malicious"
    },
    "test_samples": 942,
    "accuracy": 0.9575371549893843,
    "precision_malicious": 0.9522968197879859,
    "recall_malicious": 0.9764492753623188,
    "f1_malicious": 0.964221824686941,
    "macro_f1": 0.9560012517690579,
    "roc_auc": 0.9954570791527313,
    "confusion_matrix": {
        "true_negative_benign": 363,
        "false_positive_benign_as_malicious": 27,
        "false_negative_malicious_missed": 13,
        "true_positive_malicious_detected": 539
    },
    "inference_time_seconds": 0.11307046600086323,
    "average_inference_time_ms": 0.12003234182681871,
    "best_parameters": {
        "ngram_range": [
            1,
            2
        ],
        "min_df": 2,
        "lowercase": true,
        "C": 10.0,
        "class_weight": "balanced",
        "solver": "liblinear"
    },
    "random_state": 42
}
```

## Comparaison des configurations
Voir `baseline_validation_results.csv`.
