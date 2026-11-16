# Guide de la baseline TF-IDF + régression logistique

**Responsable : Taoufik** — Configuration Hugging Face : `core`.

## Objectif et prérequis

Construire un premier détecteur de prompts malveillants avec une méthode classique et reproductible. Avant de commencer, lire le compte rendu EDA et confirmer le nom de la colonne texte, le mapping des labels, le split et l'identifiant stable des exemples.

## Étapes

1. Charger la configuration `core` et appliquer exactement le protocole documenté dans l'EDA. Vérifier une dernière fois tailles et labels des partitions.
2. Préparer les textes et labels. Faire seulement les transformations nécessaires et identiques entre train, validation et test. Ne pas supprimer une partie du prompt qui pourrait porter le signal d'attaque.
3. Créer un pipeline qui transforme les textes en TF-IDF puis entraîne `LogisticRegression`. Ajuster le vectoriseur exclusivement sur les textes d'entraînement.
4. Définir une baseline simple et noter les paramètres : paramètres TF-IDF (par exemple unigrammes/bigrammes, `min_df`, limite de vocabulaire), régularisation/class_weight et graine. Si vous comparez plusieurs variantes, choisir avec la validation, jamais avec le test.
5. Entraîner la variante retenue sur l'entraînement prévu. Calculer sur validation les métriques utiles si le protocole en prévoit une. Ne consulter le test qu'une fois les choix figés.
6. Sur le test, calculer précision, rappel et F1 pour la classe positive malveillante, ainsi que les supports et la matrice de confusion. Conserver aussi les prédictions et, si possible, le score/probabilité de la classe malveillante.
7. Sauvegarder localement le pipeline complet (vectoriseur et classifieur), les paramètres et les résultats. Indiquer la version de scikit-learn et la graine.

## Livrables et format des prédictions

Placer les artefacts dans un emplacement local clairement nommé. L'export des prédictions doit comporter au minimum une clé `example_id` stable (ou la clé de correspondance validée), `y_true` et `y_pred`. Ajouter le score malveillant et la configuration/modèle si possible. Conserver les identifiants et l'ordre des classes tels que définis dans l'EDA.

Transmettre à Ayoub et à la phase dashboard : le fichier de prédictions, les métriques, le modèle/paramètres, le split utilisé et toute exclusion appliquée. Ne pas envoyer uniquement une capture d'écran des scores.

## Vérifications avant de conclure

- Le pipeline TF-IDF a été ajusté sur train seulement.
- Aucun choix de paramètres n'a été fait à partir des résultats test.
- Les valeurs `y_true`/`y_pred` et la classe positive sont cohérentes avec l'EDA.
- L'export est alignable par identifiant avec les prédictions DistilBERT, ou la raison de non-alignement est consignée.
- Les erreurs, notamment les attaques manquées (faux négatifs), sont examinées.
