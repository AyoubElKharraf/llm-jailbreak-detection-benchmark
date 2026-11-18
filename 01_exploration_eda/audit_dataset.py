
from pathlib import Path

import pandas as pd

# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REVISION = "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75"

DATA_DIR = PROJECT_ROOT / "data_local" / "neuralchemy" / REVISION

CONFIGS = ["core", "full"]
SPLITS = ["train", "validation", "test"]


# --------------------------------------------------
# 2. CHARGEMENT DES DONNEES
# --------------------------------------------------

def load_dataset(config, split):

    path = DATA_DIR / config / f"{split}.parquet"

    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    return pd.read_parquet(path)


# --------------------------------------------------
# 3. AUDIT DES TEXTES DUPLIQUES
# --------------------------------------------------

def audit_duplicates():

    print("\n" + "=" * 70)
    print("1. AUDIT DES TEXTES DUPLIQUES")
    print("=" * 70)

    df = load_dataset("full", "train")

    duplicates = df[df["text"].duplicated(keep=False)]

    print(f"Nombre de lignes concernées : {len(duplicates)}")
    print(f"Nombre de textes distincts concernés : {duplicates['text'].nunique()}")

    if not duplicates.empty:

        print("\nExemples de textes dupliqués :")

        for text, group in duplicates.groupby("text"):

            print("\n----------------------------------------")
            print("Texte :", text[:200].replace("\n", " "))
            print("Nombre d'occurrences :", len(group))
            print("Labels :", group["label"].tolist())
            print("Groupes :", group["group_id"].tolist())
            print("Augmented :", group["augmented"].tolist())

            if group["label"].nunique() > 1:
                print("ALERTE : labels contradictoires !")


# --------------------------------------------------
# 4. COHERENCE LABEL / CATEGORY
# --------------------------------------------------

def audit_labels():

    print("\n" + "=" * 70)
    print("2. COHERENCE ENTRE LABEL ET CATEGORY")
    print("=" * 70)

    for config in CONFIGS:

        df = load_dataset(config, "train")

        print(f"\nConfiguration : {config.upper()}")

        print(pd.crosstab(
            df["category"],
            df["label"],
            margins=True
        ).to_string())


# --------------------------------------------------
# 5. VALEURS VIDES DE SEVERITY
# --------------------------------------------------

def audit_severity():

    print("\n" + "=" * 70)
    print("3. AUDIT DE SEVERITY")
    print("=" * 70)

    for config in CONFIGS:

        df = load_dataset(config, "train")

        empty = df["severity"].astype("string").str.strip().eq("")

        print(f"\nConfiguration : {config.upper()}")

        print("Valeurs vides :", empty.sum())

        print("\nRépartition des labels pour severity vide :")
        print(df.loc[empty, "label"].value_counts().to_string())

        print("\nRépartition des labels pour severity renseignée :")
        print(df.loc[~empty, "label"].value_counts().to_string())


# --------------------------------------------------
# 6. CHEVAUCHEMENT DES GROUP_ID
# --------------------------------------------------

def audit_group_overlap():

    print("\n" + "=" * 70)
    print("4. CHEVAUCHEMENT DES GROUP_ID ENTRE SPLITS")
    print("=" * 70)

    for config in CONFIGS:

        print(f"\nConfiguration : {config.upper()}")

        datasets = {
            split: load_dataset(config, split)
            for split in SPLITS
        }

        for i, split_a in enumerate(SPLITS):

            for split_b in SPLITS[i + 1:]:

                groups_a = set(datasets[split_a]["group_id"])
                groups_b = set(datasets[split_b]["group_id"])

                overlap = groups_a.intersection(groups_b)

                print(
                    f"{split_a} / {split_b} : "
                    f"{len(overlap)} groupes communs"
                )


# --------------------------------------------------
# 7. CHEVAUCHEMENT DES TEXTES
# --------------------------------------------------

def audit_text_overlap():

    print("\n" + "=" * 70)
    print("5. CHEVAUCHEMENT DES TEXTES ENTRE SPLITS")
    print("=" * 70)

    for config in CONFIGS:

        print(f"\nConfiguration : {config.upper()}")

        datasets = {
            split: load_dataset(config, split)
            for split in SPLITS
        }

        for i, split_a in enumerate(SPLITS):

            for split_b in SPLITS[i + 1:]:

                texts_a = set(datasets[split_a]["text"])
                texts_b = set(datasets[split_b]["text"])

                overlap = texts_a.intersection(texts_b)

                print(
                    f"{split_a} / {split_b} : "
                    f"{len(overlap)} textes communs"
                )


# --------------------------------------------------
# 8. COMPARAISON CORE / FULL
# --------------------------------------------------

def audit_core_full():

    print("\n" + "=" * 70)
    print("6. COMPARAISON CORE / FULL")
    print("=" * 70)

    for split in SPLITS:

        core = load_dataset("core", split)
        full = load_dataset("full", split)

        print(f"\nSplit : {split.upper()}")

        print("Core :", len(core), "exemples")
        print("Full :", len(full), "exemples")

        same_texts = (
            core["text"].reset_index(drop=True)
            .equals(full["text"].reset_index(drop=True))
        )

        print("Textes identiques dans le même ordre :", same_texts)


# --------------------------------------------------
# 9. EXECUTION
# --------------------------------------------------

def main():

    audit_duplicates()
    audit_labels()
    audit_severity()
    audit_group_overlap()
    audit_text_overlap()
    audit_core_full()

    print("\n" + "=" * 70)
    print("AUDIT TERMINE")
    print("=" * 70)


if __name__ == "__main__":
    main()

