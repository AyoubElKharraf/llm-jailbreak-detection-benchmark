# Phase 5 — Rapport final

**Responsable : Ayoub**

**Échéance de rendu : 28 novembre 2026**

## Objectif

Présenter le projet de manière compréhensible, reproductible et critique. Le rapport doit décrire la source NeurAlchemy retenue et ses configurations, comparer les modèles avec les résultats réellement mesurés et expliquer les limites. Utiliser `rapport_template.md` comme trame.

## Ce qu'il faut rassembler avant de rédiger

- Inventaire et validation de la source NeurAlchemy, définition des labels et résultats EDA de la phase 1 ;
- compte rendu EDA et protocole anti-fuite validé par Taoufik ;
- fiches d'expérience baseline et DistilBERT (paramètres, versions, graines, matériel) ;
- exports, métriques, matrices de confusion et synthèse des erreurs du tableau de bord ;
- références officielles des datasets, modèles et bibliothèques ;
- consignes de présentation et format imposés par le cours, s'il y en a.

## Plan de travail de rédaction

### 1. Fixer le message et le périmètre

Formuler l'objectif exact : détection d'injection, détection de jailbreak/demande nuisible, ou tâche plus large explicitement définie. Éviter d'utiliser ces termes comme synonymes si le corpus mélange des phénomènes différents. Énoncer les questions auxquelles les expériences peuvent réellement répondre.

### 2. Décrire le dataset retenu

Donner l'identifiant exact, la version/date de récupération, les configurations `core`/`full`, les tailles observées, les champs utiles, la langue, les labels et les catégories. Expliquer la différence entre train original de `core` et train augmenté de `full`, ainsi que la vérification des jeux de validation/test. Attribuer la provenance des sources intégrées à la carte du fournisseur ; ne pas présenter une fusion manuelle réalisée par le binôme.

### 3. Décrire la qualité et le protocole

Présenter les répartitions mesurées par label, source, catégorie et split. Décrire le contrôle des groupes, doublons et quasi-doublons, les décisions de séparation, la graine et les précautions pour éviter que le modèle apprenne seulement des indices propres à une source. Préciser si une source entière a été gardée pour tester la généralisation.

### 4. Expliquer les modèles

Décrire la baseline TF-IDF + régression logistique et DistilBERT, leurs prétraitements, paramètres retenus, règle de sélection sur validation, environnement et versions. Inclure la longueur maximale et la troncature pour DistilBERT.

### 5. Rapporter les résultats

Reporter seulement les valeurs retrouvées dans les exports : précision, rappel, F1, supports et matrices de confusion. Définir la classe positive et la convention des métriques. Indiquer clairement si les deux modèles ont le même test. Ajouter les résultats par source/catégorie seulement si l'effectif est suffisant et le périmètre comparable.

### 6. Analyser les erreurs et limites

Étudier les faux négatifs et faux positifs, les catégories où les erreurs se concentrent, les biais liés aux sources, les labels incertains, le déséquilibre et l'absence éventuelle de données représentatives. Relier chaque interprétation aux observations disponibles.

### 7. Conclure et relire

Répondre aux objectifs sans généraliser au-delà du benchmark. Vérifier chaque chiffre contre le tableau de résultats et chaque source contre la bibliographie. Ajouter les consignes nécessaires à la reproduction et faire relire le rapport par Taoufik.

## Message obligatoire sur la sécurité

Préciser que les classifieurs peuvent produire des faux positifs et faux négatifs, être contournés et ne garantissent pas une sécurité absolue en production. Une performance sur ce corpus ne prouve pas la sécurité d'un système LLM complet ; le détecteur doit être évalué dans le contexte d'usage et s'inscrire dans une approche de défense en profondeur.

## Livrables

1. Rapport complété à partir de `rapport_template.md` ;
2. tableaux/figures dont les chiffres concordent avec les exports ;
3. bibliographie et citations des jeux de données, versions et modèles ;
4. annexe de reproductibilité avec protocole et paramètres ;
5. version relue par Taoufik avant le rendu.

## Fichiers à produire dans ce dossier

| Fichier | Contenu attendu | À versionner ? |
|---|---|---|
| `rapport_final.md` ou `rapport_final.docx` | Rapport complété depuis `rapport_template.md`, avec résultats vérifiés, références et analyse critique. | Oui |
| `figures/` | Figures finales numérotées, légendées et citées dans le rapport. | Oui |
| `references.bib` (si BibTeX est utilisé) | Références des sources, modèles et outils ; sinon les inclure dans le rapport. | Oui |
| `reproduction.md` | Sources, split, versions, paramètres et étapes nécessaires pour reproduire les expériences. | Oui |
| `annexes/` (si nécessaire) | Tableaux supplémentaires, dictionnaire des données et détails expérimentaux utiles. | Oui, sous réserve des conditions des données |

Ne pas inclure dans le rapport prompts ou données sources si leur redistribution n'est pas autorisée. Citer les sources et décrire comment les récupérer selon leurs conditions.

## Checklist finale

- [ ] La tâche et les classes sont définies sans ambiguïté.
- [ ] Les sources, versions, licences/conditions et transformations sont décrites.
- [ ] Les effectifs finaux sont après harmonisation/déduplication.
- [ ] Le split et les contrôles anti-fuite sont expliqués.
- [ ] Les deux modèles sont comparés sur un périmètre identifié.
- [ ] Chaque chiffre est vérifiable dans un artefact de résultat.
- [ ] Les faux négatifs, faux positifs, limites du dataset et limites de généralisation sont abordés.
- [ ] Le rapport affirme qu'un classifieur ne garantit pas une sécurité absolue en production.
- [ ] Taoufik a relu les chiffres et les conclusions comparatives.
