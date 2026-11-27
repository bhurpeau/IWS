# G0.0 — Manifeste des sources et état initial

**Phase :** G0.0 (gel des sources et préparation)
**Date d'exécution :** 27 novembre 2026
**Plan de référence :** `audits/G0/PLAN_G0.md`, version 2.0 (SHA-256 `241b11944332ec0a9a53c863a40dc6d7f97f8cfd94ac7d97dbe933913545e07c`)
**Branche de travail :** `harmonisation/g0`, créée sur le commit de base `c74fa04`
**Statut :** **validé** par l'auteur le 27 novembre 2026 (décisions A1bis, A2, A3, § 10).
**Révision :** 27 novembre 2026 — compilations de référence réalisées après installation des paquets manquants (arbitrage A1 : `tlmgr`), § 3.2 et 3.4.

Conventions de ce document :

- **[CTRL]** contrôle réalisé, avec son résultat observé ;
- **[IMPOSSIBLE]** contrôle tenté ou prévu, non réalisable dans l'environnement ; cause indiquée ;
- **[CONSTAT]** fait établi par lecture directe des dépôts ou des journaux ;
- **[HYP]** hypothèse ou interprétation non vérifiée.

Aucune notation, définition, équation, hypothèse, démonstration ou conclusion mathématique n'a été modifiée. Les dépôts `iws-lean`, `IWS_minimality_package` et `IWS_1` ont été consultés en lecture seule.

---

## 1. Versions de référence des dépôts

[CTRL] Pour chaque dépôt : `git rev-parse HEAD` et `HEAD^{tree}`, `git ls-remote origin`, état de l'arbre de travail. Les quatre copies locales sont sur `main`, identiques à `origin/main` au moment du contrôle, sans modification suivie non validée (seuls des fichiers ignorés : `.DS_Store`, `.lake/`, `CLAUDE.md` côté Lean).

| Dépôt | Branche | Commit (SHA complet) | Arbre Git | Date du commit | Tags pertinents |
|---|---|---|---|---|---|
| IWS | `main` | `c74fa047171ff51e308f1855d8f636add2ac33ca` | `dfb3eb26c7c6d418065d755f3b3b70c4ecd6d3b4` | 2026-11-27 12:06 +0100 — « Add G0 plan » | aucun |
| iws-lean | `main` | `e9fb1a6728e458ab14aee37560633c27c5dbea03` | `dd8d510e35f192c1d8d08fd1be9c0e0cf969bf9d` | 2026-11-26 21:03 +0100 — Annexe D, reste O(δ³) | `annex-d-certified-v4.36.0` (annoté, pointe sur HEAD) ; `annex-c-certified-v4.36.0` → `a9b7fc1` ; `annex-a-certified-v4.33.1` → `e1dcb10` |
| IWS_minimality_package | `main` | `b1a973842eae11d1dc9bed83f49a14b530e772d7` | `77f2ba52f1973863ca22cd120370b4e1776001f8` | 2026-10-20 15:27 +0200 — « Add finite-depth transmission certificates » | aucun |
| IWS_1 | `main` | `42402339f3b2da3371d0a188a5d9583eb8932e5b` | `b761145cf9b9a295a339c8dfed15938c5f545a04` | 2026-07-17 23:58 +0200 — F-III.13 | `V0` (ne pointe pas sur HEAD) |

**Gel proposé.** Commit de base du dépôt principal : `c74fa04`. Les travaux G0 sont portés par la branche locale `harmonisation/g0` (non poussée). Les trois autres dépôts sont référencés par les commits ci-dessus ; aucun tag n'a été créé.

### 1.1. Correction d'un constat du plan (§ 2.3)

[CONSTAT] Les identifiants présentés dans le plan comme des « identifiants d'arbre » sont en réalité des **commits** (`git cat-file -t` → `commit`) :

| Identifiant cité dans le plan | Nature réelle | Dépôt |
|---|---|---|
| `8cdf171a056203268f5dde545a65e691220409d0` | commit « Reorg » | IWS |
| `22e14626de715b3a88783f55f89b662594ee9171` | commit « First commit » | IWS |
| `b1a973842eae11d1dc9bed83f49a14b530e772d7` | commit, actuel HEAD | IWS_minimality_package |

La correction est tracée par l'erratum E1 (`ERRATA_PLAN_G0.md`), avec renvoi inséré dans le § 2.3 du plan ; le texte du plan n'est pas réécrit.

### 1.2. Évolution depuis les commits inspectés antérieurement

[CTRL] `git diff --stat 22e1462 c74fa04 -- Volume_I Volume_II` : **aucune modification de `Volume_I/`** ; dans `Volume_II/`, seules la suppression de la source redondante `IWS_Volume_II_V5_17_source_corrige.tex` (1918 lignes) et celle du PDF V5.17 (1,5 Mo). `8cdf171..c74fa04` ne touche que `README.md` et `audits/G0/PLAN_G0.md`.

[CONSTAT] Conséquence : les sources du volume I sur lesquelles l'audit historique des 455 occurrences de `\rho` a été recompté (`22e1462`) sont identiques octet pour octet à celles du commit gelé. Le recomptage lui-même relève de G0.1.

---

## 2. Manifeste des sources actives

[CTRL] Résolution récursive des `\input`, `\include`, `\includegraphics`, de la macro `\planche` du volume I et des bibliographies, commentaires LaTeX retirés, `\graphicspath` pris en compte ; script `G0_00_controls/manifest.py`, sorties `manifest_volI.json` et `manifest_volII.json` (empreintes SHA-256, labels, macros, paquets). Le journal `-recorder` (`.fls`) des compilations de diagnostic confirme la liste des fichiers lus.

Résultats :

- [CTRL] Volume I : 1 document maître, 3 livres, 12 annexes, `TABLE_ENONCES.tex`, 1 bibliographie ; profondeur d'inclusion 1 (aucune inclusion imbriquée) ; **aucun fichier manquant** ; aucune inclusion commentée ; 473 `\label` littéraux (le relevé brut de 475 compte aussi les paramètres `#1`, `#2` des macros `\resultheading` et `\resultstep`), auxquels s'ajoutent 52 labels posés par ces macros ; **525 labels effectifs** dans le `.aux` de référence, **aucun dupliqué**.
- [CTRL] Volume II : **une seule source maîtresse** (`IWS_volume_II_classe_objets_transformations_v5_17.tex`, autonome, sans `\input`) ; aucune bibliographie externe ; 7 figures, toutes résolues via `\graphicspath{{fig/}}` ; 19 `\label`, aucun dupliqué ; 7 appels `\ref`.
- [CONSTAT] Aucun autre fichier `.tex` du dépôt ne peut être confondu avec la source canonique du volume II : la source redondante a bien disparu de l'arbre.

### 2.1. Classification

| Catégorie | Contenu |
|---|---|
| Manuscrits | Volume I : `main.tex` et ses 16 fichiers inclus + `.bib` ; Volume II : source V5.17 |
| Compagnons actifs (hors manuscrit) | `Volume_II/NOTES_V5_17.md` ; `Volume_II/preuves_compagnons/` : `certification_huit_episodes_V2.tex`, `transmission_profondeur_finie_V2.tex` (documents `article` autonomes), `audit_cauchy_lemme_V2.md` |
| Illustrations | Volume I : 3 planches PDF (via `\planche`), 5 figures scientifiques ; Volume II : 7 PNG |
| Sources d'illustrations non incluses | `Volume_I/fig/planche_*.tex` (sources TikZ des planches PDF) |
| Audits historiques (non modifiés) | `audits/diag_rho_volI.md`, `audits/IWS_VolII_audit_notations_v5_16.md` |
| Pilotage G0 | `audits/G0/` |
| Fichiers générés | aucun versionné (`.aux`, `.log`, PDF des volumes absents de l'arbre) ; diagnostics produits hors dépôt |
| Exclusions | `.DS_Store` (ignorés) ; dépôts expérimentaux et Lean (consultation seule) ; `notations/` vide (`.keep`) |

### 2.2. Empreintes

#### Volume_I — manuscrit

| Fichier | Inclus par | Lignes | Labels | SHA-256 |
|---|---|---:|---:|---|
| `Volume_I/main.tex` | — (maître) | 326 | 14 | `7aa3b2ae69491c35f94283de3b214927de62013d79fb77c69a0c7ae2b6d9e6de` |
| `Volume_I/IWS_PART_I.tex` | `main.tex` | 1459 | 48 | `14b04918ee60e0a2199b6eb66b2a75609ad5c53c974a22c7f87e8e89e43972c4` |
| `Volume_I/IWS_PART_II.tex` | `main.tex` | 1858 | 69 | `7a960b50f9eae2ea3b13811f7d67259ed3c506f5c7534c869cdef81e6d701e99` |
| `Volume_I/IWS_PART_III.tex` | `main.tex` | 2413 | 53 | `5e7c42dcde0804fdf3bb3b3b36b2da0ed4999d44373d5d15a3d4eedef833245c` |
| `Volume_I/Annexes/IWS_ANNEXE_A.tex` | `main.tex` | 1191 | 21 | `069c0d852e60dc73c4bf24a3ad54809fef4329919cefd6ee72740d4dac6f0a78` |
| `Volume_I/Annexes/IWS_ANNEXE_B.tex` | `main.tex` | 1002 | 13 | `031fd65dc64c5ea34c86ab372a1312e7731e87a157c58f62938270182c966e0d` |
| `Volume_I/Annexes/IWS_ANNEXE_C.tex` | `main.tex` | 1955 | 21 | `58f1705fbff62ed4facfcd9a2527686ff7ad5658f308de1f53662d340b6b1b2b` |
| `Volume_I/Annexes/IWS_ANNEXE_D.tex` | `main.tex` | 2093 | 27 | `3cc52bfe10a3dfdd64f9b99ee03ecc6580512af5e0fcd0d17add56a407edc61d` |
| `Volume_I/Annexes/IWS_ANNEXE_E.tex` | `main.tex` | 1687 | 27 | `bacce928084c9fa0c19ef2d44a0b07f0e68efa75695febdeff8da62ab5d48ec5` |
| `Volume_I/Annexes/IWS_ANNEXE_F.tex` | `main.tex` | 1386 | 32 | `f00e68d51979b0ef6bd376a96cc4c001a4d082722c68b54bddcfc2958b20329b` |
| `Volume_I/Annexes/IWS_ANNEXE_G.tex` | `main.tex` | 963 | 32 | `cbc1219ef2aee6c94d2efa5a79ea054fbc2c5aea744bef59355577dffab93206` |
| `Volume_I/Annexes/IWS_ANNEXE_H.tex` | `main.tex` | 882 | 41 | `a096cb29d3af0734e73ae68c577289cee91185841ea1277ec8ca3f01146553d5` |
| `Volume_I/Annexes/IWS_ANNEXE_I.tex` | `main.tex` | 582 | 23 | `6d444bc4a9c37cddca022c3ad07a6095f63727c8ec22d0f0392f53c0da885038` |
| `Volume_I/Annexes/IWS_ANNEXE_J.tex` | `main.tex` | 521 | 19 | `f8bc3e6c547554da0bed8f1cf97015e84a71ca6b57ef67b9a78c5a573d617346` |
| `Volume_I/Annexes/IWS_ANNEXE_K.tex` | `main.tex` | 487 | 15 | `27a3c97f5b2776325a53e760c4afd53a5168acaacb750483b47acaccad192021` |
| `Volume_I/Annexes/IWS_ANNEXE_L.tex` | `main.tex` | 519 | 20 | `9fedc13bd8cd7c45835bafbd8e15ba71f79ad27fe9461c2423cebe5e60a6827c` |
| `Volume_I/TABLE_ENONCES.tex` | `main.tex` | 89 | 0 | `03a850ce606f6d3bd2d6712f340220e6ec4d3dfad535cd1124424bf2ee08c86b` |
| `Volume_I/IWS_TOME_I_II_REFERENCES.bib` | `main.tex` (bibliographie) | — | — | `6476866181a9ed13e3a549d150b285bf35a665d2067b40450312a4d0c95d621f` |

#### Volume_I — figures référencées

| Fichier | Appel | Source:ligne | SHA-256 |
|---|---|---|---|
| `Volume_I/fig/planche_I_sillon.pdf` | `planche` | `main.tex:186` | `36adfc0a106f4f136069449972910f98188f022fbf0253569a619e5cc6c0d2ad` |
| `Volume_I/fig/planche_II_reste.pdf` | `planche` | `main.tex:200` | `2e2874cae90c52a7edb04c7d6bfcc1f3e1feca375eb7632b28f8c42e99204dab` |
| `Volume_I/fig/planche_III_question.pdf` | `planche` | `main.tex:215` | `5f3dac6393c37b2e5fdc23d84e96436626b2a5eecdcc166b561ffe4d8a9b8a8e` |
| `Volume_I/fig/scientifiques/figure_trois_seuils.pdf` | `includegraphics` | `IWS_PART_II.tex:614` | `7a7cd54a962d829133937373775d6706a85d1df010c1dbec1098acaba47b829e` |
| `Volume_I/fig/scientifiques/figure_duree_appropriation.pdf` | `includegraphics` | `IWS_PART_II.tex:764` | `b785c204f5966c63878fbba3d237ab2fef6ecb68d05a310166e4333c7bd1ae01` |
| `Volume_I/fig/scientifiques/figure_frontiere_reponse.png` | `includegraphics` | `IWS_PART_III.tex:1703` | `c22285ab19c8edd5bc8625d55e0609777a6a35bd50e966c1a7a5accc91920a85` |
| `Volume_I/fig/scientifiques/figure_raccord_frontiere.png` | `includegraphics` | `IWS_PART_III.tex:2178` | `a24918f3ce4defa22a9e5be392f0437edd4b54a2fc4c1f26eaec45c29e4e27eb` |
| `Volume_I/fig/scientifiques/figure_separabilite_budgets.png` | `includegraphics` | `IWS_PART_III.tex:2392` | `a112cd8b56dbbf7a0471d464400711691c8c4c50ce5e9497b105ff125a2b5041` |

#### Volume_I — fichiers présents non inclus

| Fichier | SHA-256 |
|---|---|
| `Volume_I/fig/planche_III_question.tex` | `bbfb08c001d23cc6a66b41115480c9371aa5c8b96cf902d71d827ecfd8595ba4` |
| `Volume_I/fig/planche_II_reste.tex` | `4dd9af60e0aa8203f3b2b91ca4da6bb4b3135b67af49c3db1ee171286bd5f3a4` |
| `Volume_I/fig/planche_I_sillon.tex` | `2a1908e2d4c05ad215957d0547be668bf510ba41dee20ca4272950b495531bbf` |

#### Volume_II — manuscrit

| Fichier | Inclus par | Lignes | Labels | SHA-256 |
|---|---|---:|---:|---|
| `Volume_II/IWS_volume_II_classe_objets_transformations_v5_17.tex` | — (maître) | 1925 | 19 | `f11fb4bb7725d840de30d4c8e1e4c98ea91c9011b55449afbe7aac363af6d50f` |

#### Volume_II — figures référencées

| Fichier | Appel | Source:ligne | SHA-256 |
|---|---|---|---|
| `Volume_II/fig/opacity_walls_protocol_control.png` | `includegraphics` | `IWS_volume_II_classe_objets_transformations_v5_17.tex:969` | `0fa4328b65b05f235f9157546fd2cedf52a85862495f93c5d90f28f88edfb604` |
| `Volume_II/fig/opacity_adaptive_refinement.png` | `includegraphics` | `IWS_volume_II_classe_objets_transformations_v5_17.tex:1008` | `aaac7c88328282b4d8b82a65b0dd1a30d3f0b2a52486e7a3980469d7cd97da93` |
| `Volume_II/fig/opacity_recursive_refinement.png` | `includegraphics` | `IWS_volume_II_classe_objets_transformations_v5_17.tex:1033` | `9c3cf9946014635b23cc0dc20657328226ff5ed47afcc6c4aa0ef8f0eca42d8a` |
| `Volume_II/fig/reachability_joint_N9.png` | `includegraphics` | `IWS_volume_II_classe_objets_transformations_v5_17.tex:1253` | `be2939a7b92be48a664138e341f35afe2700b70819103a1c7bebb3f2fe465242` |
| `Volume_II/fig/margin_first_crossing_N9.png` | `includegraphics` | `IWS_volume_II_classe_objets_transformations_v5_17.tex:1290` | `fb61ed85dfdc7db901b247f64ce7bc7a6591668a4b3807372a5d963a60da7864` |
| `Volume_II/fig/active_walls_site2_bas_r4.png` | `includegraphics` | `IWS_volume_II_classe_objets_transformations_v5_17.tex:1378` | `1913104ab78ec7d6880e69984d51441dfac6dd25eb5d758bb27395333d9ce31f` |
| `Volume_II/fig/structural_wall_fixsigma.png` | `includegraphics` | `IWS_volume_II_classe_objets_transformations_v5_17.tex:1395` | `f9d0b2e854eb8a8fadb6bea6199b6fe50b03a4df3779c5221b75bf58ca8bc424` |

#### Volume_II — fichiers présents non inclus

| Fichier | SHA-256 |
|---|---|
| `Volume_II/NOTES_V5_17.md` | `c98c1bec6c16249f434d16f967dfcc1ff0855e38abe1a0b622aeb1a29e7dccf4` |
| `Volume_II/preuves_compagnons/audit_cauchy_lemme_V2.md` | `0a2fc7cc844dca05f7603da48c13971992e1c8ba7624d33478861f0f9488cc92` |
| `Volume_II/preuves_compagnons/certification_huit_episodes_V2.tex` | `a1ed397f6ae08f2b35ce6ec31c0d7018c3fae73c6a3851184dcb17f46cda2998` |
| `Volume_II/preuves_compagnons/transmission_profondeur_finie_V2.tex` | `0a3f255885e7aed1cf6b5c522fa07c6cae69e3e8268f3310466612c6920bcdda` |

#### Compagnons et audits

| Fichier | SHA-256 |
|---|---|
| `Volume_II/NOTES_V5_17.md` | `c98c1bec6c16249f434d16f967dfcc1ff0855e38abe1a0b622aeb1a29e7dccf4` |
| `Volume_II/preuves_compagnons/audit_cauchy_lemme_V2.md` | `0a2fc7cc844dca05f7603da48c13971992e1c8ba7624d33478861f0f9488cc92` |
| `Volume_II/preuves_compagnons/certification_huit_episodes_V2.tex` | `a1ed397f6ae08f2b35ce6ec31c0d7018c3fae73c6a3851184dcb17f46cda2998` |
| `Volume_II/preuves_compagnons/transmission_profondeur_finie_V2.tex` | `0a3f255885e7aed1cf6b5c522fa07c6cae69e3e8268f3310466612c6920bcdda` |
| `audits/diag_rho_volI.md` | `5bc969b1c9d7f444615c729d03d2de81d2052ccaf90a80b9999300b5cca9518c` |
| `audits/IWS_VolII_audit_notations_v5_16.md` | `d3de397dd55dab47e62b6df6759069958ebebdef35ce4881a7f42ac1d694626e` |

### 2.3. Préambules, macros et paquets

[CTRL] Volume I (`book`, 11pt, a4) : `natbib` + BibTeX (`unsrt`, 13 entrées, 13 citées, aucun avertissement BibTeX), `tcolorbox[most]` (environnement `encadre`, 42 usages dans I et G–L), `appendix`, `babel` avec `\babelprovide{french}`, `xurl`, `selnolig` sous `\ifLuaTeX` uniquement. Macros définies : 12 dans `main.tex` (`\resultheading`, `\resultstep`, `\planche`, `\tome`, `\tightlist`…), redéfinitions locales de `\labelenumi` (5, livres I et II), `\arraystretch` (table des énoncés). **Aucune macro mathématique sémantique** n'est définie dans le volume I.

[CTRL] Volume II (`article`, 11pt, a4) : `babel[french]`, `mathtools`, `mathrsfs`, `enumitem`, `tikz`, `graphicx`. 24 définitions : 9 environnements de type théorème (dont `proposition` intitulé « Proposition candidate » et `propositionthm` intitulé « Proposition ») et 15 macros (`\IWS`, `\Hyb`, `\X`, `\Sstruct`, `\M`, `\Madm`, `\Supp`, `\Reach`, `\End`, `\Word`, `\Rep`, `\Exec`, `\Id`, `\panelnodes`, `\commonkept`).

[CONSTAT] Les deux volumes ont des préambules disjoints ; aucun préambule commun n'existe. Le recensement sémantique de ces macros relève de G0.1–G0.2.

---

## 3. Compilations LaTeX

### 3.1. Environnement

[CONSTAT] Deux distributions coexistent sur la machine :

- TeX Live 2026 **BasicTeX** (`/Library/TeX/texbin`) : pdfTeX 3.141592653-2.6-1.40.29, BibTeX 0.99e ; pas de `latexmk` ni de `biber` ;
- MiKTeX : le `latexmk` présent dans le `PATH` est un lanceur MiKTeX (`runperl`) qui déclenche une maintenance de paquets à l'invocation.

[CONSTAT] `latexmk -pdf` n'a **pas** été utilisé : il aurait mélangé les deux distributions et pu installer des paquets à la volée (modification de l'environnement hors périmètre). Une seule invocation `latexmk -v` a été lancée pour identifier l'outil ; elle a affiché « starting package maintenance… ». Les compilations ont été faites avec `pdflatex` TeX Live, dans un répertoire de sortie hors dépôt, depuis le répertoire de chaque volume :

```bash
cd Volume_I && pdflatex -interaction=nonstopmode -recorder -output-directory=<BUILD> main.tex
cd Volume_II && pdflatex -interaction=nonstopmode -recorder -output-directory=<BUILD> IWS_volume_II_classe_objets_transformations_v5_17.tex
```

### 3.2. Premières tentatives (BasicTeX initial)

[CONSTAT] Dans l'environnement initial, **aucune compilation n'a abouti** : arrêt fatal à la première passe, faute de paquets absents de BasicTeX :

| Document | Premier arrêt | Paquets / ressources manquants (vérifiés par `kpsewhich`) |
|---|---|---|
| Volume I | `appendix.sty` not found | `appendix`, `tcolorbox`, `xurl` (`selnolig` absent mais non requis sous pdfTeX) |
| Volume II | `enumitem.sty` not found | `enumitem` ; polices `rsfs10` (TFM) pour `mathrsfs` |
| Compagnons (2 `.tex`) | `enumitem.sty` not found | `enumitem` |

Journaux : `G0_00_controls/logs/echec_basictex_*.log`. Arbitrage A1 rendu : installation dans TeX Live par `tlmgr`, exécutée par l'auteur (droits administrateur) : `appendix tcolorbox pdfcol tikzfill listingsutf8 environ trimspaces xurl enumitem rsfs standalone adjustbox collectbox currfile filemod gincltex`. Contrôle après installation : les 16 fichiers attendus sont trouvés par `kpsewhich` ; `tcolorbox` 6.10.0, `enumitem` 3.11.

[CONSTAT] Effet de bord : `mktexpk`/`mktextfm` ont tenté de générer des polices dans le cache utilisateur TeX Live (`~/Library/texlive/2026basic/texmf-var`) ; aucune écriture dans les dépôts (`git status` vérifié propre après chaque compilation).

### 3.3. Compilations de diagnostic (non-référence)

Pour détecter d'éventuelles anomalies indépendantes des paquets manquants, les volumes ont été recompilés avec des **paquets factices** placés en tête de `TEXINPUTS` (`G0_00_controls/diag_stubs/`) : `appendix` vide, `xurl` → `url`, `enumitem` sans effet (options de listes imprimées comme texte), `tcolorbox` réduit à un environnement `encadre` sans cadre, `mathrsfs` avec `\mathscr` ≡ `\mathcal`. **Ces PDF ne sont pas des PDF de référence** et ne sont pas conservés comme tels ; la typographie (y compris l'aspect de `\mathscr`) n'y est pas représentative.

| Document | Séquence | Sortie | Erreurs | Références / citations non définies | Autres avertissements |
|---|---|---|---|---|---|
| Volume I | pdflatex, bibtex, pdflatex ×2 | 305 pages | 0 | 0 / 0 | 2 overfull hbox, 7 underfull hbox |
| Volume II | pdflatex ×3 | 42 pages | 1, artefact du faux `enumitem` (`description[leftmargin=…]`, l. 331–332) | 0 | 8 « Token not allowed in a PDF string » (hyperref, math dans titres) |
| `certification_huit_episodes_V2` | pdflatex ×2 | 5 pages | 3, artefacts du faux `enumitem` (l. 49, 123, 130) | 0 | — |
| `transmission_profondeur_finie_V2` | pdflatex ×2 | 4 pages | 1, artefact du faux `enumitem` (l. 40) | 0 | — |

[CTRL] Toutes les erreurs observées sous diagnostic sont imputables aux paquets factices (texte placé avant le premier `\item`). Aucune erreur, référence ou citation non définie propre aux sources n'a été observée.

L'hypothèse formulée à ce stade (compilation sans erreur avec les vrais paquets) est **confirmée** par le § 3.4 ; les nombres de pages diffèrent légèrement (306 et 41 pages).

### 3.4. Compilations de référence

[CTRL] Moteur : pdfTeX 3.141592653-2.6-1.40.29, TeX Live 2026 (format du 2026-03-25), BibTeX 0.99e, `pdflatex` de `/Library/TeX/texbin` exclusivement (pas de `latexmk`, cf. R-G0-03). Sortie hors dépôt ; `git status` inchangé après compilation.

| Document | Séquence | Code de sortie | Pages | Erreurs | Réf. / citations non définies | « Rerun » | Avertissements |
|---|---|---|---:|---:|---|---:|---|
| Volume I (`main.tex`) | pdflatex, bibtex, pdflatex ×2 | 0 | 306 | 0 | 0 / 0 | 0 | 2 overfull, 7 underfull hbox ; BibTeX : 0 |
| Volume II (V5.17) | pdflatex ×3 | 0 | 41 | 0 | 0 / — | 0 | 8 hyperref « Token not allowed in a PDF string » (R-G0-07) |
| `certification_huit_episodes_V2` | pdflatex ×2 | 0 | 5 | 0 | 0 | 0 | 3 underfull hbox ; 1 spécificateur de flottant modifié |
| `transmission_profondeur_finie_V2` | pdflatex ×2 | 0 | 4 | 0 | 0 | 0 | — |
| `fig/planche_II_reste.tex` | pdflatex ×1 | 0 | 1 | 0 | — | — | — |
| `fig/planche_III_question.tex` | pdflatex ×1 | 0 | 1 | 0 | — | — | — |

Aucun « Missing character » dans les journaux. Les planches régénérées ont les mêmes dimensions de page que les PDF versionnés (424,522 × 341,53 pt et 221,73 × 221,73 pt) ; la comparaison visuelle n'a pas été faite.

Empreintes des PDF produits (indicatives : elles dépendent de la date de compilation, faute de `SOURCE_DATE_EPOCH` ; elles ne servent pas de critère de reproductibilité) :

| PDF | SHA-256 |
|---|---|
| Volume I `main.pdf` | `2904b4facb921d8638843941e7d790109734d0b57ce11830529a034ab6c63ed3` |
| Volume II | `63cc4055ecf34afa75d2c886c6b2e7049945be65cb641e49bc02f0d80b7c522c` |
| `certification_huit_episodes_V2.pdf` | `7c9e13a770904377dce229363ca6589ba6f2fcc64dbd35777e34d30a3beae6e7` |
| `transmission_profondeur_finie_V2.pdf` | `1b1d7216a11dfb5587d7cd53ae9a24444e601553650bb2f476a79763cddc02d5` |

[CTRL] Les PDF de référence ne sont pas versionnés dans l'arbre Git. Conformément à A1bis, ils sont archivés dans la **prépublication GitHub [« IWS — G0 Baseline »](https://github.com/bhurpeau/IWS/releases/tag/g0-baseline)** (tag annoté `g0-baseline` → commit `c74fa04`), avec un fichier `SHA256SUMS`. Empreintes contrôlées avant envoi, puis après téléchargement depuis la release (`shasum -a 256 -c SHA256SUMS` : 4/4 OK). Les PDF de diagnostic ne sont pas inclus. Copie locale de sauvegarde hors dépôt : `IWS_artifacts/g0-baseline/`, à côté des dépôts.

**Séquence de compilation de référence (TeX Live 2026 exclusivement)**, depuis la racine du dépôt, avec `TL=/Library/TeX/texbin` (ou le répertoire `bin` de TeX Live 2026) :

```bash
cd Volume_I && $TL/pdflatex main.tex && $TL/bibtex main && $TL/pdflatex main.tex && $TL/pdflatex main.tex
```

```bash
cd Volume_II && for i in 1 2 3; do $TL/pdflatex IWS_volume_II_classe_objets_transformations_v5_17.tex; done
```

```bash
cd Volume_II/preuves_compagnons && for f in certification_huit_episodes_V2 transmission_profondeur_finie_V2; do $TL/pdflatex $f.tex && $TL/pdflatex $f.tex; done
```

Paquets requis au-delà de BasicTeX : `appendix tcolorbox pdfcol tikzfill listingsutf8 environ trimspaces xurl enumitem rsfs` (et `standalone adjustbox collectbox currfile filemod gincltex` pour les planches). L'usage de `latexmk` ou de MiKTeX n'est pas couvert par cette référence.

[CTRL] Inventaire des labels issu des `.aux` de référence : `G0_00_controls/labels_volI.csv` (525 labels : 315 sections, 53 propositions, 52 sous-sections, 50 équations, 37 chapitres, 12 annexes, 5 figures, 1 chapitre non numéroté) et `labels_volII.csv` (19 labels : 8 figures, 8 définitions, 1 section, 1 sous-section, 1 table). Colonnes : label, numéro, page, type d'ancre hyperref. Concordance avec les sources : volume II, 19/19 ; volume I, 473 littéraux + 52 via macros, aucun label de source absent du `.aux`.

---

## 4. Figures et provenance

[CTRL] Les 15 figures référencées par les manuscrits existent (8 pour I, 7 pour II) ; empreintes en § 2.2. Recherche par nom de fichier dans `IWS_minimality_package` (commit `b1a9738`) et `IWS_1` (commit `4240233`), sans exécution d'aucun script.

| Figure (volume II) | Générateur identifié | Niveau de preuve |
|---|---|---|
| `opacity_adaptive_refinement.png` | `scripts/genealogie_n9/make_fig_adaptive.py` | [CONSTAT] nom de sortie identique (`../../output/…png`, dpi 150) |
| `opacity_recursive_refinement.png` | `scripts/genealogie_n9/make_fig_recursive.py` | [CONSTAT] le script n'écrit que le **PDF** ; la chaîne vers le PNG n'est pas établie |
| `opacity_walls_protocol_control.png` | `scripts/genealogie_n9/make_fig_walls_control.py` | [CONSTAT] nom de sortie identique (PNG dans `figures/`) ; la ligne 42 (`savefig` du PDF) contient un chemin mal construit (chaîne littérale `"str(_pathlib…"`), qui échouerait ou écrirait sous un nom aberrant |
| `active_walls_site2_bas_r4.png`, `structural_wall_fixsigma.png` | aucun ; `scripts/construction_temoin_Q/contour_active_walls*.py` contiennent les mots-clés mais aucun `savefig` | [HYP] candidats par mots-clés seulement |
| `reachability_joint_N9.png`, `margin_first_crossing_N9.png` | aucun | [IMPOSSIBLE] provenance non identifiée |

| Figure (volume I) | Provenance |
|---|---|
| `fig/planche_{I,II,III}_*.pdf` | [CONSTAT] sources TikZ présentes dans `fig/` (`planche_II` et `planche_III` : documents `standalone` ; `planche_I_sillon.tex` : fragment `tikzpicture` sans préambule). `planche_II` et `planche_III` recompilent sans erreur (§ 3.4) ; `planche_I` non recompilable en l'état |
| `fig/scientifiques/*` (5 fichiers) | [IMPOSSIBLE] aucun générateur trouvé dans les dépôts consultés |

[CONSTAT] Le libellé « chambre(s) » de `opacity_recursive_refinement.png`, signalé par l'audit V5.16, n'a pas été réexaminé (G0.7, sous-chantier figures). Aucune reproductibilité de figure n'a été testée.

---

## 5. Référence Lean (consultation seule)

[CTRL] Sur `iws-lean@e9fb1a6` : `lean-toolchain` = `leanprover/lean4:v4.36.0` ; `lakefile.toml` version de paquet `0.1.11`. Dépendances directes épinglées (`lake-manifest.json`) :

| Dépendance | Révision | Entrée |
|---|---|---|
| mathlib | `fc4f59e577feb1a4956671bc04ac18aaaf8cd842` | `v4.36.0` |
| LeanForControl | `21cb162342b7b93780136e7950fda6853886d39e` | même SHA |
| doc-gen4 | `b3ed25bf7905565f793c47f2a13737d742d96f14` | `v4.36.0` |
| checkdecls | `3d425859e73fcfbef85b9638c2a91708ef4a22d4` | non spécifiée |

[CTRL] Le fichier versionné `audits/AuditAxioms-lean-4.36.0.txt` (dernière modification au commit `e9fb1a6`) indique : « 905 théorèmes IWS audités ; axiomes utilisés : [Quot.sound, Classical.choice, propext] ; avec sorryAx : [] », suivi de 25 audits ciblés, tous sur ces trois axiomes. Le README Lean date le dernier `lake build` réussi au 26 novembre 2026 et détaille la répartition : 438 (A), 14 (interopérabilité), 35 (spectral), 12 (linéarisation et Chetaev), 2 (unicité et troncature), 276 (C), 124 (D).

[CONSTAT] La somme de ces postes vaut **901**, et non 905 (réserve R-G0-08). Le total 905 provient de la sortie d'audit elle-même ; l'écart porte sur la ventilation documentaire, non vérifiée par reconstruction.

[IMPOSSIBLE / non tenté] Reconstruction Lean et réexécution de l'audit : hors périmètre G0.0 (aucune modification ni build de `iws-lean`). Le bilan ci-dessus est **rapporté**, non reproduit.

---

## 6. README

[CTRL] Modifications documentaires de `README.md` sur la branche de travail, sans contenu scientifique :

- arborescence : retrait du PDF V5.17 absent, placement des audits sous `audits/`, ajout de `audits/G0/` et `notations/` ;
- liens vers `PLAN_G0.md`, `STATUS.md`, ce manifeste et `notations/` ; statut du chantier ;
- référence Lean précisée (commit `e9fb1a6`, tag `annex-d-certified-v4.36.0`) et mention que le bilan n'a pas été reconstruit ;
- prérequis LaTeX observés (paquets requis absents de BasicTeX).

[CONSTAT] Les liens vers les audits historiques pointaient déjà vers `audits/` ; le lien vers la source canonique V5.17 est valide ; aucune mention de la source redondante ne subsistait dans le README.

---

## 7. Anomalies préexistantes

| Id | Nature | Description | Impact G0 |
|---|---|---|---|
| R-G0-01 | Documentaire | Le plan § 2.3 qualifie trois commits d'« identifiants d'arbre » | **Corrigé** par l'erratum E1 tracé |
| R-G0-02 | Environnement | Compilations de référence initialement impossibles (paquets manquants) | **Clôturée** : paquets installés par `tlmgr`, compilations de référence réussies (§ 3.4) |
| R-G0-03 | Environnement | `latexmk` du `PATH` appartient à MiKTeX, distribution différente de `pdflatex` ; les commandes `latexmk -pdf` du README ne sont donc pas celles de la référence | **Traitée** : chaîne de référence TeX Live 2026 documentée (§ 3.4) |
| R-G0-04 | Figures | Provenance inconnue pour 2 figures du volume II et les 5 figures scientifiques du volume I ; seulement candidate pour 2 autres | **Reportée** au sous-chantier figures (G0.7) |
| R-G0-05 | Figures | `make_fig_walls_control.py` l. 42 : chemin de sauvegarde mal construit ; `make_fig_recursive.py` ne produit pas le PNG utilisé | **Reportée** à G0.7 ; dépôt expérimental non modifié |
| R-G0-06 | Figures | `planche_I_sillon.tex` est un fragment sans préambule : la chaîne vers `planche_I_sillon.pdf` n'est pas documentée | **Reportée** à G0.7 |
| R-G0-07 | Typographie | Volume II : 8 avertissements hyperref (mathématiques dans les titres de section, signets PDF) | Conservée comme réserve cosmétique |
| R-G0-08 | Documentaire (Lean) | README `iws-lean` : ventilation par annexe sommant à 901 pour un total audité de 905 | **Reportée** à G0.8 ; aucune intervention sur Lean à ce stade |

Aucune anomalie mathématique n'a été recherchée ni constatée en G0.0.

---

## 8. Pièces de contrôle

`audits/G0/G0_00_controls/` (texte uniquement, chemins locaux remplacés par `<BUILD>`, `<TMP>`, `<HOME>`) :

- `manifest.py` : script d'inclusion récursive (lecture seule) ; `python3 -I manifest.py Volume_I main.tex` ;
- `manifest_volI.json`, `manifest_volII.json` : fichiers, empreintes, figures, labels, macros, paquets, fichiers non inclus ;
- `diag_stubs/` : paquets factices du diagnostic (à ne jamais utiliser pour une compilation de référence) ;
- `logs/ref_*.log`, `ref_volI_bibtex.blg` : compilations de référence ; `logs/echec_basictex_*.log` : premières tentatives échouées ; `logs/diag_*.log`, `diag_volI_bibtex.blg` : diagnostics à paquets factices ;
- `labels_volI.csv`, `labels_volII.csv` : inventaire des labels issu des `.aux` de référence.

Aucun PDF (référence ou diagnostic) n'est versionné.

---

## 9. Porte de validation G0.0

| Critère du plan | État |
|---|---|
| Sources actives identifiées | Atteint |
| Source canonique unique (volume II) | Atteint |
| Commits figés | Atteint (base `c74fa04`, branche `harmonisation/g0` locale ; commits des trois autres dépôts relevés) |
| État initial documenté | Atteint |
| Compilations de référence | **Atteint** : les deux volumes et les deux compagnons compilent sans erreur ni référence non définie (§ 3.4) ; PDF archivés dans la [release `g0-baseline`](https://github.com/bhurpeau/IWS/releases/tag/g0-baseline) |

---

## 10. Décisions de validation (27 novembre 2026)

| Id | Décision |
|---|---|
| A1 | Installation des paquets manquants dans TeX Live 2026 par `tlmgr` (exécutée par l'auteur) |
| A1bis | Conservation durable des quatre PDF de référence dans une prépublication GitHub technique « IWS — G0 Baseline », tag `g0-baseline` → `c74fa047171ff51e308f1855d8f636add2ac33ca` ; réalisée : https://github.com/bhurpeau/IWS/releases/tag/g0-baseline |
| A2 | Commit `c74fa04` accepté comme base ; branche `harmonisation/g0` validée ; commit et poussée autorisés ; pas de fusion dans `main` |
| A3 | Ouverture de G0.1 autorisée après versionnement de G0.0 |
| Réserves | Aucune bloquante pour G0.1 : R-G0-01 corrigée (E1), R-G0-02 clôturée, R-G0-03 traitée, R-G0-04 à 06 reportées à G0.7, R-G0-07 conservée (cosmétique), R-G0-08 reportée à G0.8 |
