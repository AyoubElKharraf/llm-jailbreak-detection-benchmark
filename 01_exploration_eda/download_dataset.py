"""Télécharge les fichiers Parquet NeurAlchemy à une révision figée.

Depuis la racine du dépôt :
    python 01_exploration_eda/download_dataset.py

Par défaut, télécharge `core` et `full` dans `data_local/` (ignoré par Git).
Le script n'a besoin que de la bibliothèque standard de Python.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


DATASET_ID = "neuralchemy/Prompt-injection-dataset"
DATASET_REVISION = "7d70432dfcf47a821612cbf9d34e9d9e3ad20e75"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = (
    REPOSITORY_ROOT / "data_local" / "neuralchemy" / DATASET_REVISION
)

# Empreintes et tailles relevées dans l'arbre officiel Hugging Face à REVISION.
FILES = {
    "core": {
        "train": ("core/train-00000-of-00001.parquet", 387456, "c0724f8e00eebb65c001be9ba94291d1608e5da0374012e53dfd4077c5f92558"),
        "validation": ("core/validation-00000-of-00001.parquet", 92943, "bbd417bfd0df1553dd769e814a0b62ca58ad5b1d08d153c90f66937a4af74deb"),
        "test": ("core/test-00000-of-00001.parquet", 94145, "fb5432035fdd8453d61f6593bfe78ee2970403c5ea59959b642a6708e2bef670"),
    },
    "full": {
        "train": ("full/train-00000-of-00001.parquet", 1409838, "47e72340dc1eea05e5a341acad936d3fedee724d205c784d1b6a196093270990"),
        "validation": ("full/validation-00000-of-00001.parquet", 92943, "bbd417bfd0df1553dd769e814a0b62ca58ad5b1d08d153c90f66937a4af74deb"),
        "test": ("full/test-00000-of-00001.parquet", 94145, "fb5432035fdd8453d61f6593bfe78ee2970403c5ea59959b642a6708e2bef670"),
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Télécharge les configs core/full de NeurAlchemy."
    )
    parser.add_argument(
        "--config",
        choices=("core", "full", "both"),
        default="both",
        help="Configuration à télécharger (défaut : both).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Dossier parent des configurations téléchargées.",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_file(relative_path: str, expected_size: int, expected_sha256: str, target: Path) -> None:
    if target.exists():
        if target.stat().st_size != expected_size or sha256_file(target) != expected_sha256:
            raise ValueError(f"Le fichier local existe mais ne correspond pas à la révision attendue : {target}")
        print(f"Déjà téléchargé et vérifié : {target}")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".partial")
    if partial.exists():
        raise FileExistsError(
            f"Téléchargement incomplet présent : {partial}. Vérifiez-le puis supprimez-le manuellement."
        )

    url = (
        f"https://huggingface.co/datasets/{DATASET_ID}/resolve/"
        f"{DATASET_REVISION}/{quote(relative_path, safe='/')}?download=true"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "llm-jailbreak-detection-benchmark/1.0"})
    digest = hashlib.sha256()
    total = 0
    try:
        with urllib.request.urlopen(request, timeout=60) as response, partial.open("wb") as output:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                output.write(block)
                digest.update(block)
                total += len(block)
        if total != expected_size or digest.hexdigest() != expected_sha256:
            raise ValueError(
                f"Vérification échouée pour {relative_path}: "
                f"taille={total}, SHA-256={digest.hexdigest()}"
            )
        os.replace(partial, target)
    except Exception:
        if partial.exists():
            partial.unlink()
        raise
    print(f"Téléchargé et vérifié : {target}")


def main() -> None:
    args = parse_args()
    configs = ("core", "full") if args.config == "both" else (args.config,)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "dataset_id": DATASET_ID,
        "revision": DATASET_REVISION,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "configs": {},
    }

    for config_name in configs:
        config_manifest = {}
        for split_name, (relative_path, size, digest) in FILES[config_name].items():
            target = output_dir / config_name / f"{split_name}.parquet"
            download_file(relative_path, size, digest, target)
            config_manifest[split_name] = {
                "path": str(target.relative_to(output_dir)),
                "bytes": size,
                "sha256": digest,
            }
        manifest["configs"][config_name] = config_manifest

    manifest_path = output_dir / "download_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Manifeste enregistré : {manifest_path}")
    print("Terminé. Le dossier data_local/ n'est pas suivi par Git.")


if __name__ == "__main__":
    main()
