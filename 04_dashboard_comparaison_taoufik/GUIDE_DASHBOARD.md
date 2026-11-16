# Guide du tableau de bord comparatif

**Responsable : Taoufik** — Cette phase commence lorsque les deux responsables ont remis des prédictions de test et leur protocole.

## Objectif et éléments nécessaires

Présenter les résultats de la baseline et de DistilBERT de manière lisible, vérifiable et honnête sur la comparabilité. Récupérer les deux exports avec au minimum identifiant stable, label réel et prédiction, ainsi que les définitions des labels et splits utilisés. Les scores seuls ou deux captures d'écran ne suffisent pas.

## Étapes

1. Vérifier le format, le nombre de lignes, les valeurs manquantes, les labels et les identifiants des deux exports. Repérer les doublons d'identifiants.
2. Joindre les fichiers par identifiant d'exemple, jamais simplement par numéro de ligne. Mesurer le nombre d'exemples présents dans les deux fichiers et ceux absents de l'un ou l'autre.
3. Vérifier que `y_true` est identique pour chaque exemple aligné. Si les labels divergent, arrêter la comparaison et résoudre le problème de mapping ou de version du dataset.
4. Déterminer le périmètre d'évaluation : comparaison appariée sur les seuls exemples communs si ce périmètre est valide, ou résultats séparés si les tests ne sont pas comparables. Indiquer les exclusions et supports.
5. Pour chaque modèle, calculer précision, rappel, F1-score et support, avec la classe positive malveillante explicitement définie. Ajouter la matrice de confusion avec ordre des axes lisible. Utiliser les mêmes conventions de métriques.
6. Présenter les résultats dans un tableau comparatif et des graphiques simples. Ajouter des filtres ou vues utiles (modèle, classe, catégorie si disponible) sans masquer les tailles d'échantillons.
7. Examiner des erreurs représentatives : faux négatifs (attaques manquées) et faux positifs (prompts bénins signalés). Masquer ou anonymiser le contenu si nécessaire.
8. Construire le tableau de bord avec l'outil choisi (Streamlit ou autre dépendance déjà prévue) et indiquer comment le lancer ainsi que les chemins attendus pour les exports.

## Attention à « avant/après protection »

Le projet compare deux classifieurs. Il ne mesure pas automatiquement une protection appliquée à un LLM. N'utiliser une comparaison « avant/après protection » que si une défense, un protocole et des données avant/après ont réellement été définis et évalués. Sinon, nommer clairement les vues « baseline vs DistilBERT ».

## Livrables

- Un tableau consolidé des métriques et des supports ;
- les matrices de confusion des deux modèles ;
- une visualisation comparative et un tableau de bord exécutable ;
- une note qui décrit l'alignement, le split, les exclusions et toute limite de comparabilité ;
- une synthèse transmissible à Ayoub pour le rapport.

## Contrôle qualité

- Les prédictions sont jointes par identifiant et les labels réels concordent.
- Le nombre d'exemples évalués est visible et cohérent avec les exports.
- Les métriques utilisent la même définition de classe positive.
- Les graphiques ne suggèrent pas une comparaison équitable si les populations test diffèrent.
