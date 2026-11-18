import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score,
    confusion_matrix
)
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
    set_seed
)
from datasets import Dataset

# -----------------------------------------------------------------------------
# 1. CONFIGURATION GLOBALE
# -----------------------------------------------------------------------------
SEED = 42
set_seed(SEED)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data_processed" / "full"
OUTPUT_DIR = PROJECT_ROOT / "03_distilbert_ayoub"
ARTIFACTS_DIR = OUTPUT_DIR / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "distilbert-base-uncased"
MAX_LENGTH = 512
NUM_LABELS = 2
BATCH_SIZE = 16
NUM_EPOCHS = 3
LEARNING_RATE = 2e-5

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[*] Utilisation du device : {device}")

# -----------------------------------------------------------------------------
# 2. CHARGEMENT DES DONNÉES
# -----------------------------------------------------------------------------
print("[*] Chargement des données Parquet...")
train_df = pd.read_parquet(DATA_DIR / "train.parquet")
val_df = pd.read_parquet(DATA_DIR / "validation.parquet")
test_df = pd.read_parquet(DATA_DIR / "test.parquet")

# Ajout d'un example_id stable pour l'alignement test
test_df["example_id"] = [f"test_{i:04d}" for i in range(len(test_df))]

print(f"    Train      : {len(train_df)} exemples")
print(f"    Validation : {len(val_df)} exemples")
print(f"    Test       : {len(test_df)} exemples")

# -----------------------------------------------------------------------------
# 3. TOKENISATION ET ANALYSE DE TRONCATURE
# -----------------------------------------------------------------------------
print(f"[*] Chargement du tokenizer : {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        max_length=MAX_LENGTH,
        truncation=True
    )

train_ds = Dataset.from_pandas(train_df[["text", "label"]])
val_ds = Dataset.from_pandas(val_df[["text", "label"]])
test_ds = Dataset.from_pandas(test_df[["text", "label", "example_id"]])

train_tokenized = train_ds.map(tokenize_function, batched=True)
val_tokenized = val_ds.map(tokenize_function, batched=True)
test_tokenized = test_ds.map(tokenize_function, batched=True)

# Mesure de troncature sur le train
raw_token_lengths = [len(tokenizer.encode(t, truncation=False)) for t in train_df["text"]]
truncated_count = sum(1 for l in raw_token_lengths if l > MAX_LENGTH)
truncation_rate = (truncated_count / len(raw_token_lengths)) * 100
print(f"[*] Taux de troncature (Train > {MAX_LENGTH} tokens) : {truncation_rate:.2f}% ({truncated_count}/{len(raw_token_lengths)})")

# -----------------------------------------------------------------------------
# 4. CONFIGURATION DU MODÈLE ET MÉTRIQUES
# -----------------------------------------------------------------------------
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    probs = torch.softmax(torch.tensor(logits), dim=1)[:, 1].numpy()

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="binary", pos_label=1, zero_division=0
    )
    acc = accuracy_score(labels, preds)
    try:
        roc_auc = roc_auc_score(labels, probs)
    except Exception:
        roc_auc = 0.0

    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc
    }

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

training_args = TrainingArguments(
    output_dir=str(ARTIFACTS_DIR / "checkpoints"),
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=LEARNING_RATE,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=NUM_EPOCHS,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    greater_is_better=True,
    logging_dir=str(ARTIFACTS_DIR / "logs"),
    logging_steps=50,
    seed=SEED,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tokenized,
    eval_dataset=val_tokenized,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

# -----------------------------------------------------------------------------
# 5. ENTRAÎNEMENT
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("DÉBUT DU FINE-TUNING DE DISTILBERT")
print("=" * 60)
start_time = time.time()
trainer.train()
training_duration = time.time() - start_time
print(f"[*] Entraînement terminé en {training_duration / 60:.2f} minutes.")

# Sauvegarde du modèle final
final_model_dir = ARTIFACTS_DIR / "distilbert_saved_model"
trainer.save_model(str(final_model_dir))
tokenizer.save_pretrained(str(final_model_dir))
print(f"[*] Modèle et tokenizer sauvegardés dans : {final_model_dir}")

# -----------------------------------------------------------------------------
# 6. ÉVALUATION SUR LE JEU DE TEST
# -----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("ÉVALUATION SUR LE JEU DE TEST")
print("=" * 60)
test_predictions = trainer.predict(test_tokenized)
logits = test_predictions.predictions
y_pred = np.argmax(logits, axis=1)
probs = torch.softmax(torch.tensor(logits), dim=1)[:, 1].numpy()
y_true = np.array(test_df["label"].tolist())

# Calcul des métriques
acc = accuracy_score(y_true, y_pred)
precision, recall, f1, support = precision_recall_fscore_support(
    y_true, y_pred, average="binary", pos_label=1, zero_division=0
)
precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
    y_true, y_pred, average="macro", zero_division=0
)
roc_auc = roc_auc_score(y_true, probs)

cm = confusion_matrix(y_true, y_pred)
tn, fp, fn, tp = cm.ravel()

metrics = {
    "model": "DistilBERT (distilbert-base-uncased)",
    "dataset": "neuralchemy/Prompt-injection-dataset (full)",
    "split_evaluated": "test",
    "test_samples": len(y_true),
    "accuracy": round(float(acc), 4),
    "precision_malicious": round(float(precision), 4),
    "recall_malicious": round(float(recall), 4),
    "f1_malicious": round(float(f1), 4),
    "macro_f1": round(float(f1_macro), 4),
    "roc_auc": round(float(roc_auc), 4),
    "confusion_matrix": {
        "true_negative_benign": int(tn),
        "false_positive_benign_as_malicious": int(fp),
        "false_negative_malicious_missed": int(fn),
        "true_positive_malicious_detected": int(tp)
    },
    "truncation_rate_percent": round(float(truncation_rate), 2),
    "training_time_minutes": round(training_duration / 60, 2),
    "device_used": str(device)
}

print(json.dumps(metrics, indent=2))

# Sauvegarde des métriques JSON
with open(OUTPUT_DIR / "distilbert_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

# -----------------------------------------------------------------------------
# 7. EXPORT DES PRÉDICTIONS POUR ALIGNEMENT (CSV)
# -----------------------------------------------------------------------------
pred_df = pd.DataFrame({
    "example_id": test_df["example_id"],
    "y_true": y_true,
    "y_pred": y_pred,
    "score_malicious": probs
})
pred_df.to_csv(OUTPUT_DIR / "distilbert_test_predictions.csv", index=False)
print(f"[*] Prédictions de test exportées dans : {OUTPUT_DIR / 'distilbert_test_predictions.csv'}")

# -----------------------------------------------------------------------------
# 8. MATRICE DE CONFUSION (FIGURE)
# -----------------------------------------------------------------------------
plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Bénin (0)", "Malveillant (1)"],
    yticklabels=["Bénin (0)", "Malveillant (1)"]
)
plt.xlabel("Classe Prédite")
plt.ylabel("Classe Réelle")
plt.title("Matrice de Confusion — DistilBERT (Test)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "distilbert_confusion_matrix.png", dpi=300)
plt.close()
print(f"[*] Matrice de confusion enregistrée dans : {OUTPUT_DIR / 'distilbert_confusion_matrix.png'}")

print("\n" + "=" * 60)
print("PHASE 3 FINALISÉE AVEC SUCCÈS")
print("=" * 60)

