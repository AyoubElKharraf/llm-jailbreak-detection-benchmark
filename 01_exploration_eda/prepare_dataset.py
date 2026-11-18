from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. CHEMINS DU PROJET
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REVISION = "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75"

RAW_DIR = PROJECT_ROOT / "data_local" / "neuralchemy" / REVISION
OUTPUT_DIR = PROJECT_ROOT / "data_processed"

# --------------------------------------------------
# 2. CREATION DU DOSSIER DE SORTIE
# --------------------------------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 65)
print("PREPARATION DU DATASET")
print("=" * 65)


# --------------------------------------------------
# 3. COPIE DES DONNEES CORE
# --------------------------------------------------

for split in ["train", "validation", "test"]:

    input_file = RAW_DIR / "core" / f"{split}.parquet"
    output_folder = OUTPUT_DIR / "core"
    output_folder.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(input_file)

    output_file = output_folder / f"{split}.parquet"
    df.to_parquet(output_file, index=False)

    print(f"CORE/{split} : {len(df)} exemples conservés")


# --------------------------------------------------
# 4. PREPARATION DES DONNEES FULL
# --------------------------------------------------

for split in ["train", "validation", "test"]:

    input_file = RAW_DIR / "full" / f"{split}.parquet"
    output_folder = OUTPUT_DIR / "full"
    output_folder.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(input_file)

    original_count = len(df)
    removed_count = 0

    # On nettoie uniquement le train.
    if split == "train":

        # Identifier les textes apparaissant plusieurs fois.
        duplicated = df[df.duplicated(subset=["text"], keep=False)]

        # Vérifier chaque groupe de textes dupliqués.
        for text_value, group in duplicated.groupby("text", sort=False):

            valid_pair = (
                len(group) == 2
                and set(group["augmented"].tolist()) == {False, True}
                and group["label"].nunique() == 1
                and group["group_id"].nunique() == 1
            )

            if not valid_pair:
                raise ValueError(
                    "Doublon inattendu détecté. "
                    "Arrêt du nettoyage pour éviter une suppression incorrecte."
                )

        # Supprimer uniquement les copies augmentées exactes.
        duplicated_texts = duplicated["text"].unique()

        mask_to_remove = (
            df["augmented"]
            & df["text"].isin(duplicated_texts)
        )

        removed_count = int(mask_to_remove.sum())

        df = df.loc[~mask_to_remove].copy()

        print("\nAudit des doublons FULL/train :")
        print("Textes dupliqués vérifiés :", len(duplicated_texts))
        print("Copies augmentées supprimées :", removed_count)

    # Enregistrer les données préparées.
    output_file = output_folder / f"{split}.parquet"
    df.to_parquet(output_file, index=False)

    print(
        f"FULL/{split} : {original_count} -> {len(df)} exemples "
        f"({removed_count} supprimés)"
    )


# --------------------------------------------------
# 5. FIN
# --------------------------------------------------

print("\n" + "=" * 65)
print("PREPARATION TERMINEE")
print("Dossier de sortie :", OUTPUT_DIR)
print("=" * 65)
