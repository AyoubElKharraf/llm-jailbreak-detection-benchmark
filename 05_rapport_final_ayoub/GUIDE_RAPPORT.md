# Guide de rédaction du rapport final

**Responsable : Ayoub** — Échéance : **28 novembre 2026**.

## Objectif

Raconter l'expérience de façon reproductible et critique : pourquoi le problème est étudié, quelles données et méthodes ont été utilisées, quels résultats ont été mesurés et dans quelles limites les conclusions sont valables. Utiliser `rapport_template.md` comme plan de départ.

## Documents à récupérer avant rédaction

- Compte rendu EDA : schéma, effectifs, labels, contrôle des groupes et protocole de split ;
- fiche d'expérience baseline et fiche DistilBERT : paramètres, graine, versions et métriques ;
- exports et tableau comparatif validés par Taoufik ;
- références vérifiables du dataset, du modèle pré-entraîné et des outils utilisés.

## Étapes de rédaction

1. **Introduction** : définir le problème, expliquer l'objectif du mini-projet et annoncer les deux approches comparées sans revendiquer une solution de sécurité complète.
2. **Dataset** : citer `neuralchemy/Prompt-injection-dataset`, distinguer les configurations `core` et `full`, décrire les colonnes pertinentes, classes, catégories disponibles, effectifs mesurés et limites connues.
3. **Protocole** : documenter splits, prévention des fuites, `group_id`, mapping des labels, graine, identifiants et conditions nécessaires à une comparaison équitable. Préciser si les modèles sont évalués sur les mêmes exemples.
4. **Méthodes** : décrire TF-IDF + régression logistique et DistilBERT, les traitements, paramètres retenus, versions logicielles et matériel suffisamment pour reproduire l'expérience.
5. **Résultats** : reporter les valeurs vérifiées de précision, rappel, F1, support et matrices de confusion. Définir la classe positive et les conventions. Ne pas remplir les chiffres avant la fin des évaluations.
6. **Analyse** : expliquer les compromis observés et examiner les faux négatifs et faux positifs. Relier les interprétations aux observations sans tirer de conclusion au-delà du jeu évalué.
7. **Limites** : discuter couverture du dataset, labels potentiellement ambigus, doublons/groupes, déséquilibre, configurations différentes, évolution des attaques et écart entre benchmark et prompts rencontrés en pratique.
8. **Conclusion et suite** : répondre aux objectifs, résumer les constats mesurés et proposer des améliorations réalistes.
9. Relire les chiffres en les comparant aux exports et au tableau de bord ; vérifier les citations et compléter les instructions de reproduction.

## Message obligatoire sur la sécurité

Écrire clairement que le classifieur peut produire des faux positifs et des faux négatifs, être contourné et ne garantit pas une sécurité absolue en production. Les résultats d'un benchmark ne démontrent pas la sécurité d'un système LLM complet ; une défense doit être évaluée dans son contexte et s'inscrire dans une approche en profondeur.

## Vérification finale

- [ ] Chaque chiffre peut être retrouvé dans un résultat exporté.
- [ ] Les limites de comparabilité `core`/`full` sont explicites.
- [ ] Le contrôle anti-fuite est expliqué, avec ses limites.
- [ ] Les erreurs et limites du dataset sont discutées.
- [ ] Les sources, versions, paramètres et consignes de reproduction sont indiqués.
- [ ] Le rapport ne présente pas le classifieur comme une garantie de sécurité.
