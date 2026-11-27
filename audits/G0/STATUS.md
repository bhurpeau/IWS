# G0 — État d'avancement

**Dernière mise à jour :** 27 novembre 2026
**Phase courante :** G0.2 **validée comme première itération, non clôturée** ; G0.2bis (complétude) **en cours** ; G0.3 non autorisée (C5)
**Commit de base :** `c74fa047171ff51e308f1855d8f636add2ac33ca` (IWS, tag `g0-baseline`)
**Branche de travail :** `harmonisation/g0` (poussée sur `origin`, non fusionnée dans `main`)
**Dernier commit de travail :** voir `git log` ; G0.1 : `05afddd` (tag `g0.1-inventaire-ref`, poussé, référence de non-régression) ; G0.2 itération 1 : commit « G0.2 (itération 1) » (registre candidat intermédiaire, 95 objets)
**PDF de référence :** prépublication [IWS — G0 Baseline](https://github.com/bhurpeau/IWS/releases/tag/g0-baseline) (4 PDF + `SHA256SUMS`, empreintes vérifiées après téléchargement)

## Références figées

| Dépôt | Commit |
|---|---|
| IWS | `c74fa04` (base, tag `g0-baseline`) |
| iws-lean | `e9fb1a6` = tag `annex-d-certified-v4.36.0` |
| IWS_minimality_package | `b1a9738` |
| IWS_1 | `4240233` |

Détail : [G0_00_manifest.md](G0_00_manifest.md), § 1.

## Phases

| Phase | État | Livrable |
|---|---|---|
| G0.0 | **Clôturée, validée le 27/11/2026** | `G0_00_manifest.md`, `G0_00_controls/`, `ERRATA_PLAN_G0.md`, ce fichier, README actualisé, release `g0-baseline` |
| G0.1 | **Clôturée, validée le 27/11/2026** | `G0_01_inventory/` (occurrences, expressions, familles, glyphes, exclusions, couverture, `extraction_report.md`) ; `notations/scripts/extract_symbols.py`, `check_coverage.py`, tests |
| G0.2 | **Itération 1 acceptée (C1) ; non clôturée** | `notations/registry.yaml` (registre candidat **intermédiaire**, 95 objets ; copie figée `G0_02_semantic/reference_95/`), `G0_02_objects_report.md`, `RESERVES.md`, `G0_02_semantic/`, scripts `definition_sites.py`, `link_registry.py` ; addendum G0.1 (B2a) et `check_regression.py` |
| G0.3 – G0.9 | Non entamées | — |

## Résultats des contrôles G0.0

| Contrôle | Résultat |
|---|---|
| Synchronisation des quatre dépôts avec `origin/main` | Conforme |
| Inclusions LaTeX volume I (17 fichiers + `.bib`) | Tous présents, aucun label dupliqué |
| Source canonique unique volume II | Conforme |
| Figures référencées (8 + 7) | Toutes présentes |
| Compilation de référence (pdfTeX, TeX Live 2026, sans `latexmk`) | Réussie : volume I 306 p., volume II 41 p., compagnons 5 et 4 p. ; 0 erreur, 0 référence ou citation non définie |
| Inventaire des labels (`.aux`) | Volume I : 525 ; volume II : 19 ; concordant avec les sources |
| Archivage des PDF | Release `g0-baseline`, SHA-256 vérifiés avant envoi et après téléchargement (4/4) |
| Intégrité des sources mathématiques | `git diff c74fa04 -- Volume_I Volume_II` vide |
| Bilan Lean | Rapporté (905 théorèmes, 3 axiomes standard, sans `sorryAx`) ; non reconstruit |

## Résultats des contrôles G0.1

| Contrôle | Résultat |
|---|---|
| Occurrences inventoriées | Volume I : 11 697 ; volume II : 3 591 (+14 dans les définitions de macros) ; compagnons LaTeX : 1 415 (+4) ; Markdown : 23 (extraction limitée) |
| Classes lexicales | I : 6 741 nu, 3 459 indexé, 1 102 variante, 395 composite ; II : 2 132 / 1 109 / 261 / 89 ; 0 non classé |
| Audit des 455 `\rho` | 455/455 ; répartition 48 / 8 / 4 / 395 reproduite par les plages de l'audit |
| Contrôle croisé regex ↔ inventaire | 408 couples commande × fichier, 0 écart |
| Lettres latines (indicatif) | 17/20 fichiers égaux ; 3 écarts expliqués par une limite du contrôle |
| Segmentation | 0 délimiteur non fermé ; 0 commande non reconnue |
| Ancres | Tous les labels utilisés existent dans les `.aux` de référence ; volume II : 37 % des occurrences sans label (19 labels seulement) |
| Motifs obsolètes V5.16 (13) | 0 occurrence dans V5.17 |
| Déterminisme | Deux exécutions identiques octet pour octet ; 15 tests unitaires passent |
| Intégrité des sources | `git diff c74fa04 -- Volume_I Volume_II` vide |

## Résultats des contrôles G0.2

| Contrôle | Résultat |
|---|---|
| Registre candidat | 95 objets (II : 57 ; I : 36 ; compagnons : 2) ; 82 EXPLICIT, 8 IMPLICIT, 4 AMBIGUOUS, 1 UNDEFINED ; confiance haute 72, moyenne 23 |
| Validation du schéma | 0 erreur (unicité, statuts, dépendances, notation canonique vide) ; 0 sélecteur vide ; 0 occurrence rattachée à plusieurs objets |
| Couverture des clés structurantes (≥ 5 occurrences, niveau 0) | Volume II 60,2 % ; volume I 35,3 % ; compagnons 28,8 % ; clés non résolues listées, principales classées à la main |
| Audit ρ | 4 objets distincts : 48 / 8 / 4 / 395 occurrences, reproduits |
| Symboles nouveaux dans V5.17 | Aucun glyphe nouveau dans la sous-section ajoutée ; 6 clés nouvelles ; 131 glyphes hors tableau V5.16, tous antérieurs à cette sous-section |
| Cas d'étude | d_ρ : UNDEFINED (A-G02-04) ; \mathcal R^{\mathfrak B,ρ} : AMBIGUOUS (A-G02-05) |
| Échantillon de contrôle | 30 rattachements : 28 corrects, 2 recevables avec réserve ; 24 tirages sur les sélecteurs larges cohérents |
| Addendum B2a | Attributs secondaires ajoutés ; non-régression contre `05afddd` : 0 différence |
| Intégrité des sources | `git diff c74fa04 -- Volume_I Volume_II` vide |


## Décisions rendues

| Id | Date | Décision |
|---|---|---|
| A1 | 27/11/2026 | Paquets manquants installés dans TeX Live 2026 via `tlmgr` |
| A1bis | 27/11/2026 | PDF de référence archivés en prépublication GitHub `g0-baseline` → `c74fa04` |
| A2 | 27/11/2026 | Base `c74fa04` acceptée ; branche `harmonisation/g0` validée ; commit et poussée autorisés ; pas de fusion dans `main` |
| A3 | 27/11/2026 | G0.1 autorisée après versionnement de G0.0 |
| B1 | 27/11/2026 | G0.1 validée ; livrables, scripts et tests committés et poussés sur `harmonisation/g0` (pas de fusion dans `main`) ; résultats d'extraction conservés comme **références de non-régression** |
| B2a | 27/11/2026 | Classe `composite` acceptée ; elle peut porter sur l'indice, l'exposant ou les deux ; classification principale déterministe et documentée ; attributs élémentaires (glyphe, police, indices, exposants, structure, liens) conservés ; catégorie principale distinguée des attributs secondaires |
| B2b | 27/11/2026 | Regroupement des polices dans une même famille lexicale accepté ; les formes restent distinctes ; une même famille n'implique **aucune** identité ni proximité sémantique |
| B3 | 27/11/2026 | Localisation par section et empreinte acceptée pour les occurrences sans label ; aucun label ajouté aux manuscrits ; ajout éventuel de labels aux définitions structurantes du volume II inscrit comme amélioration documentaire à examiner en G0.7 (R-G0-09) |
| B4 | 27/11/2026 | Extraction Markdown limitée acceptée ; compagnons = corpus auxiliaire distinct, mobilisable avec provenance explicite ; pas d'analyseur Markdown exhaustif |
| B5 | 27/11/2026 | G0.2 autorisée après clôture de G0.1, ordre G0.2a–f imposé ; registre **candidat**, non normatif ; arrêt avant G0.3 |
| C1 | 27/11/2026 | G0.2 acceptée comme **première itération** ; commit et poussée autorisés (livrables, B2a, tests) ; tag `g0.1-inventaire-ref` poussé après vérification de sa cible (`05afddd`) ; registre qualifié de candidat **intermédiaire** ; état de référence des 95 objets conservé ; pas de fusion dans `main` |
| C2 | 27/11/2026 | « Fibre d'opacité » : deux objets distincts, « fibre d'opacité complète » (l. 185) et « fibre d'opacité admissible au flot » \mathcal O_y (l. 863), reliés par O_y = ρ_X^{-1}(y)∩C = (ρ_X\|_C)^{-1}(y) ; égalité non présumée ; désignations provisoires, arbitrage terminologique en G0.5 ; aucun manuscrit modifié |
| C3 | 27/11/2026 | Correspondance intervolumes non limitée aux objets instruits ; ouverture de **G0.2bis** (complétude et consolidation) : lecture intégrale du volume I, complétude du volume II, environnements formels, matrice de couverture documentaire, classement des non-rattachés, différentiel ; pas de pourcentage lexical cible |
| C4 | 27/11/2026 | JSON compatible YAML recevable pour le registre intermédiaire ; PyYAML autorisé dans un environnement virtuel dédié, version épinglée, dépendance documentée ; YAML lisible privilégié pour le registre pérenne ; conversion à vérifier sans perte ; aucune installation globale |
| C5 | 27/11/2026 | G0.3 **non autorisée** avant validation de G0.2bis et clôture de G0.2 |

## Réserves

| Id | Description | Statut | Échéance / décision |
|---|---|---|---|
| R-G0-01 | Plan § 2.3 : trois commits qualifiés d'« arbres » | Corrigée par erratum E1 (`ERRATA_PLAN_G0.md`) | — |
| R-G0-02 | Compilations de référence impossibles dans l'environnement initial | Clôturée | — |
| R-G0-03 | `latexmk` du `PATH` relève de MiKTeX | Traitée : chaîne de référence TeX Live 2026 documentée (manifeste § 3.4) | — |
| R-G0-04 | Provenance inconnue ou seulement candidate pour 4 figures de II et 5 de I | Reportée | G0.7 (sous-chantier figures) |
| R-G0-05 | `make_fig_walls_control.py` l. 42 ; PNG de `make_fig_recursive.py` non produit | Reportée | G0.7 |
| R-G0-06 | `planche_I_sillon.tex` sans préambule | Reportée | G0.7 |
| R-G0-07 | Volume II : 8 avertissements hyperref | Conservée, cosmétique | — |
| R-G0-08 | README Lean : ventilation 901 pour 905 audités | Reportée, sans intervention Lean | G0.8 |
| R-G0-09 | Volume II : 19 labels seulement ; 37 % des occurrences sans label pertinent | Amélioration documentaire, non bloquante | G0.7 (B3) |
| R-G0-10 | Lecture partielle du volume I en G0.2 (couverture 35 %) | Traitée en G0.2bis (C3) | G0.2bis |
| A-G02-01 à 07 | Anomalies sémantiques G0.2 (détail dans `RESERVES.md`) | Ouvertes, non corrigées | Auteur |

Aucune réserve n'est bloquante en l'état ; A-G02-01 et R-G0-10 conditionnent la qualité de G0.3.

## Prochaine action

G0.2bis en cours ; arrêt avant G0.3.

