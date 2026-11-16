# Guide d'exploration des données (EDA)

**Responsable : Taoufik** — C'est le point de départ technique commun. Ayoub doit recevoir les décisions de cette étape avant de figer son protocole d'entraînement.

## Objectif

Comprendre exactement le contenu des configurations `core` et `full` de `neuralchemy/Prompt-injection-dataset`, vérifier la qualité des données et établir une séparation d'entraînement/validation/test sans fuite connue.

## À préparer

- Un environnement Python avec les dépendances de `requirements.txt`.
- L'accès réseau pour récupérer le dataset via Hugging Face `datasets`.
- Un emplacement de travail pour les tableaux et graphiques ; éviter de versionner les fichiers de cache du dataset.

## Étapes à suivre

1. Charger séparément les configurations `core` et `full`. Noter les splits réellement fournis (par exemple train/test ou train/validation/test), leur taille et les colonnes. Ne pas supposer que les deux configurations ont le même schéma.
2. Examiner des exemples de chaque split. Identifier et consigner : colonne texte, colonne cible, identifiant d'exemple éventuel, catégorie d'attaque éventuelle, source et `group_id` éventuel.
3. Comprendre les labels d'origine : valeurs possibles, signification et correspondance exacte avec les deux classes **bénin** et **malveillant**. Signaler toute valeur ambiguë ou classe non binaire au lieu de la convertir silencieusement.
4. Produire un bilan par split : nombre de lignes, répartition des labels en effectifs et pourcentages, valeurs manquantes, textes vides, doublons exacts et statistiques de longueur des prompts. Visualiser l'équilibre des classes et les longueurs.
5. Si des catégories d'attaques existent, compter les exemples par catégorie et vérifier leur répartition entre splits. Une catégorie peut être absente d'un split ; le signaler.
6. Examiner `group_id` s'il existe : nombre de groupes, tailles min/max, groupes présents dans plusieurs splits et cohérence des labels au sein d'un groupe. Si vous créez des splits, grouper les exemples liés dans une seule partition. Ne jamais répartir aléatoirement les lignes sans vérifier les groupes.
7. Comparer les textes et identifiants entre splits pour repérer des recouvrements ou quasi-doublons susceptibles de créer une fuite. Décrire la méthode et reconnaître qu'une recherche de doublons exacts ne repère pas toutes les reformulations.
8. Décider avec Ayoub du protocole commun : splits officiels ou split groupé, graine, mapping des labels, colonne d'identification et format des exports. Vérifier que les exemples des configurations `core` et `full` peuvent être reliés avant de promettre une comparaison appariée.

## Résultats à laisser dans ce dossier

Créer un compte rendu EDA (Markdown, tableur ou notebook, selon le choix du binôme) indiquant :

- la date et la version/source du dataset, les configurations et splits consultés ;
- les noms et définitions des colonnes utiles ;
- les distributions de classes, catégories, valeurs manquantes, doublons et longueurs ;
- les contrôles de groupes/fuites réalisés et leurs résultats ;
- les décisions de split, mapping des labels et identifiant retenus ;
- les questions restant ouvertes et les limites de l'analyse.

Joindre des graphiques lisibles si cela aide l'interprétation. Les chiffres du compte rendu doivent venir du dataset chargé, pas être estimés à l'avance.

## Contrôle avant passage à la suite

- [ ] Les schémas de `core` et `full` sont connus et leurs différences sont notées.
- [ ] Les labels bénin/malveillant sont définis sans ambiguïté.
- [ ] La présence/absence de `group_id` est vérifiée et les recouvrements entre splits sont examinés.
- [ ] La règle de séparation et la graine sont communiquées à Ayoub.
- [ ] La possibilité d'aligner le jeu de test des deux modèles est vérifiée ou la limite est signalée.
