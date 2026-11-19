# Guide de Suivi et Protocole d'Exécution — Phase 4 (Taoufik)

Ce document sert de **feuille de route détaillée** pour Taoufik (ou tout agent d'assistance qui l'accompagne) afin de finaliser la Phase 4 : la comparaison statistique et le branchement complet des prédictions Baseline dans l'interface web.

---

## 📌 ÉTAT D'AVANCEMENT ACTUEL DU PROJET (Point de Situation)
1. **Phase 1 (EDA & Données) :** 100 % terminée (`data_processed/` est prêt et nettoyé).
2. **Phase 3 (DistilBERT Ayoub) :** 100 % terminée (F1: 96,84 %, AUC: 99,55 %). Les prédictions officielles sont stockées dans `03_distilbert_ayoub/distilbert_test_predictions.csv`.
3. **Phase 4 (Application Web Streamlit) :** **L'APPLICATION EST DÉJÀ DÉVELOPPÉE ET PRÊTE !**
   - Le code complet de l'interface se trouve dans `04_dashboard_comparaison_taoufik/app.py`.
   - Elle inclut déjà : la présentation du projet, le benchmark comparatif, l'analyse forensique des erreurs/attaques, le démonstrateur interactif en direct (Live Playground) et les recommandations de sécurité.

---

## 🎯 CE QUI RESTE À FAIRE PAR TAOUFIK DANS CETTE PHASE

Taoufik a uniquement **deux actions précises** à réaliser pour que tout soit 100 % complet et branché sans conflit :

### Action 1 : Finaliser sa Baseline (Phase 2)
Taoufik doit exécuter l'entraînement de sa Baseline TF-IDF + Régression Logistique (voir `02_baseline_taoufik/PROCESS_SUIVI_TAOUFIK.md`) et s'assurer d'exporter :
- `02_baseline_taoufik/baseline_test_predictions.csv` (avec colonnes : `example_id`, `y_true`, `y_pred`, `score_malicious`).
- `02_baseline_taoufik/baseline_metrics.json`.

### Action 2 : Générer le script de consolidation `compare_models.py`
Créer le script `04_dashboard_comparaison_taoufik/compare_models.py` qui :
1. Charge les deux fichiers de prédictions (`baseline_test_predictions.csv` et `distilbert_test_predictions.csv`).
2. Fait la jointure sur `example_id` et vérifie que `y_true` concorde à 100 %.
3. Exporte le fichier de synthèse : `04_dashboard_comparaison_taoufik/comparison_results.csv`.
4. Sauvegarde le graphique comparatif en barres : `04_dashboard_comparaison_taoufik/comparison_summary.png`.

> 💡 **MAGIE DE L'APPLICATION WEB :**
> Dès que Taoufik aura déposé ses fichiers de Phase 2 et Phase 4, **l'application Streamlit `app.py` les chargera automatiquement** en temps réel au prochain rafraîchissement (F5) sans toucher au code de l'interface !

### Action 3 : Captures d'écran et reporting final
1. Lancer l'application web via la commande :
   `"%LOCALAPPDATA%\Programs\Python\Python312\python.exe" -m streamlit run 04_dashboard_comparaison_taoufik/app.py`
2. Prendre des captures d'écran des 4 pages (Accueil, Benchmark, Analyse des erreurs, Démonstrateur en direct).
3. Les déposer dans `05_rapport_final_ayoub/figures/`.
4. Remplir le tableau comparatif dans `05_rapport_final_ayoub/DONNEES_CONSOLIDEES_POUR_RAPPORT.md`.

- [ ] Jointure exacte sur `example_id` entre la baseline et DistilBERT validée.
- [ ] Zéro divergence sur `y_true`.
- [ ] Tableau consolidé `comparison_results.csv` généré.
- [ ] Graphique comparatif `comparison_summary.png` sauvegardé.
- [ ] Application Streamlit fonctionnelle (`streamlit run 04_dashboard_comparaison_taoufik/app.py`).
- [ ] Résultats transmis à Ayoub pour le rapport final (Phase 5).

---

## 4. Prompt d'Accueil pour l'Agent de Taoufik (Phase 4)

Quand Taoufik sera prêt à finaliser la Phase 4 avec son agent, il lui suffira de copier-coller ce prompt :

```text
Bonjour ! Je suis Mansouri Taoufik et je travaille sur la Phase 4 de notre projet de benchmark de sécurité LLM (dossier `04_dashboard_comparaison_taoufik/`).

Voici l'état d'avancement exact :
- Phase 1 (EDA) : Validée et terminée dans `01_exploration_eda/`.
- Phase 3 (DistilBERT par Ayoub) : Terminée avec d'excellents résultats (F1 test: 96,84 %, ROC-AUC: 99,55 %). Ses prédictions sont prêtes dans `03_distilbert_ayoub/distilbert_test_predictions.csv`.
- L'Application Web Streamlit (`app.py`) a déjà été créée par Ayoub dans `04_dashboard_comparaison_taoufik/app.py` et fonctionne parfaitement !

Mon objectif pour clore les Phases 2 et 4 sans conflit est :
1. Finaliser l'entraînement de ma Baseline TF-IDF (Phase 2) et exporter `02_baseline_taoufik/baseline_test_predictions.csv` et `baseline_metrics.json`.
2. Développer le script `04_dashboard_comparaison_taoufik/compare_models.py` pour aligner les 942 exemples de test entre la Baseline et DistilBERT, générer `comparison_results.csv` et le graphique comparatif `comparison_summary.png`.
3. Lancer l'application web Streamlit (`app.py`), vérifier que les métriques de la Baseline s'y intègrent automatiquement, et prendre les captures d'écran des pages pour les mettre dans `05_rapport_final_ayoub/figures/`.
4. Reporter les résultats finaux dans `05_rapport_final_ayoub/DONNEES_CONSOLIDEES_POUR_RAPPORT.md` pour qu'Ayoub puisse finaliser le rapport Phase 5.
Consulte `04_dashboard_comparaison_taoufik/PROCESS_SUIVI_DASHBOARD_TAOUFIK.md` pour respecter l'ordre des tâches.
```

