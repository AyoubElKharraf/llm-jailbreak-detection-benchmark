# Guide du fine-tuning DistilBERT

**Responsable : Ayoub** — Configuration Hugging Face : `full` ; modèle initial : `distilbert-base-uncased`.

## Objectif et prérequis

Fine-tuner un transformer pour la classification binaire, puis évaluer et exporter ses prédictions. Avant d'entraîner, récupérer le compte rendu EDA et confirmer avec Taoufik les labels, l'identifiant des exemples et les règles de séparation anti-fuite. Vérifier la mémoire disponible : l'entraînement peut être lent sur CPU et les lots doivent être adaptés au GPU/CPU.

## Étapes

1. Charger la configuration `full`. Confirmer les colonnes et splits réels ; ne pas supposer qu'ils sont identiques à `core`.
2. Appliquer le split convenu dans l'EDA. Si `group_id` représente des exemples apparentés, vérifier qu'un groupe ne traverse pas train, validation et test. Garder le test à l'écart du réglage.
3. Définir le mapping explicite des deux labels vers `0` et `1` et indiquer que `1` correspond à la classe malveillante (ou documenter le mapping retenu). Vérifier qu'il correspond à celui utilisé par la baseline.
4. Charger tokenizer et modèle `distilbert-base-uncased` avec une tête à deux classes. Tokeniser les prompts avec troncature et padding adapté. Choisir la longueur maximale à partir des longueurs observées en EDA et noter quelle part des textes est tronquée.
5. Préparer les données pour Hugging Face `Trainer`. Choisir les paramètres avant l'entraînement : nombre d'époques, batch size, taux d'apprentissage, graine, stratégie d'évaluation/sauvegarde et métrique de sélection. Enregistrer versions, matériel et paramètres.
6. Entraîner sur train et sélectionner le meilleur état à l'aide de validation. Surveiller surapprentissage, déséquilibre de classes et ressources. Ne pas ajuster le modèle en fonction des scores de test.
7. Une fois les choix figés, prédire le test et calculer les mêmes mesures que pour la baseline : précision, rappel, F1 de la classe malveillante, supports et matrice de confusion.
8. Sauvegarder modèle et tokenizer. Exporter les prédictions avec une clé `example_id` compatible avec la baseline, `y_true`, `y_pred` et le score/probabilité malveillante.

## Livrables et passage de relais

Fournir les prédictions test, les métriques, les paramètres exacts, la graine, les versions et l'emplacement du modèle sauvegardé. Confirmer si les exemples test sont réellement les mêmes que ceux de la baseline. Si les jeux diffèrent, ne pas présenter la comparaison comme appariée.

## Points à documenter dans le rapport

- La troncature et la longueur maximale choisie ;
- le coût matériel/temps utile et les contraintes rencontrées ;
- les critères de sélection sur validation et les réglages effectués ;
- les faux négatifs/faux positifs intéressants et les limites de généralisation.
