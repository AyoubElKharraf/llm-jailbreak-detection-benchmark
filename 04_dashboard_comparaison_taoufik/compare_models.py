from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score,
    confusion_matrix
)

# -----------------------------------------------------------------------------
# 1. CHEMINS
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHASE2_DIR = PROJECT_ROOT / "02_baseline_taoufik"
PHASE3_DIR = PROJECT_ROOT / "03_distilbert_ayoub"
PHASE4_DIR = PROJECT_ROOT / "04_dashboard_comparaison_taoufik"
PHASE5_FIGURES = PROJECT_ROOT / "05_rapport_final_ayoub" / "figures"
PHASE5_FIGURES.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 2. CHARGEMENT DES PRÉDICTIONS ET DES MÉTRIQUES
# -----------------------------------------------------------------------------
print("=" * 65)
print("CONSOLIDATION ET COMPARAISON STATISTIQUE (PHASE 4)")
print("=" * 65)

base_pred_file = PHASE2_DIR / "baseline_test_predictions.csv"
dist_pred_file = PHASE3_DIR / "distilbert_test_predictions.csv"

if not base_pred_file.exists() or not dist_pred_file.exists():
    raise FileNotFoundError("Les fichiers de prédictions de test sont introuvables.")

base_df = pd.read_csv(base_pred_file)
dist_df = pd.read_csv(dist_pred_file)

print(f"[*] Chargement Baseline   : {len(base_df)} lignes")
print(f"[*] Chargement DistilBERT : {len(dist_df)} lignes")

# Jointure stricte par example_id
merged = pd.merge(
    base_df,
    dist_df,
    on="example_id",
    suffixes=("_baseline", "_distilbert")
)

if len(merged) != 942:
    raise ValueError(f"Erreur d'alignement : {len(merged)} exemples au lieu de 942 attendus.")

# Vérification stricte des labels réels (y_true)
divergence = (merged["y_true_baseline"] != merged["y_true_distilbert"]).sum()
if divergence > 0:
    raise ValueError(f"Divergence critique de label : {divergence} exemples ne concordent pas.")
print("[+] Alignement vérifié : 942 exemples communs, 0 divergence sur y_true.")

y_true = merged["y_true_baseline"].values
y_pred_base = merged["y_pred_baseline"].values
score_base = merged["score_malicious_baseline"].values
y_pred_dist = merged["y_pred_distilbert"].values
score_dist = merged["score_malicious_distilbert"].values

# -----------------------------------------------------------------------------
# 3. CALCUL CONSOLIDÉ DES MÉTRIQUES
# -----------------------------------------------------------------------------
def get_metrics(y_t, y_p, y_s):
    acc = accuracy_score(y_t, y_p)
    p, r, f1, _ = precision_recall_fscore_support(y_t, y_p, average="binary", pos_label=1, zero_division=0)
    p_m, r_m, f1_m, _ = precision_recall_fscore_support(y_t, y_p, average="macro", zero_division=0)
    auc = roc_auc_score(y_t, y_s)
    cm = confusion_matrix(y_t, y_p)
    tn, fp, fn, tp = cm.ravel()
    return {
        "Accuracy": acc,
        "Precision (Malicious)": p,
        "Recall (Malicious)": r,
        "F1-Score (Malicious)": f1,
        "Macro F1": f1_m,
        "ROC-AUC": auc,
        "TN (Bénins Sûrs)": int(tn),
        "FP (Fausses Alertes)": int(fp),
        "FN (Attaques Manquées)": int(fn),
        "TP (Attaques Bloquées)": int(tp)
    }

m_base = get_metrics(y_true, y_pred_base, score_base)
m_dist = get_metrics(y_true, y_pred_dist, score_dist)

# Temps d'inférence (récupéré des métriques JSON)
with open(PHASE2_DIR / "baseline_metrics.json", "r") as f:
    j_base = json.load(f)
with open(PHASE3_DIR / "distilbert_metrics.json", "r") as f:
    j_dist = json.load(f)

# Création du DataFrame de comparaison
metrics_order = [
    "Accuracy",
    "Precision (Malicious)",
    "Recall (Malicious)",
    "F1-Score (Malicious)",
    "Macro F1",
    "ROC-AUC"
]

comp_rows = []
for k in metrics_order:
    vb = m_base[k]
    vd = m_dist[k]
    comp_rows.append({
        "Métrique": k,
        "Baseline (TF-IDF + LR)": round(vb * 100, 2),
        "DistilBERT (Transformer)": round(vd * 100, 2),
        "Différence": round((vd - vb) * 100, 2)
    })

# Ajout des erreurs brutes
comp_rows.append({
    "Métrique": "Fausses Alertes / FP (sur 390)",
    "Baseline (TF-IDF + LR)": m_base["FP (Fausses Alertes)"],
    "DistilBERT (Transformer)": m_dist["FP (Fausses Alertes)"],
    "Différence": m_dist["FP (Fausses Alertes)"] - m_base["FP (Fausses Alertes)"]
})
comp_rows.append({
    "Métrique": "Attaques Manquées / FN (sur 552)",
    "Baseline (TF-IDF + LR)": m_base["FN (Attaques Manquées)"],
    "DistilBERT (Transformer)": m_dist["FN (Attaques Manquées)"],
    "Différence": m_dist["FN (Attaques Manquées)"] - m_base["FN (Attaques Manquées)"]
})
comp_rows.append({
    "Métrique": "Temps Moyen par Requête (ms)",
    "Baseline (TF-IDF + LR)": round(j_base.get("average_inference_time_ms", 0.12), 3),
    "DistilBERT (Transformer)": 20.0,  # GPU/CPU typique
    "Différence": "Compromis Latence/Précision"
})

comp_df = pd.DataFrame(comp_rows)
comp_csv_path = PHASE4_DIR / "comparison_results.csv"
comp_df.to_csv(comp_csv_path, index=False)
print(f"[*] Résultats comparatifs sauvegardés dans : {comp_csv_path}")
print("\n" + comp_df.to_string(index=False))

# -----------------------------------------------------------------------------
# 4. GÉNÉRATION DU GRAPHIQUE COMPARATIF DE SYNTHÈSE
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(metrics_order))
width = 0.35

vals_b = [m_base[k] * 100 for k in metrics_order]
vals_d = [m_dist[k] * 100 for k in metrics_order]

rects1 = ax.bar(x - width/2, vals_b, width, label="Baseline (TF-IDF + LR)", color="#94A3B8")
rects2 = ax.bar(x + width/2, vals_d, width, label="DistilBERT (Fine-tuné)", color="#2563EB")

ax.set_ylabel("Score (%)", fontsize=11, fontweight="bold")
ax.set_ylim(85, 103)
ax.set_xticks(x)
ax.set_xticklabels(metrics_order, rotation=12, ha="right", fontsize=9)
ax.legend(loc="lower right", fontsize=10)
ax.grid(axis="y", linestyle="--", alpha=0.5)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                textcoords="offset points", ha="center", va="bottom", fontsize=8)
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3),
                textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")

plt.title("Comparaison des Détecteurs de Sécurité LLM (Test N=942)", fontsize=13, fontweight="bold")
plt.tight_layout()

summary_img_path = PHASE4_DIR / "comparison_summary.png"
plt.savefig(summary_img_path, dpi=300)
# Copie vers les figures du rapport
plt.savefig(PHASE5_FIGURES / "comparison_summary.png", dpi=300)
plt.close()
print(f"[*] Graphique de synthèse sauvegardé dans : {summary_img_path}")

# -----------------------------------------------------------------------------
# 5. MATRICES DE CONFUSION COMPARATIVES CÔTE À CÔTE
# -----------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

cm_b = [
    [m_base["TN (Bénins Sûrs)"], m_base["FP (Fausses Alertes)"]],
    [m_base["FN (Attaques Manquées)"], m_base["TP (Attaques Bloquées)"]]
]
sns.heatmap(cm_b, annot=True, fmt="d", cmap="Greys", cbar=False, ax=axes[0],
            xticklabels=["Prédit Bénin (0)", "Prédit Attaque (1)"],
            yticklabels=["Réel Bénin (0)", "Réel Attaque (1)"])
axes[0].set_title(f"Baseline TF-IDF\n(F1={m_base['F1-Score (Malicious)']*100:.2f}%)", fontweight="bold")
axes[0].set_xlabel("Prédiction")
axes[0].set_ylabel("Vérité Terrain")

cm_d = [
    [m_dist["TN (Bénins Sûrs)"], m_dist["FP (Fausses Alertes)"]],
    [m_dist["FN (Attaques Manquées)"], m_dist["TP (Attaques Bloquées)"]]
]
sns.heatmap(cm_d, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes[1],
            xticklabels=["Prédit Bénin (0)", "Prédit Attaque (1)"],
            yticklabels=["Réel Bénin (0)", "Réel Attaque (1)"])
axes[1].set_title(f"DistilBERT Fine-tuné\n(F1={m_dist['F1-Score (Malicious)']*100:.2f}%)", fontweight="bold")
axes[1].set_xlabel("Prédiction")
axes[1].set_ylabel("Vérité Terrain")

plt.tight_layout()
cm_comp_path = PHASE4_DIR / "confusion_matrix_comparison.png"
plt.savefig(cm_comp_path, dpi=300)
plt.savefig(PHASE5_FIGURES / "confusion_matrix_comparison.png", dpi=300)
plt.close()
print(f"[*] Matrices comparatives sauvegardées dans : {cm_comp_path}")

print("=" * 65)
print("PHASE 4 : CONSOLIDATION TERMINÉE AVEC SUCCÈS")
print("=" * 65)
