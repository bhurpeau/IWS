# G0 — État d'avancement

**Dernière mise à jour :** 27 novembre 2026
**Phase courante :** G0.0 **clôturée et validée** ; G0.1 autorisée (A3)
**Commit de base :** `c74fa047171ff51e308f1855d8f636add2ac33ca` (IWS, tag `g0-baseline`)
**Branche de travail :** `harmonisation/g0` (poussée sur `origin`, non fusionnée dans `main`)
**Dernier commit de travail :** voir `git log harmonisation/g0` (commit de clôture G0.0)
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
| G0.1 | Autorisée, en cours | — |
| G0.2 – G0.9 | Non entamées | — |

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

## Décisions rendues

| Id | Date | Décision |
|---|---|---|
| A1 | 27/11/2026 | Paquets manquants installés dans TeX Live 2026 via `tlmgr` |
| A1bis | 27/11/2026 | PDF de référence archivés en prépublication GitHub `g0-baseline` → `c74fa04` |
| A2 | 27/11/2026 | Base `c74fa04` acceptée ; branche `harmonisation/g0` validée ; commit et poussée autorisés ; pas de fusion dans `main` |
| A3 | 27/11/2026 | G0.1 autorisée après versionnement de G0.0 |

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

Aucune réserve n'est bloquante pour G0.1.

## Prochaine action

Exécuter G0.1 (inventaire lexical) selon `PLAN_G0.md` § 5 et les exigences complémentaires de A3 ; s'arrêter avant G0.2.
