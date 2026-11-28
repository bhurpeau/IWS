# Référence G0.4 (état F) — règles, contrôles et bilan

Copie figée à la clôture de G0.4 (décision F2). Ne pas modifier : les arbitrages de G0.5 portent sur `notations/collisions.yaml`.

## Règles de classification

- **Nature** (une ou plusieurs) : HOMONYMIE (même notation, objets distincts) ; SYNONYMIE (plusieurs notations, même objet) ; QUASI_COLLISION (proximité graphique ou conceptuelle) ; AMBIGUITE (identification sémantique insuffisante).
- **Niveau** (indépendant de la nature) :
  - N0 : réemploi local légitime ;
  - N1 : collision graphique sans ambiguïté de rôle ;
  - N2 : collision sémantique dans une portée significative ;
  - N3 (règle F1) : collision intervolumes entre objets distincts dont les portées, rôles ou contextes sont assez proches pour compromettre l'interprétation du corpus commun ;
  - N4 : définition absente, ambiguïté mathématique ou types incompatibles.
- **Facteur aggravant** : réservation explicite par le volume II. Elle fixe la priorité notationnelle à l'arbitrage ; elle n'est ni nécessaire ni suffisante pour N3.
- **Intervention** : PRESERVER, DOCUMENTER, CORRECTION_CANDIDATE, A_ARBITRER. Un classement N0 ou N1 n'implique pas d'intervention dans les manuscrits.
- **Catégorie de correction** : NOTATIONNELLE, TERMINOLOGIQUE, DOCUMENTAIRE, SCIENTIFIQUE. Les corrections scientifiques A-G02-14, A-G02-15 et le constat ζ_min suivent un circuit distinct.

## Contrôles (`notations/scripts/build_collisions.py`)

Les contrôles portent sur :

- les champs obligatoires et les valeurs autorisées ;
- l'existence des objets, des relations et des anomalies ;
- les sélecteurs non vides ;
- la couverture des 50 clés ambiguës ;
- l'examen des relations DIST, ANA et UNK, et des synonymies des relations ID ;
- la règle F1 ;
- la documentation des reclassements.

Résultat à la clôture : 0 erreur ; 37 tests verts.

## Bilan quantitatif

- **Collisions :** 65.
- **Niveaux :** N0 4, N1 18, N2 32, N3 7, N4 4. Au diagnostic initial : N2 30, N3 9 ; reclassements COL-PHI-01 et COL-C-01, de N3 à N2.
- **Interventions :** A_ARBITRER 49, PRESERVER 10, DOCUMENTER 5, CORRECTION_CANDIDATE 1.
- **Occurrences distinctes côté volume I :** 3 619 au total (borne supérieure), dont 643 pour les N3 et N4.
- **ρ (lecture) :** 395, rapprochées de l'audit historique.
- **50 clés ambiguës :** couvertes 50/50 ; niveau maximal N0 10, N1 22, N2 18.
