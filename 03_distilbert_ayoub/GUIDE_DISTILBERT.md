# Phase 3 — Fine-tuning de DistilBERT

**Responsable : Ayoub**

**Modèle de départ :** `distilbert-base-uncased`

**Données nécessaires :** le même corpus et les mêmes partitions validés en phase 1 et utilisés pour la baseline.

## Objectif

Fine-tuner un modèle transformer pour classifier les prompts selon la définition de tâche commune, puis exporter ses prédictions de test afin que Taoufik puisse les comparer à la baseline.

## Ce qu'il faut avoir avant de commencer

- Corpus, manifeste et compte rendu EDA finalisés ;
- labels et mapping établis, avec `1` associé à la classe malveillante si c'est le mapping commun retenu ;
- train, validation et test établis avec la stratégie anti-fuite convenue ;
- identifiant stable des exemples ;
- accès au modèle pré-entraîné sur Hugging Face ;
- environnement Python avec les dépendances installées et mémoire suffisante. Le fine-tuning est plus rapide avec un GPU, mais il faut adapter les lots au matériel.

## Suivi pas à pas

### 1. Reprendre exactement le protocole commun

Charger le corpus convenu, vérifier les effectifs et les noms de colonnes, puis confirmer que les identifiants de train/validation/test sont ceux transmis à Taoufik. Ne pas refaire un split aléatoire indépendant : cela empêcherait une comparaison directe et pourrait créer des fuites par groupe.

### 2. Vérifier labels et groupes

Appliquer le mapping documenté en phase 1. Contrôler qu'aucune classe inconnue n'est convertie silencieusement. Vérifier qu'aucun groupe apparenté ne traverse les partitions et que le test reste réservé à l'évaluation finale.

### 3. Choisir le traitement des textes

Charger le tokenizer et le modèle `distilbert-base-uncased` avec une tête de classification à deux classes. Choisir une longueur maximale à partir des longueurs observées en EDA. Mesurer et rapporter la proportion des textes tronqués. Utiliser un padding adapté et préserver le contenu du prompt autant que possible.

### 4. Fixer les paramètres d'entraînement

Avant l'entraînement, consigner nombre d'époques, taille des lots, taux d'apprentissage, graine, stratégie d'évaluation/sauvegarde et métrique de sélection. Enregistrer la version de Transformers/PyTorch, le matériel et les éventuelles contraintes mémoire.

### 5. Entraîner et sélectionner

Entraîner sur train. Utiliser validation pour surveiller le modèle et choisir le meilleur état selon la métrique définie. Noter les courbes ou résultats utiles et les signes de surapprentissage. Le test ne sert pas au réglage.

### 6. Évaluer et exporter

Après avoir figé le modèle, évaluer test avec les mêmes définitions que la baseline : précision, rappel et F1 de la classe malveillante, supports et matrice de confusion. Exporter `example_id`, `y_true`, `y_pred` et si possible `score_malicious` pour chaque exemple test.

### 7. Sauvegarder et passer le relais

Sauvegarder modèle et tokenizer, paramètres, versions, graine et résultats. Transmettre à Taoufik l'export ainsi que la confirmation que les identifiants test correspondent à ceux de la baseline.

## Livrables

1. Fiche d'expérience reproductible avec paramètres et environnement ;
2. poids du modèle et tokenizer sauvegardés localement ;
3. résultats test et analyse des erreurs ;
4. export de prédictions alignable par identifiant avec la baseline ;
5. note sur troncature, temps/matériel et difficultés rencontrées.

## Fichiers à produire dans ce dossier

| Fichier | Contenu attendu | À versionner ? |
|---|---|---|
| `distilbert_experiment.md` | Corpus/split, mapping, longueur maximale et taux de troncature, paramètres, sélection sur validation, graine, versions et matériel. | Oui |
| `distilbert_metrics.json` ou `distilbert_metrics.csv` | Métriques finales et supports, classe positive, ordre des labels et identifiant du test. | Oui, chiffres uniquement |
| `distilbert_test_predictions.csv` | `example_id`, `y_true`, `y_pred`, `score_malicious` si disponible, une ligne par exemple test. | Selon les conditions des données ; ne pas inclure le texte brut sans autorisation |
| `distilbert_confusion_matrix.png` | Matrice de confusion annotée et lisible. | Oui |
| `artifacts/` (local) | Modèle, tokenizer, journaux et checkpoints utiles. | Non si volumineux ; garder localement et ignorer par Git |

Utiliser la même clé `example_id` que la baseline. Ne pas committer les checkpoints ou poids volumineux sans décision du binôme.

## Checklist avant de remettre le travail

- [ ] Le corpus, mapping des labels et split sont les mêmes que ceux de la baseline.
- [ ] Aucun groupe lié ne traverse les partitions.
- [ ] Les paramètres ont été choisis sans consulter le test.
- [ ] La longueur maximale et l'effet de troncature sont documentés.
- [ ] Les métriques et supports suivent la convention commune.
- [ ] L'export comporte une clé stable, `y_true`, `y_pred` et idéalement le score.
- [ ] Modèle, tokenizer, versions et graine sont sauvegardés ou consignés.
