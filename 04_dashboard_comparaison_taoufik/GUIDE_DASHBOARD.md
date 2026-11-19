# Phase 4 — Évaluation comparative et tableau de bord

**Responsable : Taoufik**

**Entrées :** export baseline et export DistilBERT produits en phases 2 et 3.

## Objectif

Comparer les deux détecteurs sur un test commun, expliquer les résultats et rendre les métriques consultables dans un tableau de bord. Cette phase mesure des classifieurs ; elle ne mesure pas à elle seule une protection appliquée à un LLM.

## Ce qu'il faut avoir avant de commencer

- Deux exports avec `example_id`, `y_true`, `y_pred` et, si possible, `score_malicious` ;
- fiches d'expérience et définitions communes des labels/métriques ;
- confirmation du split, du corpus et de la version utilisés par chacun ;
- choix de l'outil de visualisation (Streamlit est prévu dans `requirements.txt`) ;
- environnement avec les dépendances du projet.

## Suivi pas à pas

### 1. Contrôler les fichiers reçus

Vérifier les colonnes, types, lignes vides, valeurs de labels, prédictions manquantes et identifiants dupliqués. Confirmer que chaque fichier correspond au test annoncé et que la classe positive est identique.

### 2. Aligner les prédictions

Joindre les exports par `example_id`, jamais par ordre de ligne. Rapporter combien d'exemples sont communs, manquants ou dupliqués. Pour chaque identifiant commun, comparer `y_true`. Si les labels réels divergent, suspendre la comparaison jusqu'à correction du mapping ou du corpus.

### 3. Définir le périmètre de comparaison

Si les deux modèles ont exactement les mêmes exemples test, comparer sur cet ensemble. S'ils diffèrent, utiliser un sous-ensemble commun seulement si sa construction reste valide et documenter l'exclusion ; sinon présenter deux évaluations séparées. Afficher le support associé à chaque métrique.

### 4. Calculer les métriques

Pour chacun des modèles, calculer précision, rappel et F1 pour la classe malveillante, supports par classe et matrice de confusion. Indiquer la classe positive, l'ordre des axes et les conventions de calcul. Ne pas comparer une moyenne macro pour un modèle avec une moyenne binaire pour l'autre.

### 5. Analyser les résultats

Comparer les métriques et examiner des exemples de faux négatifs et faux positifs. Si les catégories ou sources sont conservées, examiner aussi les résultats par groupe/source sans tirer de conclusions sur des sous-groupes trop petits. Protéger ou masquer les prompts dans une présentation publique.

### 6. Construire le tableau de bord

Prévoir au minimum : résumé du protocole et du nombre d'exemples, tableau des scores, matrices de confusion, comparaison visuelle et accès aux erreurs représentatives. Indiquer où déposer les exports et comment lancer le tableau de bord. Les détails d'implémentation seront écrits dans le code au moment de cette phase ; ce dépôt reste un guide, pas un script.

### 7. Transmettre les résultats

Fournir à Ayoub les métriques consolidées, figures exportées, définition du périmètre, supports, exclusions et quelques constats d'erreurs pour le rapport.

## Attention à la formulation « avant/après protection »

Ne pas appeler la comparaison « avant/après protection » sauf si une défense réelle a été appliquée et évaluée avec un protocole dédié. Pour le projet actuel, nommer les vues **Baseline vs DistilBERT**.

## Livrables

1. Tableau de métriques avec supports et protocole ;
2. matrices de confusion et graphiques comparatifs ;
3. tableau de bord exécutable et consignes de lancement ;
4. note de comparabilité, erreurs observées et limites ;
5. synthèse remise à Ayoub pour le rapport final.

## Fichiers à produire dans ce dossier

| Fichier | Contenu attendu | À versionner ? |
|---|---|---|
| `comparison_protocol.md` | Sources des exports, split, règle d'alignement, exclusions, définition des métriques et limites de comparaison. | Oui |
| `comparison_results.csv` | Résultats consolidés : métriques, supports, modèles et périmètre test. | Oui |
| `comparison_summary.png` | Graphique comparatif avec noms des modèles et supports visibles. | Oui |
| `confusion_matrix_baseline.png` et `confusion_matrix_distilbert.png` | Matrices annotées avec axes et ordre des classes. | Oui |
| `dashboard/` | Application de visualisation et consignes d'utilisation. Le code sera créé durant cette phase. | Oui, hors données privées et secrets |
| `inputs/` (local) | Exports de prédictions utilisés par le tableau de bord. | Garder localement si les conditions des données l'exigent |

Le tableau de bord doit pouvoir être relancé avec les exports attendus. Ne pas intégrer de clés d'accès, prompts soumis à restriction ou copies du corpus dans son dossier.

## Checklist avant de remettre le travail

- [x] L'application web interactive Streamlit (`app.py`) a été développée et fonctionne avec ses 5 pages.
- [ ] Les exports ont été contrôlés et joints par identifiant stable via `compare_models.py`.
- [ ] Les labels réels concordent sur les exemples comparés.
- [ ] Même classe positive, même convention métrique, supports affichés.
- [ ] Les différences de corpus/split et exclusions sont visibles.
- [ ] Les matrices de confusion ont des axes et classes clairement nommés.
- [ ] Les captures d'écran et métriques consolidées sont déposées dans `05_rapport_final_ayoub/`.
- [ ] L'analyse présente des erreurs, pas seulement les scores agrégés.
- [ ] Le tableau de bord et ses instructions ont été transmis à Ayoub.
