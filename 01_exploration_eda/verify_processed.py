from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. CHEMINS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data_processed"

EXPECTED_ROWS = {
    "core": {
        "train": 4391,
        "validation": 941,
        "test": 942
    },
    "full": {
        "train": 13934,
        "validation": 941,
        "test": 942
    }
}

splits = ["train", "validation", "test"]
configs = ["core", "full"]

print("=" * 65)
print("VERIFICATION DES DONNEES PREPAREES")
print("=" * 65)

datasets = {}

# --------------------------------------------------
# 2. VERIFIER LES SIX FICHIERS
# --------------------------------------------------

for config in configs:

    datasets[config] = {}

    for split in splits:

        file_path = DATA_DIR / config / f"{split}.parquet"

        if not file_path.exists():
            raise FileNotFoundError(f"Fichier absent : {file_path}")

        df = pd.read_parquet(file_path)
        datasets[config][split] = df

        expected = EXPECTED_ROWS[config][split]

        print(f"\n{config.upper()}/{split}")
        print("Nombre de lignes :", len(df))
        print("Nombre attendu :", expected)

        if len(df) != expected:
            raise ValueError(
                f"Nombre de lignes incorrect dans {config}/{split}"
            )

        # Vérifier les valeurs manquantes.
        missing = int(df.isna().sum().sum())
        print("Valeurs manquantes :", missing)

        if missing != 0:
            raise ValueError(
                f"Valeurs manquantes détectées dans {config}/{split}"
            )

        # Vérifier les labels.
        labels = set(df["label"].unique())
        print("Labels présents :", sorted(labels))

        if not labels.issubset({0, 1}) or labels != {0, 1}:
            raise ValueError(
                f"Labels inattendus dans {config}/{split}"
            )

# --------------------------------------------------
# 3. VERIFIER LES DOUBLONS DANS FULL/TRAIN
# --------------------------------------------------

full_train = datasets["full"]["train"]

duplicate_count = int(
    full_train.duplicated(subset=["text"]).sum()
)

print("\n" + "=" * 65)
print("VERIFICATION DES DOUBLONS")
print("=" * 65)

print("Textes dupliqués dans FULL/train :", duplicate_count)

if duplicate_count != 0:
    raise ValueError("Des textes dupliqués subsistent dans FULL/train")

# --------------------------------------------------
# 4. VERIFIER LES CHEVAUCHEMENTS ENTRE LES SPLITS
# --------------------------------------------------

print("\n" + "=" * 65)
print("VERIFICATION DES CHEVAUCHEMENTS")
print("=" * 65)

for config in configs:

    train = datasets[config]["train"]
    validation = datasets[config]["validation"]
    test = datasets[config]["test"]

    train_groups = set(train["group_id"])
    validation_groups = set(validation["group_id"])
    test_groups = set(test["group_id"])

    overlaps = {
        "train / validation": len(train_groups & validation_groups),
        "train / test": len(train_groups & test_groups),
        "validation / test": len(validation_groups & test_groups)
    }

    print(f"\n{config.upper()}")

    for name, count in overlaps.items():
        print(f"{name} : {count}")

        if count != 0:
            raise ValueError(
                f"Chevauchement détecté dans {config} : {name}"
            )

# --------------------------------------------------
# 5. BILAN
# --------------------------------------------------

print("\n" + "=" * 65)
print("TOUTES LES VERIFICATIONS SONT REUSSIES")
print("=" * 65)
