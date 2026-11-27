# G0.1 — Inventaire lexical : rapport d'extraction et de couverture

**Phase :** G0.1 (inventaire lexical), soumise à validation ; G0.2 non entamée
**Date :** 27 novembre 2026
**Sources :** contenu de `Volume_I/` et `Volume_II/` identique au commit de base `c74fa04` (tag `g0-baseline`) ; `git diff c74fa04 -- Volume_I Volume_II` vide avant et après extraction
**Branche :** `harmonisation/g0`, à partir du commit de clôture G0.0 `59a7778`
**Outils :** `notations/scripts/extract_symbols.py`, `notations/scripts/check_coverage.py`, tests `notations/scripts/tests/` (Python 3, bibliothèque standard uniquement)

Conventions : **[CTRL]** contrôle exécuté et résultat observé ; **[CONSTAT]** fait établi par lecture ; **[LIMITE]** limite connue de l'extraction ; **[HYP]** hypothèse non vérifiée.

> **Nature des données.** La classification est **purement lexicale**. Une même famille lexicale (par exemple `rho`) regroupe des objets mathématiques éventuellement distincts. Aucune identification d'objet, aucune décision de notation et aucune relation intervolumes n'est établie ici : cela relève de G0.2 et des phases suivantes.

---

## 1. Corpus

| Corpus | Fichiers | Statut |
|---|---|---|
| Manuscrit, volume I | les 17 fichiers inclus par `main.tex` (manifeste G0.0) | inventaire complet |
| Manuscrit, volume II | `IWS_volume_II_classe_objets_transformations_v5_17.tex` | inventaire complet |
| Compagnons LaTeX (corpus complémentaire, statistiques séparées) | `certification_huit_episodes_V2.tex`, `transmission_profondeur_finie_V2.tex` | inventaire complet, fichier distinct |
| Compagnons Markdown | `NOTES_V5_17.md`, `audit_cauchy_lemme_V2.md` | extraction limitée : caractères grecs et mathématiques Unicode dans les spans de code |
| Exclus | `Volume_I/fig/planche_*.tex` (illustrations TikZ), journaux, audits | hors corpus lexical |

Les entrées des inventaires G0.0 sont réutilisées : liste des fichiers actifs (`G0_00_controls/manifest_*.json`), labels des `.aux` de référence (`G0_00_controls/labels_*.csv`, servant au contrôle des ancres).

## 2. Méthode

### 2.1. Segmentation

[CTRL] Pour chaque fichier, dans l'ordre :

1. masquage des commentaires `%…` (offsets préservés) et des blocs `verbatim` et `\verb` ;
2. détection des segments mathématiques : `$…$`, `$$…$$`, `\(…\)`, `\[…\]`, environnements `equation`, `align`, `gather`, `multline` et variantes étoilées ;
3. dans un segment, retour au mode texte pour `\text`, `\textbf`, `\emph`, `\mbox`, `\tag`, `\parbox` et les environnements `minipage`, `tabular`, `itemize`, `enumerate`, `center`. Les mathématiques imbriquées dans ces groupes sont analysées à leur tour (position `texte_imbrique`) ;
4. analyse séparée des mathématiques figurant dans les commentaires (contexte `commentaire`) et des corps de macros mathématiques (contexte `definition_macro`), exclus des statistiques principales.

Aucune mathématique n'a été trouvée dans les commentaires.

### 2.2. Atomes

Un **atome** est une base symbolique avec ses décorations, primes, indices et exposants. Natures de base :

- `latine` : lettre nue ;
- `grecque` : `\alpha` … `\Omega`, variantes `\var…` comprises ;
- `police` / `police_grecque` / `police_mot` : `\mathcal`, `\mathscr`, `\mathfrak`, `\mathbb`, `\mathbf`, `\boldsymbol`… ;
- `romaine` / `nom_operateur` : `\mathrm`, `\operatorname`, bascules anciennes `\rm` ;
- `operateur_nomme` : `\sin`, `\max`… ;
- `grand_operateur` : `\sum`, `\int`… ;
- `symbole_constant` : `\infty`, `\partial`, `\emptyset`… ;
- `lettre_speciale` : `\ell`… ;
- `macro_utilisateur` : macro sans argument du document, à corps mathématique.

Les relations, opérateurs binaires, délimiteurs, chiffres, espacements et commandes de structure (`\frac`, `\left`…) ne sont pas des atomes. Un nom de commande est lu en entier : `\rho` n'est jamais confondu avec `\rhd`, ni `\varrho` avec `\rho`.

Les atomes situés dans un indice ou un exposant sont aussi enregistrés :

- colonne `niveau` (0, 1 ou 2) ;
- colonnes `parent_id` et `porteur` ;
- colonne `position` : `indice`, `exposant`, `argument_decoration`, ou `script_orphelin` pour un script porté par `)`, un chiffre…

Exemple : `\mathcal R^{\mathfrak B,\rho}` donne trois lignes. `\mathcal{R}` au niveau 0, puis `\mathfrak{B}` et `\rho` au niveau 1, rattachés à `\mathcal{R}`.

### 2.3. Forme littérale et forme développée

`symbole_source` est la forme **littérale** du source, avec ses scripts. `forme_developpee` n'est renseignée que pour les macros utilisateur sans argument, développées une fois depuis le préambule du document. Exemples :

- `\X_t` → `\mathcal X_{t}` ;
- `\Madm` → `\mathfrak M^{\mathrm{adm}}` ;
- `\vth` (compagnons) → `\vartheta`.

Macros développées :

- volume II : `\IWS`, `\Hyb`, `\X`, `\Sstruct`, `\M`, `\Madm`, `\Supp`, `\Reach`, `\End`, `\Word`, `\Rep`, `\Exec`, `\Id` ;
- compagnons : `\R`, `\vth`.

`\norm{…}` est une macro à argument : elle n'est pas développée, et son contenu est analysé directement. Le volume I ne définit aucune macro mathématique.

### 2.4. Classe lexicale (une seule par atome)

| Classe | Règle |
|---|---|
| `nu` | base sans police, sans variante `\var…`, sans décoration, sans prime ni script |
| `variante_typographique` | police, variante `\var…`, décoration (`\hat`, `\dot`, `\bar`…) ou prime, sans script |
| `indexe` | indice ou exposant « simple » : lettres, chiffres, étiquettes `\mathrm{…}`, au plus un atome non latin |
| `composite` | script contenant un script imbriqué, au moins deux atomes dont un non latin (grec, police, macro), une structure (`\frac`, `\sum`, `\in`, `\le`…) ou une décoration, ou décoration d'une expression entière (`\widehat{AB}`) |

Le drapeau orthogonal `variante` signale une police ou une décoration sur un atome indexé ou composite. `glyphe` conserve la base avec sa police (`\mathcal{R}` ≠ `R`). `famille_lexicale` regroupe les glyphes d'une même lettre, polices et variantes `\var…` comprises (`R`, `\mathcal{R}`, `\mathbb{R}` → `R` ; `\vartheta` → `theta`). Elle sert de première maille de regroupement, non d'identité.

### 2.5. Localisation (exigence 4)

Chaque occurrence porte :

- `fichier`, `ligne`, `colonne` de l'atome, et `expr_ligne_debut`–`expr_ligne_fin` de l'expression ;
- `expr_id`, qui renvoie à `expressions_*.csv`, où figure la forme source normalisée de l'expression ;
- `section` (chemin tome/partie/chapitre/section) et `environnement` (pile d'environnements) ;
- `label_stable` et `type_ancre` :
  - `env:<nom>` pour le label de l'environnement englobant (énoncé, équation, figure) ;
  - `precedent` pour le dernier label antérieur dans le fichier, qui n'implique pas l'inclusion ;
  - vide si aucun label ne précède ;
- `empreinte` : SHA-1 tronqué de (fichier, section, label, expression normalisée, rang de l'expression, symbole, rang dans l'expression). Elle est indépendante des numéros de ligne et unique dans chaque fichier CSV ([CTRL]).

## 3. Bilan quantitatif

Les statistiques excluent les corps de définitions de macros (14 lignes pour II, 4 pour les compagnons).

| | Volume I | Volume II | Compagnons LaTeX |
|---|---:|---:|---:|
| Expressions mathématiques | 3 290 | 1 255 | 514 |
| Occurrences d'atomes | 11 697 | 3 591 | 1 415 |
| dont niveau 0 / 1 / 2 | 8 720 / 2 910 / 67 | 2 521 / 1 044 / 26 | 1 034 / 366 / 15 |
| `nu` | 6 741 | 2 132 | 772 |
| `indexe` | 3 459 | 1 109 | 511 |
| `variante_typographique` | 1 102 | 261 | 106 |
| `composite` | 395 | 89 | 26 |
| non classées | 0 | 0 | 0 |
| Familles lexicales | 143 | 141 | 77 |
| Glyphes distincts | 179 | 167 | 81 |
| Formes source distinctes | 859 | 480 | 229 |
| Occurrences via macro utilisateur | 0 | 110 | 15 |
| Dans un titre de section | 53 | 7 | 5 |

Compagnons Markdown : 23 caractères Unicode mathématiques relevés dans 131 spans de code, tous dans `audit_cauchy_lemme_V2.md`.

Lettres grecques les plus fréquentes :

- volume I : `\rho` 455, `\tau` 287, `\theta` 236, `\chi` 209, `\kappa` 152 ;
- volume II : `\rho` 107, `\tau` 104, `\mu` 69, `\varphi` 60, `\gamma` 50.

Détails :

- `symbol_families.csv` : familles × classes × corpus ;
- `symbol_glyphs.csv` : glyphes × classes × corpus, indices principaux et formes source.

## 4. Couverture

### 4.1. Confrontation avec l'audit historique des 455 `\rho` (`audits/diag_rho_volI.md`)

[CTRL] L'inventaire relève **455** atomes de glyphe `\rho` dans le volume I, comme l'audit, sans `\varrho` ni ρ Unicode. Les décomptes par fichier sont les suivants :

| Fichier | Occurrences |
|---|---:|
| `main.tex` | 1 |
| Livre II | 11 |
| Livre III | 87 |
| Annexe C | 8 |
| Annexe E | 39 |
| Annexe F | 2 |
| Annexe G | 109 |
| Annexe H | 56 |
| Annexe I | 46 |
| Annexe J | 9 |
| Annexe K | 29 |
| Annexe L | 58 |

[CTRL] Attribution par les **plages de lignes et indices donnés par l'audit**, reportée dans `coverage_rho_volI.csv`. Elle reproduit exactement ses quatre groupes :

| Groupe de l'audit | Critère lexical appliqué | Audit | Inventaire |
|---|---|---:|---:|
| Coefficient R1 | Livre II 889–983, annexe E 55–475 et 1554, annexe F 158 | 48 | 48 |
| Valeur propre modale | annexe C 1844–1888 | 8 | 8 |
| Rayon spectral | indice `\mathrm{sp}` (E 1238, 1241, 1248 ; F 479) | 4 | 4 |
| Lecture / résolution | reste | 395 | 395 |

Cette concordance porte sur des comptages et des localisations. Elle reprend les frontières de l'audit **sans revalider l'interprétation sémantique** de chaque occurrence, qui relève de G0.2.

Répartition lexicale des 455 `\rho` du volume I :

- par niveau : 141 au niveau 0 ; 313 en indice ou exposant, portés principalement par `\mathcal{R}` (101), `\Omega` (62), `A` (18), `\ell` (16), `\operatorname{Acc}` (14) ; 1 au niveau 2 ;
- par classe : 403 nus, 52 indexés.

Les deux anomalies signalées par l'audit sont **localisées** dans les sources courantes, sans diagnostic (G0.4) :

- `d_\rho` : annexe I, l. 497 ;
- `\mathcal R^{\mathfrak B,\rho}` : annexe K, l. 101 et 348.

Pour mémoire, dans le volume II, au niveau 0 : `\rho_X` (45), `\rho_{\mathrm{int}}` (20), `\rho` nu (11), `\rho_j` (2), `\rho_{X,T}`, `\rho_{X,S}`, `\rho_\pm` (1 chacun).

### 4.2. Contrôle croisé indépendant (`coverage_crosscheck.csv`)

[CTRL] Pour chaque commande de lettre grecque, de police, de nom d'opérateur et de grand opérateur, et pour chaque fichier (408 couples), on compare le décompte brut par expression régulière dans les segments mathématiques au décompte des atomes inventoriés. **0 écart.**

Les occurrences brutes situées hors segments mathématiques sont toutes dans les préambules du volume II et des compagnons : 14 commandes dans les corps de `\X`, `\Sstruct`, `\IWS`, `\Hyb`, `\M`, `\Madm`, `\Supp`… ; `\R` et `\vth` dans les compagnons.

### 4.3. Lettres latines (contrôle indicatif)

[CTRL] Décompte brut après retrait des commandes et des arguments non mathématiques, comparé aux atomes `latine` : égalité sur 17 fichiers sur 20. Les 3 écarts (−2, −2, −1) sont des **limites du contrôle**, non de l'inventaire. Le contrôle retire en bloc `\tag{…}` et `\text{…}`, y compris leurs maths imbriquées : `\tag{\(Z_R^\sharp\)}` (livre I l. 1157, annexe B l. 887) et `\text{$S$ …}` (volume II l. 102). Ces atomes sont bien présents dans l'inventaire.

### 4.4. Délimiteurs

[CTRL] Aucun délimiteur non fermé (0 problème de segmentation). Pour chaque fichier, le nombre de segments est égal au décompte brut des délimiteurs, à trois exceptions près :

- `\(` dans un `\tag` : livre I l. 1157 ;
- `\(` dans un `minipage` : annexe D l. 2087 (`minipage` ouvert l. 2082) ;
- `$S$` dans un `\text` : volume II l. 102.

Ces trois délimiteurs ouvrent des maths imbriquées : elles sont traitées comme telles et non comptées comme segments autonomes.

### 4.5. Labels et ancres

[CTRL] Tous les labels utilisés comme ancre existent dans les `.aux` de référence de G0.0 (`coverage_labels.csv` vide) :

- volume I : 443 labels employés sur 525 ;
- volume II : 19 sur 19.

[CONSTAT] Le volume II ne compte que 19 labels. 1 316 occurrences (37 %) précèdent son premier label et n'ont donc pas de `label_stable` ; elles restent localisées par fichier, ligne, section et empreinte. Pour le volume I, 20 occurrences sont dans ce cas (`main.tex`, avant-propos).

### 4.6. Reprise de l'audit V5.16 sur V5.17 (`coverage_v516*.csv`)

[CTRL] Recomptage des symboles du tableau V5.16 sur V5.17 (niveaux 0 et supérieurs) :

| Symbole | V5.16 (« indicatif ») | V5.17 inventaire | Observation |
|---|---:|---:|---|
| `\Xi`, `\Sigma`, `\Omega`, `\Phi`, `\mathscr F_w`, `Ω_w`, `τ_*`, `Dep` | 7, 28, 25, 11, 3, 5, 9, 19 | 7, 28, 25, 11, 3, 5, 9, 19 | identiques |
| `\vartheta` | 26 | 27 | +1 |
| `u` | 22 | 21 | −1 |
| `b_{i,w}`, `λ_{r,w}` | 8 | 15 | +7 |
| `C` | 181 | 71 | méthode V5.16 inconnue |
| `k`, `r`, `v`, `s_i` | 18, 9, 1, 1 | 189, 145, 10, 11 | V5.16 compte manifestement des occurrences sélectionnées par rôle |

[HYP] Les écarts sur `C`, `k`, `r`, `v` et `s_i` traduisent une méthode de comptage différente : l'audit V5.16 qualifie ses nombres d'« indicatifs » et vise des couples (symbole, rôle). Ils ne signalent pas en eux-mêmes une évolution du texte. Les écarts de ±1 et de +7 sont à examiner en G0.2/G0.4 par confrontation avec V5.16, dont la source n'est pas dans le dépôt.

[CTRL] Les 13 motifs obsolètes que V5.16 formule explicitement (`V5.10`, `\mathcal P_r`, `Dep(\vartheta)`, `b_{i,\Xi}`, `\lambda_{r,\Xi}`, `s_w`, `\ell_w`, `u:=\tau`, `v_i:=\tau`, `3^\ell`, `\pi_0(E)`, `\mu_w`…) ont été traduits en expressions régulières. **Aucune occurrence dans V5.17.** Les autres contrôles V5.16, de nature rédactionnelle ou sémantique, ne sont pas reproductibles lexicalement.

[CTRL] Actualisation : 131 glyphes de niveau 0 de V5.17 ne figurent pas au tableau V5.16 (`coverage_v517_new_families.csv`, avec première ligne et section). Ceux qui apparaissent pour la première fois après la ligne 1600, zone du bloc semi-algébrique, de la transmission C² et de la certification des huit Kairos, sont :

> `\mu`, `\ell`, `\epsilon`, `\Psi`, `O`, `\upsilon`, `\mathbf{e}`, `\operatorname{sign}`, `\arg`, `\mathcal{V}`, `\det`, `p`, `\mathcal{W}`, `\xi`, `\bigsqcup`, `\sum`, `\operatorname{int}`, `\mathrm{constante}`, `o`, `\arccos`, `\mathrm{rad}`

Ce sont des candidats à examiner en G0.2, non des collisions présumées.

## 5. Contrôles manuels ciblés

[CTRL] Vérifications manuelles :

- **Équation R1** (livre II l. 889) : atomes et classes conformes.
- **`\rho_{\mathrm{sp}}(\mathcal M_g)`** (annexe E l. 1238) : `\rho` indexé et `\mathcal M_g` indexé. Ce cas fait aussi l'objet d'un test.
- **`\mathcal R^{\mathfrak B,\rho}`** (annexe K l. 101) : composite, avec deux enfants de niveau 1.
- **`d_\rho`** (annexe I l. 497) : indexé, enfant `\rho`.
- **`J(\rho)`, `\zeta\rho S_\ast`** (annexe C l. 1844) : vérifiés, avec test associé.
- **Macros du volume II** : `\X`, `\Madm`, `\Reach`, `\Madm_{\End(x_0,\mathcal H_0)}` (II l. 129, composite). Formes littérale et développée conformes.
- **Échantillons aléatoires** : 15 occurrences tirées sur I et II, et 12 composites. Aucune erreur de localisation ni de classe observée.
- **Boîte `\boxed{\begin{minipage}…}`** (annexes C l. 1950, D l. 2082, F l. 1364) : prose en mode texte, désormais exclue des symboles (§ 6).

15 tests unitaires (`notations/scripts/tests/test_extract_symbols.py`) reprennent des fragments réels des sources. Tous passent.

[CTRL] Reproductibilité : deux exécutions successives produisent des fichiers identiques octet pour octet (après correction d'un défaut, § 6). Les tests et contrôles se lancent ainsi :

```bash
python3 -I notations/scripts/extract_symbols.py --out audits/G0/G0_01_inventory
```

```bash
python3 -I notations/scripts/check_coverage.py --inv audits/G0/G0_01_inventory
```

```bash
python3 -I -m unittest discover -s notations/scripts/tests
```

`check_coverage.py` renvoie le code 0 si la concordance `\rho` et le contrôle croisé sont exacts, 1 sinon.

## 6. Difficultés rencontrées et corrections de l'extracteur

| Difficulté | Traitement |
|---|---|
| **Prose dans un `minipage` à l'intérieur de `\boxed{…}` en mode mathématique** (annexes C, D, F) : sans traitement, environ 1 200 lettres de texte français auraient été comptées comme symboles. Défaut révélé par le contrôle des lettres latines | `minipage`, `tabular`, `\parbox` dans les maths traités comme texte, maths internes analysées |
| Formules dans `\tag{…}` (`Z_R^\sharp`) | `\tag` traité comme groupe textuel à maths imbriquées |
| Ancienne bascule `\rm` (compagnons, livre III) : `\tau_{\rm ref}` aurait produit trois lettres | lettres suivantes lues comme un nom romain (`statut_extraction = bascule_police`, 26 cas) |
| Environnement `document` captant tous les labels de section : toutes les occurrences de II recevaient `sec:opacity-finite-depth` | les environnements conteneurs ne possèdent pas de label |
| Liens parent fondés sur `id()` Python, réutilisable : liens instables entre exécutions | identifiant séquentiel ; déterminisme vérifié |
| Empreintes en double pour des expressions identiques sous une même ancre (`$\X$`) | rang de l'expression intégré à l'empreinte |
| Arguments non mathématiques (`\label`, `\begin{array}{c|cc}`) | ignorés |

## 7. Limites de l'extraction

- **[LIMITE] Lexical uniquement.** La règle `composite` est une heuristique documentée (§ 2.4) : `\rho_{ij}` est `indexe`, `A_{\mathcal P,\rho}` est `composite`. La famille lexicale fusionne polices et variantes ; le glyphe les distingue.
- **[LIMITE] Commandes en mode texte.** Une lettre grecque hors mode mathématique ne serait pas vue. Le contrôle croisé montre qu'il n'y en a aucune hors des préambules (corps de macros).
- **[LIMITE] Non inventoriés :** relations, opérateurs binaires, délimiteurs et chiffres, donc les applications « `J(\rho)` » comme motif. Les chiffres en police (`\mathbf 1`) sont des atomes.
- **[LIMITE] Macros à argument** (`\norm`, `\panelnodes`, `\commonkept`) : non développées. Les deux dernières sont du code TikZ.
- **[LIMITE] Ancres.** `precedent` n'implique pas l'appartenance à l'énoncé labellisé. Au volume II, 37 % des occurrences sont sans label (§ 4.5).
- **[LIMITE] Compagnons Markdown :** seuls les caractères Unicode des spans de code sont relevés. Ces documents ne sont pas en LaTeX et leur notation (`x̂`, `Σ_{k≥1}`) n'est pas analysée structurellement.
- **[LIMITE] Exclusions** (`exclusions.csv`) :
  - 3 blocs `verbatim` (annexe F : noms de scripts et sorties) ;
  - 3 `minipage` en mode mathématique ;
  - `\norm` non développé (30 usages) ;
  - extraction Markdown limitée.

## 8. Livrables

Dans `audits/G0/G0_01_inventory/` :

| Fichier | Contenu |
|---|---|
| `occurrences_volI.csv`, `occurrences_volII.csv` | occurrences des manuscrits (34 colonnes, § 2.5) |
| `occurrences_compagnons.csv`, `occurrences_compagnons_markdown.csv` | corpus complémentaire |
| `expressions_*.csv` | expressions sources référencées par `expr_id` |
| `symbol_families.csv`, `symbol_glyphs.csv` | familles et glyphes × classes × corpus |
| `exclusions.csv` | exclusions et constructions non traitées |
| `coverage_*.csv`, `coverage_summary.json`, `extraction_summary.json` | contrôles de couverture et métadonnées d'extraction |
| `extraction_report.md` | le présent rapport |

Scripts dans `notations/scripts/` : `extract_symbols.py`, `check_coverage.py`, `tests/test_extract_symbols.py`.

## 9. Porte de validation G0.1

| Critère du plan | État |
|---|---|
| Couverture documentée de toutes les sources actives | Atteint : 17 + 1 fichiers manuscrits, 2 + 2 compagnons, exclusions listées |
| Occurrences traçables | Atteint : fichier, ligne, colonne, expression, section, ancre, empreinte unique |
| Limites du parseur recensées | Atteint (§ 6–7) |
| Réutilisation de l'audit `\rho` vérifiée sur le commit gelé | Atteint : 455 = 48 + 8 + 4 + 395 |
| Motifs V5.16 actualisés sur V5.17 | Atteint pour les motifs exprimables lexicalement ; nouveaux glyphes listés |
| Aucun renommage | Atteint : sources inchangées |

Points soumis à l'auteur :

- règle de classe `composite` (§ 2.4) et regroupement des polices dans une même famille lexicale ;
- traitement des 1 316 occurrences du volume II sans label ;
- portée de l'extraction limitée des compagnons Markdown.

---

## Addendum B2a — Catégorie principale et attributs secondaires (27 novembre 2026)

À la suite de la décision B2a, cinq colonnes ont été **ajoutées à la fin** des fichiers d'occurrences. Les 34 colonnes de référence ne changent pas.

| Colonne | Contenu |
|---|---|
| `composite_portee` | `indice`, `exposant`, `indice+exposant` (motifs sur les deux positions, ou critère tenant à leur combinaison) ou `argument_decoration` ; vide si l'atome n'est pas composite |
| `motifs_composite` | motifs précis, préfixés par la position : `script_imbrique`, `composants_multiples_non_latins`, `structure`, `decoration`, `combinaison:composants_multiples_non_latins`, `argument_decoration:expression_decoree` |
| `composants_indice`, `composants_exposant` | glyphes des composants directs de chaque position |
| `attributs_secondaires` | police, variante `\var…`, décoration, primes, présence d'indice ou d'exposant, macro |

La **catégorie principale** (`classe_lexicale`) reste déterminée par la règle du § 2.4, appliquée dans l'ordre `composite` > `indexe` > `variante_typographique` > `nu`. Les attributs élémentaires restent disponibles dans leurs colonnes : glyphe, police, indice, exposant, structure, liens `parent_id`/`porteur`.

[CTRL] Résultats sur l'inventaire courant :

- chaque atome composite a au moins un motif ;
- aucun atome non composite n'en a ;
- répartition de la portée : volume I 203 indice / 51 exposant / 136 indice+exposant / 5 argument_decoration ; volume II 29 / 22 / 38 / 0.

[CTRL] Non-régression : `notations/scripts/check_regression.py` compare l'inventaire au commit de clôture G0.1 `05afddd`, conservé comme référence. On obtient **0 différence** sur les colonnes de référence des 8 fichiers comparés. Un test unitaire couvre les attributs secondaires (16 tests au total).

Rappel B2b : l'appartenance à une même `famille_lexicale` n'implique aucune identité ni proximité sémantique.
