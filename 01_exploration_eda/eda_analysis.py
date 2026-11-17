from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data_processed"

EDA_DIR = PROJECT_ROOT / "01_exploration_eda"
FIGURES_DIR = EDA_DIR / "figures"
TABLES_DIR = EDA_DIR / "tables"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

LABEL_NAMES = {
    0: "Benign",
    1: "Malicious"
}

print("=" * 65)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 65)


# ============================================================
# 2. CHARGEMENT DES DONNEES
# ============================================================

datasets = {}

for config in ["core", "full"]:

    datasets[config] = {}

    for split in ["train", "validation", "test"]:

        file_path = DATA_DIR / config / f"{split}.parquet"

        df = pd.read_parquet(file_path)

        # Calcul de la longueur des textes pour l'analyse.
        # Cette colonne est ajoutée uniquement en mémoire.
        df["text_length"] = df["text"].str.len()

        datasets[config][split] = df

        print(f"{config.upper()}/{split} : {len(df)} exemples chargés")


# ============================================================
# 3. DISTRIBUTION DES LABELS
# ============================================================

print("\n[1] ANALYSE DES LABELS")

label_results = []

for config in ["core", "full"]:

    for split in ["train", "validation", "test"]:

        df = datasets[config][split]

        counts = df["label"].value_counts().sort_index()

        for label, count in counts.items():

            percentage = count / len(df) * 100

            label_results.append({
                "configuration": config,
                "split": split,
                "label": int(label),
                "classe": LABEL_NAMES[int(label)],
                "nombre": int(count),
                "pourcentage": round(percentage, 2)
            })

label_summary = pd.DataFrame(label_results)

label_summary.to_csv(
    TABLES_DIR / "label_summary.csv",
    index=False
)

print(label_summary.to_string(index=False))


# Graphique : comparaison des labels sur les ensembles train.

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, config in zip(axes, ["core", "full"]):

    df = datasets[config]["train"]

    sns.countplot(
        data=df,
        x="label",
        hue="label",
        order=[0, 1],
        palette="Set2",
        legend=False,
        ax=ax
    )

    ax.set_title(f"Distribution des labels - {config.upper()}")
    ax.set_xlabel("Classe")
    ax.set_ylabel("Nombre d'exemples")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Benign (0)", "Malicious (1)"])

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "label_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 4. DISTRIBUTION DES CATEGORIES
# ============================================================

print("\n[2] ANALYSE DES CATEGORIES")

core_train = datasets["core"]["train"]

category_summary = (
    core_train["category"]
    .value_counts()
    .rename_axis("categorie")
    .reset_index(name="nombre")
)

category_summary["pourcentage"] = (
    category_summary["nombre"] / len(core_train) * 100
).round(2)

category_summary.to_csv(
    TABLES_DIR / "category_summary.csv",
    index=False
)

print(category_summary.to_string(index=False))


plt.figure(figsize=(12, 6))

sns.countplot(
    data=core_train,
    y="category",
    hue="category",
    order=category_summary["categorie"],
    palette="viridis",
    legend=False
)

plt.title("Distribution des catégories - CORE/train")
plt.xlabel("Nombre d'exemples")
plt.ylabel("Catégorie")
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "category_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 5. ANALYSE DE LA LONGUEUR DES TEXTES
# ============================================================

print("\n[3] ANALYSE DE LA LONGUEUR DES TEXTES")

length_results = []

for config in ["core", "full"]:

    df = datasets[config]["train"]

    length_results.append({
        "configuration": config,
        "nombre": len(df),
        "minimum": int(df["text_length"].min()),
        "maximum": int(df["text_length"].max()),
        "moyenne": round(df["text_length"].mean(), 2),
        "mediane": round(df["text_length"].median(), 2),
        "ecart_type": round(df["text_length"].std(), 2)
    })

length_summary = pd.DataFrame(length_results)

length_summary.to_csv(
    TABLES_DIR / "text_length_summary.csv",
    index=False
)

print(length_summary.to_string(index=False))


# Histogramme : longueur des textes.

plt.figure(figsize=(12, 6))

for config in ["core", "full"]:

    df = datasets[config]["train"]

    sns.histplot(
        data=df,
        x="text_length",
        bins=50,
        element="step",
        stat="density",
        common_norm=False,
        label=config.upper(),
        alpha=0.35
    )

plt.title("Distribution de la longueur des textes")
plt.xlabel("Nombre de caractères")
plt.ylabel("Densité")
plt.legend()
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "text_length_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 6. DISTRIBUTION DE LA SEVERITE
# ============================================================

print("\n[4] ANALYSE DE LA SEVERITE")

# Copie pour ne pas modifier le DataFrame chargé.
severity_df = core_train.copy()

# Les chaînes vides sont représentées par "Non renseignée".
severity_df["severity"] = (
    severity_df["severity"]
    .replace("", "Non renseignée")
    .fillna("Non renseignée")
)

severity_summary = (
    severity_df["severity"]
    .value_counts()
    .rename_axis("severite")
    .reset_index(name="nombre")
)

print(severity_summary.to_string(index=False))


plt.figure(figsize=(10, 5))

sns.countplot(
    data=severity_df,
    x="severity",
    hue="severity",
    order=severity_summary["severite"],
    palette="magma",
    legend=False
)

plt.title("Distribution des niveaux de sévérité - CORE/train")
plt.xlabel("Niveau de sévérité")
plt.ylabel("Nombre d'exemples")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "severity_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 7. COMPARAISON CORE / FULL
# ============================================================

print("\n[5] COMPARAISON CORE / FULL")

comparison = []

for config in ["core", "full"]:

    df = datasets[config]["train"]

    malicious = int((df["label"] == 1).sum())
    benign = int((df["label"] == 0).sum())

    comparison.append({
        "configuration": config,
        "total": len(df),
        "benign": benign,
        "malicious": malicious,
        "pourcentage_benign": round(benign / len(df) * 100, 2),
        "pourcentage_malicious": round(malicious / len(df) * 100, 2)
    })

comparison_df = pd.DataFrame(comparison)

print(comparison_df.to_string(index=False))


comparison_plot = comparison_df.melt(
    id_vars="configuration",
    value_vars=["pourcentage_benign", "pourcentage_malicious"],
    var_name="classe",
    value_name="pourcentage"
)

plt.figure(figsize=(9, 5))

sns.barplot(
    data=comparison_plot,
    x="configuration",
    y="pourcentage",
    hue="classe",
    palette="Set2"
)

plt.title("Comparaison des proportions de classes - CORE / FULL")
plt.xlabel("Configuration")
plt.ylabel("Pourcentage (%)")
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "core_vs_full.png",
    dpi=300
)

plt.close()


# ============================================================
# 8. FIN
# ============================================================

print("\n" + "=" * 65)
print("EDA TERMINEE")
print("=" * 65)

print("Graphiques :", FIGURES_DIR)
print("Tableaux :", TABLES_DIR)
