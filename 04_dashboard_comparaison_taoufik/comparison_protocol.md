# Protocole et Analyse Comparatifs — Phase 4

**Auteurs :** Mansouri Taoufik & Ayoub El Kharraf  
**Projet :** Benchmark de Détection de Prompt Injection et Jailbreak (Master M2I Cybersécurité CEH)  
**Date d'évaluation :** 19 novembre 2026  
**Jeu de Test Commun :** 942 exemples officiels (`neuralchemy/Prompt-injection-dataset`)

---

## 1. Rigueur du Protocole & Contrôle d'Alignement
- **Échantillons évalués :** Exactement 942 exemples de test (`test_0000` à `test_0941`).
- **Concordance des labels (`y_true`) :** **100 %** (zéro divergence entre les deux modèles).
- **Proportions du test :** 390 Bénins (41,40 %) vs 552 Malveillants (58,60 %).
- **Règles anti-fuite respectées :** 
  - La Baseline a été ajustée et entraînée exclusivement sur `core/train.parquet` (4 391 exemples).
  - DistilBERT a été fine-tuné sur `full/train.parquet` dédupliqué (13 934 exemples).
  - Aucun exemple de test n'a participé au choix des hyperparamètres.

---

## 2. Tableau Comparatif Consolidé des Performances

| Métrique d'Évaluation | Baseline (TF-IDF + LR) | DistilBERT (`full`) | Écart / Analyse |
|---|:---:|:---:|---|
| **Exactitude (Accuracy)** | 95,75 % | **96,28 %** | **+0,53 %** pour DistilBERT |
| **Précision (Malveillant)** | 95,23 % | **96,58 %** | **+1,35 %** (Moins de faux positifs) |
| **Rappel (Attaques interceptées)** | **97,64 %** | 97,10 % | Baseline très sensible aux mots-clés |
| **F1-Score (Classe Malveillante)**| 96,42 % | **96,84 %** | **+0,42 %** en faveur du Transformer |
| **Macro F1** | 95,60 % | **96,17 %** | **+0,57 %** |
| **ROC-AUC** | 99,55 % | 99,55 % | Pouvoir discriminant exceptionnel |
| **Fausses Alertes (FP / 390)** | 27 (6,92 %) | **19 (4,87 %)** | **-8 erreurs** (Meilleure usabilité) |
| **Attaques Manquées (FN / 552)** | **13 (2,36 %)** | 16 (2,90 %) | Sécurité très élevée pour les deux |
| **Temps d'inférence moyen** | **~0,12 ms / prompt** | ~15-25 ms / prompt | **Baseline ~150x plus rapide** |

---

## 3. Analyse Comparative Forensique & Enseignements

### 3.1 Accord des Détecteurs (97,35 % de concordance)
Sur les 942 requêtes testées, les deux modèles prennent exactement **la même décision sur 917 exemples** (97,35 % d'accord). Cela confirme que la grande majorité des injections directes et des prompts bénins sont identifiables de manière stable.

### 3.2 Pourquoi DistilBERT est supérieur sur les Faux Positifs (-30 % d'erreurs)
- La Baseline TF-IDF génère **27 fausses alertes** contre **19 pour DistilBERT**.
- *Cause :* Le modèle TF-IDF se base sur la présence de n-grammes isolés (comme `"system"`, `"ignore"`, `"password"`, `"shell"`). Dès qu'un prompt utilisateur légitime contient ces termes techniques (par exemple : *"Explique-moi comment fonctionne le shell Linux"*), la Baseline risque de sur-réagir et de bloquer l'utilisateur sain.
- DistilBERT, grâce à ses mécanismes d'attention bidirectionnelle, comprend la syntaxe globale et la sémantique : il distingue une demande pédagogique inoffensive d'une véritable tentative de détournement d'instructions.

### 3.3 Le Compromis Vitesse vs Puissance Sémantique
- **Baseline (TF-IDF + Régression Logistique) :** Avec un temps de calcul de **0,12 ms**, elle est quasiment instantanée et ne consomme aucune ressource GPU.
- **DistilBERT :** Bien que légèrement plus lourd (~20 ms), il offre un taux de faux positifs nettement inférieur et résiste mieux aux attaques complexes avec paraphrases ou encodages.

---

## 4. Recommandation d'Architecture Industrielle (Multi-Tier WAF)
La conclusion de ce benchmark démontre qu'en production, ces deux approches ne doivent pas s'opposer mais **se compléter en cascade** :
1. **Niveau 1 (Baseline TF-IDF ultra-rapide) :** Traite 100 % des requêtes entrantes. Si le score est manifestement hostile (> 0,90) ou clairement bénin (< 0,10), la décision est prise en 0,1 ms.
2. **Niveau 2 (DistilBERT) :** N'est déclenché que pour la zone d'incertitude (scores ambigus entre 0,10 et 0,90) afin d'apporter un arbitrage contextuel fin sans surcharger l'infrastructure.
