# Phase 1 — Construire et auditer le corpus

**Préparation et harmonisation : Ayoub**

**Audit EDA et validation du protocole : Taoufik**

Ce dossier couvre deux travaux liés : Ayoub prépare une collection unifiée et traçable ; Taoufik vérifie cette collection, son contenu et le protocole d'évaluation avant la baseline. La priorité est d'obtenir des exemples correctement définis et traçables, pas seulement un grand nombre de lignes.

## Décision à prendre avant la collecte

Le projet vise-t-il à classer **les prompt injections**, ou à classer plus largement les **jailbreaks / demandes nuisibles** ? Ces tâches sont proches mais pas identiques. Un jailbreak peut être une demande nuisible directe sans injection d'instructions, tandis qu'une injection cherche à détourner des instructions dans un contexte donné. Il faut fixer une définition opérationnelle de « malveillant » avant de combiner les sources et l'écrire dans le compte rendu.

La liste « Prompt Injection Detection Dataset » doit être identifiée par son URL ou son identifiant de dépôt exact : ce nom générique désigne plusieurs corpus. Vérifier sa carte de dataset, son schéma, sa licence et ses sources avant de l'ajouter.

## Sources envisagées et vigilance

| Source envisagée | Vérifications à faire avant inclusion |
|---|---|
| `JailbreakBench` / `JBB-Behaviors` | Distinguer le jeu de comportements bénins/nuisibles des chaînes de jailbreak soumises et des réponses de modèles. Le dépôt décrit 100 comportements nuisibles et 100 bénins, avec champs `Behavior`, `Goal`, `Target`, `Category`, `Source` ; ce ne sont pas automatiquement des exemples de prompts d'injection prêts à étiqueter. Définir précisément quel champ représente l'entrée à classifier. |
| `Prompt Injection Detection Dataset` | Confirmer le dépôt précis, les labels, la langue, les colonnes et la provenance. Par exemple, `hlyn-labs/prompt-injection-judge-deberta-dataset` est une collection annoncée comme fusionnant 12 sources, dont `deepset` et `neuralchemy`, et l'accès à ses fichiers demande d'accepter ses conditions. Si c'est le dataset visé, ne pas ajouter une seconde fois ses sources incluses. |
| `deepset/prompt-injections` | Examiner `text`, `label`, la langue, la taille et la licence actuellement affichée sur la carte Hugging Face. Garder la source/provenance et contrôler les doublons avec toutes les autres sources. |
| HarmBench | Vérifier la version/fichier utilisé et distinguer prompts de comportements, prompts d'attaque, réponses et jugements de succès. HarmBench est un benchmark de red teaming et de refus ; ses champs ne sont pas tous des labels directs « injection/bénin ». Définir une règle d'inclusion et de labellisation avant utilisation. |

Les dépôts et leurs versions peuvent changer. Consigner l'URL exacte, la révision/commit ou date de récupération, la configuration/split et la licence/conditions de chaque source. Vérifier les droits de redistribution avant de publier le corpus combiné ; si besoin, ne publier que le manifeste et les instructions de reconstruction.

## A. Travail d'Ayoub — collecte et harmonisation

### Ce qu'il faut préparer

- Accès aux pages officielles Hugging Face/GitHub de chaque source ; accès réseau pour les récupérer.
- Un tableau d'inventaire des sources et une définition écrite de la tâche cible.
- Un emplacement de travail local pour les données brutes et le corpus préparé. Ne pas écraser les originaux.
- Une décision avec Taoufik sur les colonnes communes et la partition finale avant l'entraînement.

### Étapes

1. **Inventorier chaque source séparément.** Pour chaque dataset, relever l'identifiant exact, URL, date/révision, licence/conditions, configuration, splits, taille, colonnes, langue et signification des labels. Conserver une copie ou référence des métadonnées utilisées.
2. **Choisir les unités admissibles.** Préciser si l'exemple est un prompt utilisateur, une chaîne d'injection, un comportement/objectif nuisible ou un texte de réponse. Ne pas mélanger ces unités comme si elles étaient équivalentes. Exclure ou isoler les données qui ne correspondent pas à la définition cible.
3. **Définir le schéma canonique** avec au minimum : `text` (texte réellement classifié), `label` (mapping documenté), `source_dataset`, `source_split`, `source_id` ou index d'origine, `attack_type` si disponible, `language` si connue et `group_id`/groupe de provenance si possible. Garder les colonnes originales utiles dans un fichier de provenance ou des champs préservés.
4. **Harmoniser les labels explicitement.** Écrire pour chaque label original sa conversion ou sa raison d'exclusion. Ne jamais attribuer automatiquement « malveillant » à toutes les lignes HarmBench/JailbreakBench sans confirmer que le champ est bien un prompt d'attaque correspondant à la tâche.
5. **Nettoyer sans dénaturer.** Retirer les lignes vides, normaliser uniquement les aspects techniques nécessaires, préserver le texte original et noter toute transformation. Détecter doublons exacts et conflits de labels. Pour les doublons, conserver la provenance de toutes les sources ; en cas de labels contradictoires, arbitrer selon une règle écrite ou exclure le cas ambigu.
6. **Prévenir le leakage.** Regrouper les doublons et exemples apparentés (même prompt, même comportement, même famille d'attaque ou même `group_id`) dans une seule partition. Faire le split après déduplication. Si possible, garder une source entière pour un test de généralisation « source inconnue », en plus d'un test standard stratifié ; ne pas laisser les deux partitions contenir des variantes quasi identiques.
7. **Préparer un corpus traçable**, avec une clé stable par exemple et un manifeste indiquant quelles sources/lignes ont été incluses, exclues ou dédupliquées. Garder les données de test isolées du train et de la validation.
8. **Transmettre à Taoufik** le schéma, mapping des labels, manifeste, règles de nettoyage/déduplication, split et graine, ainsi que les contrôles déjà effectués. Ne pas transmettre un CSV sans documentation.

## B. Travail de Taoufik — EDA et audit avant entraînement

### Étapes

1. Vérifier que les sources, volumes et règles annoncés par Ayoub correspondent au manifeste et au corpus remis.
2. Examiner colonnes, types, quelques exemples par source et label, valeurs manquantes, textes vides, doublons et conflits de labels.
3. Mesurer les effectifs et pourcentages par label, source, catégorie d'attaque, langue et split. Noter les sources qui ne possèdent pas de classe bénigne ou malveillante, ou dont les labels sont indirects.
4. Comparer les distributions et longueurs de texte par source. Chercher des indices de raccourcis (par exemple le modèle pourrait apprendre la source, le format, une phrase modèle ou une langue plutôt que la notion d'attaque).
5. Vérifier les recouvrements de `group_id`, identifiants, doublons exacts et similarités proches entre train/validation/test. La déduplication exacte seule ne prouve pas l'absence de fuite.
6. Décider si le corpus est suffisamment cohérent pour entraîner le classifieur. Si les sources ont des définitions incompatibles, proposer un sous-ensemble ou des évaluations séparées plutôt que forcer un label binaire douteux.
7. Valider avec Ayoub le protocole, puis communiquer à Taoufik/Ayoub les constats et décisions afin que baseline et DistilBERT utilisent la même définition de tâche et un test comparable.

## Livrables attendus dans ce dossier

1. **Inventaire des datasets** : dépôt/version, licence/conditions, contenu, labels et décision d'inclusion.
2. **Définition de la tâche et dictionnaire de données** : ce que signifie chaque classe et chaque colonne canonique.
3. **Manifeste de construction** : transformations, exclusions, déduplication, conflits, provenance et split ; permettre de reconstruire le corpus sans perdre la source de chaque ligne.
4. **Compte rendu EDA de Taoufik** : tableaux/figures et vérifications ci-dessus, avec décisions et limites.
5. **Décision de passage** : corpus validé pour l'entraînement, corpus à corriger, ou protocole révisé.

## Fichiers à produire dans ce dossier

Créer les fichiers suivants au fur et à mesure. Ces noms sont proposés pour que les deux membres échangent des livrables faciles à retrouver.

| Fichier | Responsable | Contenu attendu | À versionner ? |
|---|---|---|---|
| `sources_inventory.md` | Ayoub | Tableau des sources : URL/identifiant, version ou date, licence/conditions, schéma, labels, décision d'inclusion et provenance. | Oui |
| `data_dictionary.md` | Ayoub + Taoufik | Définition du problème, classes, mapping des labels d'origine, colonnes canoniques et règles d'inclusion/exclusion. | Oui |
| `corpus_manifest.csv` | Ayoub | Une ligne par exemple conservé : `example_id`, source, split d'origine, identifiant d'origine, label mappé et groupe si disponible. | Oui si le manifeste ne redistribue pas de contenu soumis à restriction ; sinon documenter les références sans texte brut |
| `preparation_log.md` | Ayoub | Chargement, nettoyage, déduplication, conflits de labels, exclusions, transformations et limites. | Oui |
| `eda_report.md` | Taoufik | Résultats mesurés, tableaux, contrôles qualité/fuite et décision de validation du corpus. | Oui |
| `figures/` | Taoufik | Graphiques sur les classes, sources, catégories et longueurs, avec titres/légendes. | Oui, s'ils sont légers et dérivés |
| `dataset_final.*` | Ayoub | Corpus harmonisé utilisé par les modèles et format choisi par le binôme. | Généralement non si volumineux ou soumis à restriction ; conserver localement et ignorer par Git |

Ne pas committer les téléchargements bruts, caches Hugging Face ou données dont la redistribution n'a pas été vérifiée. Si le corpus final ne peut pas être partagé, conserver un manifeste adapté et les instructions de reconstruction depuis les sources officielles.

## Contrôle avant la phase baseline / DistilBERT

- [ ] Le nom exact et la version de chaque source sont enregistrés.
- [ ] La définition « prompt injection » ou « jailbreak/demande nuisible » est explicite.
- [ ] Les unités d'observation sont cohérentes ; prompts, comportements et réponses ne sont pas confondus.
- [ ] Le mapping des labels est justifié source par source.
- [ ] Les conditions de licence/redistribution ont été vérifiées et les sources sont attribuables.
- [ ] Les doublons et exemples apparentés restent dans une même partition.
- [ ] Les distributions par source et split sont connues ; les raccourcis de source ont été considérés.
- [ ] Ayoub et Taoufik se sont mis d'accord sur le schéma, la cible, le split et l'identifiant stable.
