# Détection de prompt injection et de jailbreak sur les LLM

**Groupe 7 — Ayoub El Kharraf et Mansouri Taoufik**  
**Date limite : 28 novembre 2026**

## Résumé

<!-- Problématique, sources de données, méthodes, résultats vérifiés et conclusion en quelques lignes. -->

## 1. Introduction

### 1.1 Contexte et problématique
### 1.2 Définition de la tâche : prompt injection, jailbreak ou tâche combinée
### 1.3 Objectifs et questions de recherche

## 2. Corpus multi-sources

### 2.1 Sources et versions utilisées

| Source | Version/date | Exemples retenus | Champs/labels d'origine | Décision d'inclusion |
|---|---|---:|---|---|
| À compléter | À compléter | À mesurer | À décrire | À justifier |

### 2.2 Définition des classes et harmonisation des labels
### 2.3 Nettoyage, doublons, contradictions et provenance
### 2.4 Distribution des classes, sources, langues et catégories
### 2.5 Limites et biais possibles du corpus

## 3. Protocole expérimental

### 3.1 Découpage train/validation/test
### 3.2 Contrôle de `group_id`, doublons et fuites
### 3.3 Identifiants et reproductibilité
### 3.4 Métriques et définition de la classe positive

## 4. Modèles

### 4.1 Baseline : TF-IDF + Logistic Regression
### 4.2 Transformer : DistilBERT
### 4.3 Prétraitement, paramètres et environnement matériel/logiciel

## 5. Résultats

| Modèle | Précision (malveillant) | Rappel (malveillant) | F1-score | Support test |
|---|---:|---:|---:|---:|
| TF-IDF + Logistic Regression | À mesurer | À mesurer | À mesurer | À mesurer |
| DistilBERT | À mesurer | À mesurer | À mesurer | À mesurer |

### 5.1 Matrices de confusion
### 5.2 Comparabilité des exemples test
### 5.3 Résultats par source/catégorie, si l'effectif le permet

## 6. Analyse des erreurs et discussion

### 6.1 Faux négatifs et faux positifs
### 6.2 Comparaison des modèles
### 6.3 Limites de validité et généralisation

## 7. Limites et sécurité en production

Discuter de la couverture des sources, des labels, du déséquilibre, des biais de collecte et de la fuite potentielle. Un classifieur peut se tromper ou être contourné : ses résultats ne garantissent pas la sécurité d'un système LLM en production.

## 8. Conclusion et pistes futures

## Références

## Annexe A — Paramètres et instructions de reproduction
## Annexe B — Dictionnaire des données et mapping des labels
