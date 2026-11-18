# Guide de Suivi et Protocole d'Exécution — Phase 4 (Taoufik)

Ce document sert de **feuille de route détaillée** pour Taoufik (ou tout agent d'assistance qui l'accompagne) afin de réaliser la Phase 4 : la comparaison statistique et le développement du tableau de bord Streamlit.

---

## 1. Contexte & Données d'Entrée
- **Responsable :** Mansouri Taoufik
- **Données d'entrée indispensables :**
  1. Prédictions Baseline (produites en Phase 2) : `02_baseline_taoufik/baseline_test_predictions.csv`
  2. Prédictions DistilBERT (produites en Phase 3 par Ayoub) : `03_distilbert_ayoub/distilbert_test_predictions.csv`
  3. Métriques DistilBERT : `03_distilbert_ayoub/distilbert_metrics.json`
  4. Fichier source de test pour analyse par catégorie/longueur : `data_processed/core/test.parquet`
- **Nombre d'exemples de test commun :** 942 exemples (identifiants `test_0000` à `test_0941`).
- **Classe positive :** `1` = Malveillant (Injection / Jailbreak).

---

## 2. Feuille de Route Détaillée (Étapes à Réaliser)

### Étape 1 : Script de Consolidation et de Comparaison (`compare_models.py`)
Créer un script `04_dashboard_comparaison_taoufik/compare_models.py` qui :
1. Charge les deux fichiers de prédictions (`baseline_test_predictions.csv` et `distilbert_test_predictions.csv`).
2. Fait une jointure stricte sur `example_id` et vérifie que `y_true` concorde à 100 %.
3. Calcule et compare les métriques clés :
   - Accuracy, Precision (classe 1), Recall (classe 1), F1-Score (classe 1), Macro F1, ROC-AUC.
4. Exporte le fichier de synthèse : `04_dashboard_comparaison_taoufik/comparison_results.csv`.
5. Génère le graphique comparatif des métriques : `04_dashboard_comparaison_taoufik/comparison_summary.png`.

### Étape 2 : Développement de l'Interface Web Interactive (Streamlit / Web UI)
L'interface web est **l'élément central de démonstration du projet**. Elle doit être développée avec **Streamlit** (déjà présent dans `requirements.txt`) dans `04_dashboard_comparaison_taoufik/app.py` pour offrir une expérience visuelle moderne, dynamique et intuitive :

1. **🎨 Page 1 — Vue d'ensemble & Architecture de Cybersécurité :**
   * Présentation du projet (Master M2I - Module Cybersécurité CEH, Groupe 7).
   * Schéma d'architecture du pare-feu de prompts (*Input Prompt -> Security Detection Layer -> Safe / Unsafe -> LLM*).
   * Cadrage du dataset `neuralchemy/Prompt-injection-dataset` et protocole des 942 tests communs.

2. **📊 Page 2 — Benchmark & Comparaison Graphique Interactive :**
   * Tableaux comparatifs interactifs avec filtres et surbrillance (Baseline TF-IDF vs DistilBERT).
   * KPI Cards : F1-Score, Rappel (détection des attaques), Taux de Faux Positifs, Latence estimée.
   * Graphiques Plotly / Seaborn interactifs : Bar charts comparatifs des métriques, courbes ROC / Precision-Recall.
   * Visualisation côte à côte des deux matrices de confusion annotées.

3. **🔍 Page 3 — Exploration & Analyse Forensique des Erreurs :**
   * Table interactive filtrable de tous les 942 exemples de test avec coloration syntaxique.
   * **Focus Faux Négatifs (Attaques réussies / Évasions) :** Quels prompts ont réussi à tromper la Baseline et/ou DistilBERT ? Filtrage par famille d'attaque (`jailbreak`, `direct_injection`, `encoding`, `crescendo`, `adversarial`, etc.).
   * **Focus Faux Positifs (Requêtes légitimes bloquées) :** Pourquoi certains prompts bénins ont été signalés à tort ?

4. **🛡️ Page 4 — Démonstrateur Live / Simulateur de Pare-Feu LLM (Playground interactif) :**
   * Une boîte de saisie textuelle permettant à un utilisateur ou à l'enseignant de tester en direct n'importe quel prompt.
   * Exécution instantanée des détecteurs avec jauge de risque en couleur (Vert = Bénin / Rouge = Alerte Injection ou Jailbreak).
   * Affichage de la probabilité malveillante (`score_malicious`) et recommandation d'action (Autoriser l'envoi au LLM ou Bloquer avec alerte de sécurité).

### Étape 4 : Reporter toutes les données et captures dans le dossier du Rapport Final (Phase 5)
À la fin de la Phase 4, reporter les résultats consolidés dans le fichier central :
`05_rapport_final_ayoub/DONNEES_CONSOLIDEES_POUR_RAPPORT.md` dans la section dédiée à la **Phase 4**.
Prendre également des captures d'écran soignées de l'application Streamlit (Vue d'ensemble, Métriques comparatives, Analyse des Faux Négatifs, Playground Live) et les déposer dans `05_rapport_final_ayoub/figures/` pour illustrer le rapport final.

---

## 3. Checklist de Validation pour Taoufik (Phase 4)

- [ ] Jointure exacte sur `example_id` entre la baseline et DistilBERT validée.
- [ ] Zéro divergence sur `y_true`.
- [ ] Tableau consolidé `comparison_results.csv` généré.
- [ ] Graphique comparatif `comparison_summary.png` sauvegardé.
- [ ] Application Streamlit fonctionnelle (`streamlit run 04_dashboard_comparaison_taoufik/app.py`).
- [ ] Résultats transmis à Ayoub pour le rapport final (Phase 5).

---

## 4. Prompt d'Accueil pour l'Agent de Taoufik (Phase 4)

Quand Taoufik sera prêt à lancer la Phase 4, il pourra donner ce prompt à son agent :

```text
Bonjour ! Je suis Mansouri Taoufik et je commence à travailler sur la Phase 4 de notre projet de détection de jailbreak LLM (dossier `04_dashboard_comparaison_taoufik/`).
Les phases précédentes sont terminées :
- Phase 1 (EDA) validée dans `01_exploration_eda/`.
- Phase 2 (Baseline) terminée : `02_baseline_taoufik/baseline_test_predictions.csv` et `baseline_metrics.json` sont disponibles.
- Phase 3 (DistilBERT par Ayoub) terminée : `03_distilbert_ayoub/distilbert_test_predictions.csv` et `distilbert_metrics.json` sont disponibles (F1 test: 96,84 %, ROC-AUC: 99,55 %).

Mon objectif pour cette Phase 4 est :
1. Aligner les deux modèles sur le jeu de test commun de 942 exemples via `example_id` et vérifier la concordance des `y_true`.
2. Calculer les métriques comparatives et générer `comparison_results.csv` ainsi que le graphique `comparison_summary.png`.
3. Développer une INTERFACE WEB moderne et interactive avec Streamlit (`app.py`) comprenant :
   - Vue d'ensemble du projet et architecture du pare-feu de prompts LLM.
   - Comparaison visuelle des métriques (tableaux, KPIs, graphiques en barres, matrices de confusion côte à côte).
   - Analyse approfondie des erreurs (filtrage interactif des faux négatifs et faux positifs par catégorie d'attaque).
   - Simulateur / Démonstrateur interactif en direct (Live Playground) permettant de saisir un prompt et de voir instantanément le verdict (Safe vs Unsafe) et la jauge de risque.
4. Remplir `comparison_protocol.md` et fournir la synthèse finale ainsi que les captures d'écran de l'interface web à Ayoub pour la rédaction du rapport Phase 5.
Consulte `04_dashboard_comparaison_taoufik/PROCESS_SUIVI_DASHBOARD_TAOUFIK.md` et `GUIDE_DASHBOARD.md` pour suivre le protocole sans conflit.
```

