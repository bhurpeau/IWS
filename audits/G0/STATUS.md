# G0 — État d'avancement

**Dernière mise à jour :** 28 novembre 2026
**Phase courante :** G0.3 **clôturée** (E1) ; G0.4 **en cours** (E7)
**Commit de base :** `c74fa047171ff51e308f1855d8f636add2ac33ca` (IWS, tag `g0-baseline`)
**Branche de travail :** `harmonisation/g0` (poussée sur `origin`, non fusionnée dans `main`)
**Dernier commit de travail :** `3e837cb` (G0.2bis, clôture de G0.2, référence 301 entrées ; poussé) ; G0.3 : commit « G0.3 » (registre 305 entrées, table figée)
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
| G0.2 | **Clôturée le 28/11/2026 (D1)** | `notations/registry.yaml` (registre candidat **intermédiaire** ; itération 1 : 95 objets, copie figée `G0_02_semantic/reference_95/`), `G0_02_objects_report.md`, `RESERVES.md`, `G0_02_semantic/`, scripts `definition_sites.py`, `link_registry.py` ; addendum G0.1 (B2a) et `check_regression.py` |
| G0.2bis | **Validée, clôturée (D1)** | registre candidat intermédiaire, itération 2 (301 objets, YAML style bloc) ; `G0_02bis_completeness_report.md` ; `G0_02bis/` (journal de lecture, matrice de couverture, énoncés formels, classement des non-rattachés, revue des sites de définition, différentiel, échantillon) ; `RESERVES.md` ; scripts `registry_io.py`, `formal_environments.py`, `coverage_matrix.py`, `classify_unresolved.py`, `registry_diff.py`, tests |
| G0.3 | **Validée, clôturée (E1)** | `notations/crosswalk.csv` (généré), `notations/crosswalk_relations.yaml` (source), `G0_03_crosswalk_report.md`, `G0_03_crosswalk/` (bilan par objet, décomptes, recalcul D2), script `build_crosswalk.py`, tests |
| G0.4 – G0.9 | Non entamées | — |

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


## Résultats des contrôles G0.2bis

| Contrôle | Résultat |
|---|---|
| Lecture | Volume I lu intégralement et journalisé (livres I–III, annexes A–L, table des énoncés) ; volume II : 31 énoncés et sites non couverts relus ; compagnons lus intégralement ; 390 unités de la matrice de couverture lues intégralement, 0 non lue |
| Registre | 301 objets (I : 205 ; II : 88 ; C : 8) ; 271 éléments, 30 familles ; 265 EXPLICIT, 28 IMPLICIT, 5 AMBIGUOUS, 3 UNDEFINED |
| Schéma | 0 erreur (y compris granularité et réciprocité famille ↔ composants) ; 0 rattachement multiple ; 0 sélecteur vide |
| Couverture des clés structurantes | Volume I 69,9 % ; volume II 63,8 % ; compagnons 50,8 % (indicatif, non visé) |
| Non-rattachés | Toutes les clés structurantes non rattachées classées ; 0 objet structurant non instruit, 0 usage non résolu ; 50 clés à usage ambigu (R-G0-12) |
| Sites de définition | 198 passages non couverts revus et classés (`definition_sites_review.csv`) |
| Différentiel | 95 identifiants de référence conservés ; 206 ajoutés ; 16 décompositions ; 1 changement de statut (C2) |
| Format (C4) | YAML style bloc, PyYAML 6.0.2 en environnement `.venv-g0` ; conversion sans perte (0 écart) |
| Non-régression | Inventaire G0.1 : 0 différence ; référence 95 objets inchangée ; 27 tests verts |
| Échantillon | 40 rattachements : 38 corrects, 2 recevables avec réserve |
| Intégrité des sources | `git diff c74fa04 -- Volume_I Volume_II` vide ; dépôts connexes non modifiés |

## Résultats des contrôles G0.3

| Contrôle | Résultat |
|---|---|
| Table | 82 relations intervolumes à la remise (46 établies, 33 candidates, 3 indéterminées) ; après E2–E6 : 86 (50 établies, 33 candidates, 3 indéterminées) + 2 intravolume établies (R001, R002) |
| Couverture | 301 objets sur 301 avec bilan ; volume I : 21 correspondants établis, 10 candidats, 3 indéterminés ; volume II : 32 établis, 12 candidats, 1 indéterminé ; « sans correspondant identifié » motivé par groupe (non preuve d'absence) |
| Cohérence | 0 erreur (identifiants, codes, orientation, contradictions, NEW contre identification, propagation de familles) |
| D2 | Recalcul reproduit : c₁ = −2,1779, c₂ = 0,3220 ; annulation exacte des termes en m₂ ; occurrences et dépendances recensées |
| Non-régression | Registre identique à `reference_301` ; inventaire G0.1 : 0 différence ; 30 tests verts ; sources et dépôts connexes inchangés |

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
| D1 | 28/11/2026 | G0.2bis **validée**, G0.2 **clôturée** ; commit et poussée autorisés sur `harmonisation/g0` (pas de fusion dans `main`) ; état intermédiaire des 95 objets conservé ; nouvel état de référence des 301 entrées figé (`G0_02_semantic/reference_301/`) ; le registre reste candidat, non normatif |
| D2 | 28/11/2026 | Coefficients de la branche résistante : recalcul indépendant (annexe D, paramètres de l'annexe F) : c₁ = −2,1779, c₂ = 0,3220 ; la valeur 0,3216 (livre II) et le coefficient linéaire −2,1774 sont à corriger ultérieurement ; recalcul à reproduire et tracer ; occurrences et dépendances à recenser ; annulation exacte des contributions en m₂ à documenter ; corrections numériques distinguées des corrections notationnelles ; aucun manuscrit modifié |
| D3 | 28/11/2026 | Appropriation : deux entrées conservées ; correspondance des deux définitions à instruire en G0.3 (prédicats coïncidant par substitution de y_T et renommage de l'attracteur final, sous réserve des domaines et de la dynamique autonome), sans identité inconditionnelle ni généralisation stricte présumées ; conditions de validité à documenter |
| D4 | 28/11/2026 | Homonymies internes : relèvent de G0.4 ; en G0.3, un blocage dû à une homonymie est documenté et la relation est UNK |
| D5 | 28/11/2026 | Les 50 clés ambiguës relèvent de G0.4 ; G0.3 ne résout que les ambiguïtés indispensables à une correspondance ; occurrences non résolues et provenance préservées |
| D6 | 28/11/2026 | G0.3 autorisée après clôture, commit et poussée de G0.2 ; exécuter exclusivement G0.3 selon `PLAN_G0.md` ; relations ID, GEN, SPEC, PROJ, DER, ANA, DIST, UNK, NEW orientées ; arrêt avant G0.4 |
| E1 | 28/11/2026 | G0.3 **validée** sous réserve de l'intégration de E2–E6 (faite) ; commit et poussée autorisés ; pas de fusion dans `main` ; registre de 301 entrées conservé comme référence historique ; enrichissements documentés ; table figée après arbitrages (`G0_03_crosswalk/reference_E/`) |
| E2 | 28/11/2026 | X002 maintenue **candidate** ; spécimen (X001) distingué de la démonstration de l'appartenance à \Hyb (raccord H1–H4 / invariance d'admissibilité / annexe A) ; réserve de recherche du volume II R-G0-15 ; aucune démonstration en G0 |
| E3 | 28/11/2026 | \mathcal X réservé aux états complets ; pas d'identification globale de \mathfrak X à \mathcal X ; généralité de \mathfrak X préservée ; X043, X044 maintenues UNK ; examen des occurrences de \mathfrak X en G0.4 (états d'un système fixé, réalisations, présentations, niveau indéterminé) et conséquences pour X010, X011, X026 ; arbitrage notationnel en G0.5 |
| E4 | 28/11/2026 | X026, X028, X029 maintenues candidates ; compatibilités de X026 documentées ; réserve explicite sur l'égalité des domaines d'histoires pour X028, X029 |
| E5 | 28/11/2026 | 4 entrées du volume II ajoutées par renvoi (Q, M, Γ, D du noyau) ; attribut `provenance_definition` (LOCAL, BY_REFERENCE, DERIVED) ; relations ID X083–X086 ; rôles de D distingués ; registre de 305 entrées figé (`reference_305/`) |
| E6 | 28/11/2026 | R001 : identité conditionnelle établie entre les prédicats (C1–C4), domaines d'application non identifiés, deux entrées conservées ; R002 : équivalence conditionnelle acceptée pour le noyau (P⁻=Θ), non étendue à R2, différence hors de P⁻=Θ sauf r_P=0 |
| E7 | 28/11/2026 | G0.4 autorisée après intégration, clôture, commit et poussée de G0.3 ; exécuter exclusivement G0.4 ; arrêt avant G0.5 |

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
| R-G0-10 | Lecture partielle du volume I en G0.2 (couverture 35 %) | Levée en G0.2bis (lecture intégrale journalisée) | Validation G0.2bis |
| R-G0-11 | Motifs de fichier non ancrés dans les sélecteurs de G0.2 | Corrigés en G0.2bis, effet documenté | — |
| R-G0-12 | 50 clés à usage ambigu partiellement non rattachées | Documentée | G0.4 (D5) |
| A-G02-01 à 15 | Anomalies sémantiques (détail dans `RESERVES.md`) ; 01 instruite (C2), 03 et 08 instruites en G0.3 (R001, R002), 07 requalifiée, 14 instruite (D2), 15 nouvelle (annulation exacte en m₂) | Ouvertes, non corrigées | Auteur |
| R-G0-13 | Registre du volume II sans entrées pour Q, M, Γ, D cités par renvoi | Traitée (E5) | — |
| R-G0-15 | Appartenance du noyau à \Hyb (réserve de recherche du volume II) | Ouverte, recherche | Auteur |
| R-G0-16 | Reset de pression : portée R2 non instruite | Ouverte | Auteur |
| R-G0-14 | 33 correspondances candidates et 3 indéterminées | Ouverte | Auteur (G0.3 → G0.5) |

Aucune réserve n'est bloquante en l'état. A-G02-03 (appropriation), A-G02-10 et A-G02-13 (variantes notationnelles) ainsi que R-G0-12 (usages ambigus) conditionnent la lecture de G0.3.

## Prochaine action

G0.4 en cours (E7) ; arrêt avant G0.5.

