
from pathlib import Path

import pandas as pd
import numpy as np

# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REVISION = "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75"

DATA_DIR = PROJECT_ROOT / "data_local" / "neuralchemy" / REVISION

CONFIGS = ["core", "full"]
SPLITS = ["train", "validation", "test"]

TEXT_CANDIDATES = [
    "text",
    "prompt",
    "behavior",
    "instruction",
    "input",
    "content",
]


# --------------------------------------------------
# 2. IDENTIFIER LA COLONNE TEXTE
# --------------------------------------------------

def find_text_column(df):
    for column in TEXT_CANDIDATES:
        if column in df.columns:
            return column

    return None


# --------------------------------------------------
# 3. INSPECTER UN FICHIER
# --------------------------------------------------

def inspect_file(config, split):

    path = DATA_DIR / config / f"{split}.parquet"

    print("\n" + "=" * 70)
    print(f"CONFIGURATION : {config.upper()} | SPLIT : {split.upper()}")
    print("=" * 70)

    if not path.exists():
        print(f"ERREUR : fichier introuvable : {path}")
        return None

    df = pd.read_parquet(path)

    print(f"\nNombre d'exemples : {len(df)}")
    print(f"Nombre de colonnes : {len(df.columns)}")

    # Structure du dataset
    print("\n--- COLONNES ET TYPES ---")

    for column, dtype in df.dtypes.items():
        print(f"{column:<25} {dtype}")

    # Valeurs manquantes
    print("\n--- VALEURS MANQUANTES ---")

    missing = df.isna().sum()

    for column, count in missing.items():
        percentage = count / len(df) * 100 if len(df) else 0
        print(f"{column:<25} {count:>8} ({percentage:.2f} %)")

    # Distribution des labels
    if "label" in df.columns:

        print("\n--- DISTRIBUTION DES LABELS ---")

        counts = df["label"].value_counts(dropna=False)

        for label, count in counts.items():
            percentage = count / len(df) * 100 if len(df) else 0
            print(f"Label {label}: {count} ({percentage:.2f} %)")

    # Analyse de la colonne texte
    text_column = find_text_column(df)

    if text_column:

        print(f"\n--- ANALYSE DU TEXTE : {text_column} ---")

        text = df[text_column]

        empty = (
            text.isna()
            | text.astype("string").str.strip().eq("").fillna(False)
        )

        print(f"Textes vides : {empty.sum()}")
        print(f"Doublons de texte : {text.duplicated().sum()}")

        lengths = text.dropna().astype(str).str.len()

        if not lengths.empty:
            print(f"Longueur minimale : {lengths.min()}")
            print(f"Longueur maximale : {lengths.max()}")
            print(f"Longueur moyenne : {lengths.mean():.2f}")
            print(f"Médiane : {lengths.median():.2f}")

    else:
        print("\nATTENTION : colonne texte non identifiée automatiquement.")

    # Analyse des métadonnées
    metadata_columns = [
        "category",
        "source",
        "severity",
        "group_id",
        "augmented",
        "tags",
    ]

    print("\n--- MÉTADONNÉES ---")

    for column in metadata_columns:

        if column not in df.columns:
            continue

        print(f"\n{column} :")

        if column == "group_id":
            print(f"Nombre de groupes distincts : {df[column].nunique()}")
            continue

        if column == "tags":
            print(f"Nombre de valeurs manquantes : {df[column].isna().sum()}")
            continue

        print(df[column].value_counts(dropna=False).head(15).to_string())

    # Vérification des doublons de lignes
    print("\n--- DOUBLONS ---")

    df_duplicates = df.copy()

    for column in df_duplicates.columns:
        df_duplicates[column] = df_duplicates[column].map(
            lambda value: repr(value)
            if isinstance(value, (list, dict, set, np.ndarray))
            else value
        )

    duplicate_rows = df_duplicates.duplicated().sum()

    print(f"Lignes entièrement dupliquées : {duplicate_rows}")

    return df


# --------------------------------------------------
# 4. INSPECTER LES SIX FICHIERS
# --------------------------------------------------

def main():

    datasets = {}

    for config in CONFIGS:

        for split in SPLITS:

            df = inspect_file(config, split)

            if df is not None:
                datasets[(config, split)] = df

    print("\n" + "=" * 70)
    print("DIAGNOSTIC TERMINÉ")
    print("=" * 70)

    print(f"Fichiers inspectés : {len(datasets)} / 6")


if __name__ == "__main__":
    main()

