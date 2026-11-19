# Guide des Commandes d'Exécution du Projet

Ce document récapitule **toutes les commandes prêtes à l'emploi** pour exécuter les différentes composantes du projet : interface web Streamlit, scripts d'entraînement, vérifications des données et tests.

---

## 🚀 1. Lancer l'Application Web Interactive (Streamlit)

L'interface web permet de visualiser le benchmark, inspecter les attaques/erreurs et tester en direct le filtre sur des prompts.

### 👉 Option A : Depuis l'Invite de Commandes Windows classique (`cmd.exe`)
Ouvrez votre terminal `cmd` à la racine du projet et exécutez :
```cmd
"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m streamlit run "04_dashboard_comparaison_taoufik/app.py"
```

### 👉 Option B : Depuis PowerShell
Ouvrez PowerShell à la racine du projet et exécutez :
```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m streamlit run "04_dashboard_comparaison_taoufik/app.py"
```

### 👉 Option C : Si votre environnement virtuel `.venv` est activé
```bash
streamlit run 04_dashboard_comparaison_taoufik/app.py
```

*Une fois lancée, l'application s'ouvre automatiquement dans votre navigateur à l'adresse :*  
👉 **`http://localhost:8501`**

---

## 🔬 2. Entraînement et Modélisation

### Phase 2 : Entraîner la Baseline TF-IDF + Régression Logistique (Taoufik)
```powershell
python 02_baseline_taoufik/train_baseline.py
```
*(Utilise les données `data_processed/core/` et exporte les résultats dans `02_baseline_taoufik/`).*

### Phase 3 : Entraîner DistilBERT (Ayoub)
- **Option Recommandée (GPU Gratuit) :**  
  Ouvrir et exécuter le notebook sur Google Colab :  
  `03_distilbert_ayoub/phase03_distilbert_colab_training.ipynb`
- **Option Locale (CPU ou GPU CUDA local) :**
  ```powershell
  python 03_distilbert_ayoub/train_distilbert.py
  ```

---

## 📊 3. Phase 1 — Exploration et Préparation des Données (Audit EDA)

### Télécharger le dataset brut depuis Hugging Face :
```powershell
python 01_exploration_eda/download_dataset.py
```

### Préparer et nettoyer les données (déduplication des 102 doublons exacts) :
```powershell
python 01_exploration_eda/prepare_dataset.py
```

### Générer les figures et tables de l'EDA :
```powershell
python 01_exploration_eda/eda_analysis.py
```

### Vérifier l'intégrité des splits et de la configuration `core` vs `full` :
```powershell
python 01_exploration_eda/verify_processed.py
python 01_exploration_eda/verify_core_full.py
```

---

## 📦 4. Gestion de l'Environnement et Dépendances

### Activer l'environnement virtuel local :
- **PowerShell :**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Invite de commande (`cmd`) :**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

### Installer ou mettre à jour les dépendances du projet :
```powershell
pip install -r requirements.txt
```
