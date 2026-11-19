import json
import time
import warnings
from pathlib import Path
from itertools import product

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

warnings.filterwarnings("ignore")

# =====================================================
# 1. CONFIGURATION
# =====================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data_processed" / "core"
OUTPUT_DIR = ROOT_DIR / "02_baseline_taoufik"
ARTIFACT_DIR = OUTPUT_DIR / "artifacts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42

print("=" * 60)
print("BASELINE : TF-IDF + LOGISTIC REGRESSION")
print("=" * 60)


# =====================================================
# 2. CHARGEMENT DES DONNEES
# =====================================================

print("\n[1/6] Chargement des données...")

train_df = pd.read_parquet(DATA_DIR / "train.parquet")
val_df = pd.read_parquet(DATA_DIR / "validation.parquet")
test_df = pd.read_parquet(DATA_DIR / "test.parquet")

for name, df in [
    ("Train", train_df),
    ("Validation", val_df),
    ("Test", test_df),
]:
    if not {"text", "label"}.issubset(df.columns):
        raise ValueError(f"Colonnes text/label manquantes dans {name}")

    if df["text"].isna().any() or (df["text"].str.strip() == "").any():
        raise ValueError(f"Textes vides détectés dans {name}")

    if not set(df["label"].unique()).issubset({0, 1}):
        raise ValueError(f"Labels invalides dans {name}")

    print(f"{name}: {len(df)} exemples")
    print("  Labels :", df["label"].value_counts().to_dict())

X_train = train_df["text"].astype(str)
y_train = train_df["label"].astype(int)

X_val = val_df["text"].astype(str)
y_val = val_df["label"].astype(int)

X_test = test_df["text"].astype(str)
y_test = test_df["label"].astype(int)

# Identifiants alignés sur l'ordre du dataset DistilBERT
test_ids = [f"test_{i:04d}" for i in range(len(test_df))]

print("\nDonnées chargées avec succès.")


# =====================================================
# 3. RECHERCHE DES HYPERPARAMETRES
# =====================================================

print("\n[2/6] Recherche des hyperparamètres...")

param_grid = {
    "ngram_range": [(1, 1), (1, 2)],
    "min_df": [1, 2],
    "lowercase": [True, False],
    "C": [0.1, 1.0, 10.0],
    "class_weight": [None, "balanced"],
}

configurations = list(product(
    param_grid["ngram_range"],
    param_grid["min_df"],
    param_grid["lowercase"],
    param_grid["C"],
    param_grid["class_weight"],
))

results = []
best_model = None
best_score = -1
best_macro_f1 = -1
best_params = None

print(f"Nombre de configurations : {len(configurations)}")

for index, (ngram, min_df, lowercase, C, class_weight) in enumerate(
    configurations, start=1
):

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=ngram,
            min_df=min_df,
            lowercase=lowercase,
            sublinear_tf=True,
        )),
        ("classifier", LogisticRegression(
            C=C,
            solver="liblinear",
            class_weight=class_weight,
            random_state=RANDOM_STATE,
            max_iter=2000,
        )),
    ])

    # Entraînement uniquement sur TRAIN
    pipeline.fit(X_train, y_train)

    # Sélection uniquement sur VALIDATION
    val_pred = pipeline.predict(X_val)

    malicious_f1 = f1_score(
        y_val, val_pred, pos_label=1, zero_division=0
    )

    macro_f1 = f1_score(
        y_val, val_pred, average="macro", zero_division=0
    )

    params = {
        "ngram_range": list(ngram),
        "min_df": min_df,
        "lowercase": lowercase,
        "C": C,
        "class_weight": class_weight,
        "solver": "liblinear",
    }

    results.append({
        **params,
        "validation_f1_malicious": malicious_f1,
        "validation_macro_f1": macro_f1,
    })

    if (
        malicious_f1 > best_score
        or (
            malicious_f1 == best_score
            and macro_f1 > best_macro_f1
        )
    ):
        best_score = malicious_f1
        best_macro_f1 = macro_f1
        best_model = pipeline
        best_params = params

    print(
        f"[{index}/{len(configurations)}] "
        f"F1 Malicious={malicious_f1:.4f} | "
        f"Macro F1={macro_f1:.4f}"
    )

results_df = pd.DataFrame(results)
results_df.to_csv(
    OUTPUT_DIR / "baseline_validation_results.csv",
    index=False
)

print("\nMeilleure configuration :")
print(json.dumps(best_params, indent=4))
print("Validation F1 Malicious :", round(best_score, 4))
print("Validation Macro F1 :", round(best_macro_f1, 4))


# =====================================================
# 4. EVALUATION FINALE SUR TEST
# =====================================================

print("\n[3/6] Réentraînement sur TRAIN + VALIDATION...")

# Après sélection des hyperparamètres, on peut réunir
# train et validation pour entraîner le modèle final.
X_train_final = pd.concat([X_train, X_val], ignore_index=True)
y_train_final = pd.concat([y_train, y_val], ignore_index=True)

final_model = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=tuple(best_params["ngram_range"]),
        min_df=best_params["min_df"],
        lowercase=best_params["lowercase"],
        sublinear_tf=True,
    )),
    ("classifier", LogisticRegression(
        C=best_params["C"],
        solver="liblinear",
        class_weight=best_params["class_weight"],
        random_state=RANDOM_STATE,
        max_iter=2000,
    )),
])

final_model.fit(X_train_final, y_train_final)

print("\n[4/6] Évaluation finale sur TEST...")

start_time = time.perf_counter()

y_pred = final_model.predict(X_test)
y_proba = final_model.predict_proba(X_test)[:, 1]

inference_time = time.perf_counter() - start_time

# =====================================================
# 5. CALCUL DES METRIQUES
# =====================================================

print("\n[5/6] Calcul des métriques...")

tn, fp, fn, tp = confusion_matrix(
    y_test, y_pred, labels=[0, 1]
).ravel()

metrics = {
    "model": "TF-IDF + Logistic Regression",
    "positive_class": 1,
    "class_mapping": {
        "0": "Benign",
        "1": "Malicious",
    },
    "test_samples": len(y_test),
    "accuracy": float(accuracy_score(y_test, y_pred)),
    "precision_malicious": float(
        precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    ),
    "recall_malicious": float(
        recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    ),
    "f1_malicious": float(
        f1_score(y_test, y_pred, pos_label=1, zero_division=0)
    ),
    "macro_f1": float(
        f1_score(y_test, y_pred, average="macro", zero_division=0)
    ),
    "roc_auc": float(roc_auc_score(y_test, y_proba)),
    "confusion_matrix": {
        "true_negative_benign": int(tn),
        "false_positive_benign_as_malicious": int(fp),
        "false_negative_malicious_missed": int(fn),
        "true_positive_malicious_detected": int(tp),
    },
    "inference_time_seconds": float(inference_time),
    "average_inference_time_ms": float(
        inference_time / len(X_test) * 1000
    ),
    "best_parameters": best_params,
    "random_state": RANDOM_STATE,
}

print(json.dumps(metrics, indent=4))

with open(OUTPUT_DIR / "baseline_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)


# =====================================================
# 6. EXPORT DES PREDICTIONS ET DU MODELE
# =====================================================

print("\n[6/6] Export des résultats...")

predictions = pd.DataFrame({
    "example_id": test_ids,
    "y_true": y_test.to_numpy(),
    "y_pred": y_pred,
    "score_malicious": y_proba,
})

predictions.to_csv(
    OUTPUT_DIR / "baseline_test_predictions.csv",
    index=False
)

joblib.dump(
    final_model,
    ARTIFACT_DIR / "baseline_model.joblib"
)

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Benign (0)", "Malicious (1)"],
)

fig, ax = plt.subplots(figsize=(7, 6))
display.plot(
    ax=ax,
    cmap="Blues",
    values_format="d",
    colorbar=False
)

plt.title("Baseline - TF-IDF + Logistic Regression")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "baseline_confusion_matrix.png",
    dpi=300
)
plt.close()

# Documentation des expériences
with open(OUTPUT_DIR / "baseline_experiment.md", "w") as f:
    f.write("# Baseline TF-IDF + Logistic Regression\n\n")
    f.write("## Dataset\n")
    f.write("- Source : data_processed/core\n")
    f.write(f"- Train initial : {len(train_df)}\n")
    f.write(f"- Validation : {len(val_df)}\n")
    f.write(f"- Test : {len(test_df)}\n")
    f.write("- Classes : 0 = Benign, 1 = Malicious\n\n")

    f.write("## Protocole\n")
    f.write("- TF-IDF ajusté sur train uniquement pendant la sélection.\n")
    f.write("- Hyperparamètres sélectionnés sur validation.\n")
    f.write("- Modèle final réentraîné sur train + validation.\n")
    f.write("- Test utilisé uniquement pour l'évaluation finale.\n\n")

    f.write("## Meilleurs paramètres\n")
    f.write("```json\n")
    f.write(json.dumps(best_params, indent=4))
    f.write("\n```\n\n")

    f.write("## Résultats Test\n")
    f.write("```json\n")
    f.write(json.dumps(metrics, indent=4))
    f.write("\n```\n\n")

    f.write("## Comparaison des configurations\n")
    f.write("Voir `baseline_validation_results.csv`.\n")

print("\n" + "=" * 60)
print("ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS")
print("=" * 60)

print("\nFichiers générés :")
for file in [
    "baseline_validation_results.csv",
    "baseline_test_predictions.csv",
    "baseline_metrics.json",
    "baseline_confusion_matrix.png",
    "baseline_experiment.md",
    "artifacts/baseline_model.joblib",
]:
    print(" -", OUTPUT_DIR / file)
