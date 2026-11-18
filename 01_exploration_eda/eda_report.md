# Rapport d'Exploration et d'Audit des Données (EDA) — Phase 1

**Auteur de l'audit et de l'EDA :** Mansouri Taoufik  
**Validation de source préalable :** Ayoub El Kharraf  
**Dataset source :** [`neuralchemy/Prompt-injection-dataset`](https://huggingface.co/datasets/neuralchemy/Prompt-injection-dataset)  
**Révision figée :** `7d70432dfcf47a821612cbf9d34e9d9e3ad20e75`  
**Date :** 18 novembre 2026  
**Statut :** Validé — Feu vert (« GO ») pour le passage en Phase 2 (Baseline) et Phase 3 (DistilBERT)

---

## 1. Objectifs de la Phase 1 et Cadrage

L'objectif de cette première phase était d'auditer en profondeur les configurations `core` et `full` du dataset `neuralchemy/Prompt-injection-dataset`, de vérifier l'intégrité des splits, l'absence de fuite de données (*data leakage*) via les groupes d'exemples liés (`group_id`), et de garantir une base saine et équitable pour la comparaison des modèles.

### Décisions méthodologiques arrêtées
1. **Tâche :** Classification binaire de sécurité des prompts LLM.
2. **Mapping des classes :**
   * `0` : **Bénin** (requête utilisateur normale / sans intention malveillante).
   * `1` : **Malveillant** (Prompt Injection directe/indirecte ou Jailbreak).
3. **Configurations :**
   * `core` : Données originales sans augmentation pour la **Baseline classique** (TF-IDF + Régression Logistique).
   * `full` : Données enrichies par augmentation pour le **Transformer** (DistilBERT).
4. **Comparabilité des tests :** Les sous-ensembles de validation et de test sont strictement identiques entre `core` et `full` (mêmes tailles, mêmes identifiants/textes et mêmes labels).

---

## 2. Audit d'Intégrité et Nettoyage des Données (`data_processed/`)

L'audit local a été conduit sur les fichiers Parquet téléchargés et vérifiés par SHA-256.

### 2.1 Synthèse des effectifs

| Configuration | Split | Effectif Brut | Effectif Nettoyé (`data_processed`) | Observations |
|---|---|---:|---:|---|
| `core` | train | 4 391 | 4 391 | Données brutes originales |
| `core` | validation | 941 | 941 | Données d'évaluation de référence |
| `core` | test | 942 | 942 | Partition finale de test |
| `full` | train | 14 036 | **13 934** | **-102 copies augmentées exactes supprimées** |
| `full` | validation | 941 | 941 | Identique à `core/validation` |
| `full` | test | 942 | 942 | Identique à `core/test` |

### 2.2 Justification de la déduplication de `full/train` (102 doublons)
Lors de l'inspection de `full/train`, **102 paires d'exemples** ont été détectées où un texte marqué comme augmenté (`augmented=True`) était strictement identique mot pour mot au texte d'origine (`augmented=False`), avec le même `label` et le même `group_id`.
* **Décision retenue :** Dans le script [prepare_dataset.py](file:///c:/Users/DELL/Documents/Master/Master_M2I/SEMESTRE%203/Module%204%20-%20Cybersécurité%20CEH/Projet/llm-jailbreak-detection-benchmark/01_exploration_eda/prepare_dataset.py), ces 102 copies redondantes ont été retirées du jeu d'entraînement `full` (passant de 14 036 à **13 934** lignes).
* **Impact :** Cela élimine tout risque de surpondération artificielle de ces 102 prompts lors du fine-tuning de DistilBERT, garantissant un apprentissage plus robuste.

### 2.3 Contrôle des fuites (*Data Leakage*)
* **Chevauchement `group_id` :** Zéro chevauchement de `group_id` entre `train`, `validation` et `test` (que ce soit pour `core` ou `full`).
* **Textes vides ou nuls :** Aucun texte nul ou vide (longueur minimale observée : 10 caractères).
* **Fuite train/test :** Les textes de test sont totalement absents des partitions train.

---

## 3. Analyse Exploratoire des Données (EDA)

Les visualisations générées se trouvent dans le répertoire [figures/](file:///c:/Users/DELL/Documents/Master/Master_M2I/SEMESTRE%203/Module%204%20-%20Cybersécurité%20CEH/Projet/llm-jailbreak-detection-benchmark/01_exploration_eda/figures) et les statistiques détaillées dans [tables/](file:///c:/Users/DELL/Documents/Master/Master_M2I/SEMESTRE%203/Module%204%20-%20Cybersécurité%20CEH/Projet/llm-jailbreak-detection-benchmark/01_exploration_eda/tables).

### 3.1 Distribution des Labels (Bénin vs Malveillant)

D'après `tables/label_summary.csv` :
- **Dans `core` :**
  * `train` : 39,65 % Bénins (1 741) vs 60,35 % Malveillants (2 650).
  * `validation` : 43,25 % Bénins (407) vs 56,75 % Malveillants (534).
  * `test` : 41,40 % Bénins (390) vs 58,60 % Malveillants (552).
- **Dans `full` :**
  * `train` : 37,00 % Bénins (5 156) vs 63,00 % Malveillants (8 778).
  * `validation` et `test` : proportions strictement identiques à `core`.

> **Constat :** Le jeu de données présente un léger déséquilibre en faveur de la classe malveillante (~60/40), qui reste modéré et stable entre les différents splits.

### 3.2 Typologie des Attaques et Catégories

D'après `tables/category_summary.csv`, les données couvrent un large spectre de requêtes :
- **Bénin :** 38,69 % (1 699 requêtes dans `core/train`).
- **Attaques directes / Injection :** `direct_injection` représente la majorité des attaques (31,82 %, 1 397 requêtes), suivies de `adversarial` (8,72 %) et `jailbreak` (6,63 %).
- **Techniques sophistiquées :** `encoding` (4,03 %), `training_extraction` (1,55 %), `token_smuggling`, `rag_poisoning`, `persona_replacement`, `agent_manipulation`, `system_manipulation`, `crescendo`, `many_shot`, etc.

Cette diversité garantit que le benchmark évaluera la capacité des modèles à détecter aussi bien des injections directes simples que des techniques d'obfuscation et d'évasion complexes.

### 3.3 Analyse de Longueur des Textes

D'après `tables/text_length_summary.csv` :
- **Configuration `core` :**
  * Minimum : 10 caractères
  * Médiane : 56 caractères
  * Moyenne : 142,98 caractères (Écart-type : 364,36)
  * Maximum : 7 009 caractères
- **Configuration `full` :**
  * Minimum : 10 caractères
  * Médiane : 59 caractères
  * Moyenne : 149,82 caractères (Écart-type : 370,13)
  * Maximum : 7 009 caractères

> **Conséquence pour la modélisation :**
> - Pour la **Baseline TF-IDF**, une tokenisation avec n-grammes (1-2) et conservation des caractères de ponctuation/spéciaux sera adaptée.
> - Pour **DistilBERT**, la majorité des textes est courte (médiane ~59 car.), mais la présence de textes longs (> 7 000 car.) impose de fixer une longueur maximale de tokenisation raisonnable (`max_length=512`) avec troncature, ce qui couvrira une très large majorité des tokens utiles.

---

## 4. Décision de Clôture et Passage de Relais

### Checklist de fin de Phase 1 :
- [x] Téléchargement et intégrité SHA-256 validés.
- [x] Schéma, colonnes et mapping binaire (`0` = Bénin, `1` = Malveillant) confirmés.
- [x] Absence de fuite (`group_id`) entre train, validation et test confirmée.
- [x] Égalité stricte des multisets `test` et `validation` entre `core` et `full` vérifiée.
- [x] Nettoyage des 102 doublons redondants consigné et appliqué dans `data_processed/`.
- [x] Tables et figures de l'EDA générées et sauvegardées.
- [x] Fichier de rapport EDA (`eda_report.md`) finalisé.

### Autorisation de passage :
**Statut : VALIDÉ (GO)**  
Le projet peut maintenant entrer en **Phase 2 (Baseline TF-IDF par Taoufik)** et en **Phase 3 (Fine-tuning DistilBERT par Ayoub)** en utilisant les données stabilisées sous [data_processed/](file:///c:/Users/DELL/Documents/Master/Master_M2I/SEMESTRE%203/Module%204%20-%20Cybersécurité%20CEH/Projet/llm-jailbreak-detection-benchmark/data_processed).

