# Détection de prompt injection et de jailbreak sur les LLM

**Groupe 7 — Ayoub El Kharraf et Mansouri Taoufik**  
**Date limite : 28 novembre 2026**

## Résumé

<!-- Contexte, méthode, principaux résultats vérifiés et conclusion. -->

## 1. Introduction

### Contexte et problématique
### Objectifs et contributions

## 2. Dataset

### Source et configurations (`core` et `full`)
### Schéma, labels et catégories
### Qualité, équilibre des classes et contrôle des fuites

## 3. Méthodologie

### Baseline : TF-IDF + Logistic Regression
### Modèle transformer : DistilBERT
### Prétraitement, paramètres et environnement

## 4. Protocole expérimental

### Découpage des données et reproductibilité
### Métriques et définition de la classe positive
### Comparabilité des jeux de test

## 5. Résultats

| Modèle | Précision | Rappel | F1-score | Support test |
|---|---:|---:|---:|---:|
| TF-IDF + Logistic Regression | À compléter | À compléter | À compléter | À compléter |
| DistilBERT | À compléter | À compléter | À compléter | À compléter |

### Matrices de confusion
### Analyse des erreurs

## 6. Discussion et analyse critique

## 7. Limites du dataset et de l'étude

Discuter notamment de la couverture des attaques, de l'ambiguïté des labels, du décalage de domaine et des limites de généralisation.

**Un classifieur peut produire des faux positifs et des faux négatifs et être contourné. Il ne garantit pas une sécurité absolue en production et doit s'inscrire dans une approche de défense en profondeur.**

## 8. Conclusion et pistes futures

## Références

## Annexe : paramètres et instructions de reproduction
