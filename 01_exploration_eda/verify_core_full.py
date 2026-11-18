from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REVISION = "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75"

DATA_DIR = PROJECT_ROOT / "data_local" / "neuralchemy" / REVISION

# Charger les données
core = pd.read_parquet(DATA_DIR / "core" / "train.parquet")
full = pd.read_parquet(DATA_DIR / "full" / "train.parquet")

# Garder uniquement les exemples originaux de FULL
full_original = full[full["augmented"] == False].copy()

print("=" * 60)
print("VERIFICATION CORE / FULL")
print("=" * 60)

print("Nombre d'exemples CORE :", len(core))
print("Nombre d'exemples originaux FULL :", len(full_original))

# Comparer les identifiants de groupes
groups_core = set(core["group_id"])
groups_full = set(full_original["group_id"])

print("\nGroupes identiques :", groups_core == groups_full)
print("Groupes manquants dans FULL :", len(groups_core - groups_full))
print("Groupes supplémentaires dans FULL :", len(groups_full - groups_core))

# Comparer les contenus en utilisant group_id comme identifiant
columns = ["text", "label", "category", "source", "severity"]

core_indexed = core.set_index("group_id")[columns].sort_index()
full_indexed = full_original.set_index("group_id")[columns].sort_index()

print("\nComparaison des colonnes :")

for column in columns:
    identical = core_indexed[column].equals(full_indexed[column])
    print(f"{column:<15} : {identical}")

print("\n" + "=" * 60)
print("VERIFICATION TERMINEE")
print("=" * 60)
