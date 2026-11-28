# G0.3 — Correspondance intervolumes

**Date :** 28 novembre 2026
**Branche :** `harmonisation/g0` ; G0.2 clôturée au commit `3e837cb` (D1)
**Registre de référence :** 301 entrées, figées dans `G0_02_semantic/reference_301/` et non modifiées en G0.3
**Statut :** soumis à validation ; arrêt avant G0.4

Les marqueurs distinguent la nature des affirmations :

- **[CONTRÔLE]** contrôle réalisé ;
- **[IMPOSSIBLE]** contrôle non réalisé ou impossible ;
- **[CONSTAT]** fait établi ;
- **[HYPOTHÈSE]** supposition non vérifiée.

## 1. Objet et règles appliquées

G0.3 construit la table de correspondance entre les objets du volume I et ceux du volume II (plan § 7).

- **Orientation :** toutes les relations se lisent **du volume I (ou d'un compagnon) vers le volume II**.
- **Primauté du volume II :** elle reste notationnelle et ne présume aucune identité mathématique (plan § 1.1).
- **Codes :**
  - ID : même objet dans le cadre indiqué ;
  - GEN : l'objet II généralise l'objet I ;
  - SPEC : l'objet II spécialise l'objet I ;
  - PROJ : l'objet II est obtenu par projection ou restriction de l'objet I ;
  - DER : l'objet II est construit à partir de l'objet I ;
  - ANA : analogie sans identification ;
  - DIST : objets distincts ;
  - UNK : relation indéterminée ;
  - NEW : objet propre à un volume relativement au corpus étudié.
- **Statuts :** chaque relation est **établie** (justifiée par les définitions et, souvent, par un renvoi explicite du texte), **candidate** (conditions à vérifier ou à arbitrer) ou **indéterminée**.
- **Interdits respectés :**
  - aucune notation canonique choisie ;
  - aucune identification fondée sur la seule notation (plan § 1.2) ;
  - aucun manuscrit ni dépôt connexe modifié ;
  - aucun arbitrage notationnel (D4) ;
  - aucune désambiguïsation occurrence par occurrence (D5).

## 2. Fichiers

| Fichier | Rôle |
|---|---|
| `notations/crosswalk_relations.yaml` | **Source** des relations et des bilans « sans correspondant », rédigée à la main |
| `notations/crosswalk.csv` | Table générée (une ligne par relation), enrichie par le registre : désignations, notations, types, domaines, hypothèses, sites de définition, statuts, anomalies, conditions, justification, cardinalité |
| `notations/scripts/build_crosswalk.py` | Génération et contrôles de cohérence |
| `audits/G0/G0_03_crosswalk/coverage_by_object.csv` | Bilan de recherche pour chacun des 301 objets |
| `audits/G0/G0_03_crosswalk/crosswalk_summary.json` | Décomptes |
| `audits/G0/G0_03_crosswalk/D2_*` | Recalcul des coefficients de la branche résistante (D2) |

## 3. Bilan quantitatif

**[CONTRÔLE]** 82 relations intervolumes et 2 relations intravolume (D3, A-G02-08). Aucune erreur de cohérence.

| Relation | Établies | Candidates | Indéterminées |
|---|---:|---:|---:|
| ID | 14 | 5 | — |
| GEN | 6 | 6 | — |
| SPEC | 2 | 3 | — |
| PROJ | 3 | 0 | — |
| DER | 10 | 3 | — |
| ANA | 1 | 16 | — |
| DIST | 10 | 0 | — |
| UNK | — | — | 3 |
| **Total** | **46** | **33** | **3** |

**Cardinalités :** 26 relations un-à-un ; les autres sont un-à-plusieurs, plusieurs-à-un ou plusieurs-à-plusieurs.

- Côté volume I, 14 objets ont plusieurs correspondants, par exemple `I.CORE.STATE_SPACE` → \X, lecture découplée, π_s, ρ_int, \mathcal O_y.
- Côté volume II, 14 objets en ont plusieurs, par exemple `II.HIST.MONOID` ← monoïde de l'annexe G, histoires et épisodes du livre III.

**Bilan de recherche par objet** (`coverage_by_object.csv`) :

| Bilan | Volume I (205) | Volume II (88) | Compagnons (8) |
|---|---:|---:|---:|
| Correspondant établi (ID, GEN, SPEC, PROJ ou DER) | 21 | 32 | 3 |
| Correspondant candidat seulement | 10 | 12 | 1 |
| Relation indéterminée (UNK) | 3 | 1 | — |
| Sans correspondant identifié, avec analogie ou distinction relevée | 22 | 17 | — |
| Sans correspondant identifié | 142 | 25 | 2 |
| Analogie ou distinction seulement (non déclaré NEW) | 1 | 1 | 1 |
| Famille dont le bilan est porté par les composants | 6 | — | 1 |

« Sans correspondant identifié » ne vaut pas preuve d'absence. Chaque bilan de ce type est motivé par le contenu du volume II, groupe par groupe (`bilans_new`) : par exemple, le volume II ne traite ni la bornitude, ni la dyade, ni les interfaces R1/R2, ni la géométrie de réponse.

## 4. Correspondances établies

**Le noyau, spécimen de la classe hybride.** Le volume II écrit (l. 64) : « Le noyau du Volume I fournit un spécimen ».

- Relation GEN établie pour le système (X001), l'espace des états (X003), C (X004), D (X005) et l'opérateur de saut à granularité G0 (X007).
- L'appartenance du noyau à \Hyb (X002) reste **candidate** : H1–H4 ne sont énumérées que « provisoirement » (l. 91), même si l'annexe A établit existence, unicité, déterminisme et absence de Zénon, et si le volume II invoque lui-même ces résultats (l. 1159).

**Monoïde des histoires (X013, ID).** Volume II, l. 108 : « Conformément à l'Annexe G du manuscrit, une histoire finie est un mot d'un monoïde d'épisodes ». Réserves :

- le volume II ne réénonce ni la liberté du monoïde ni l'inclusion des délais (D-06) ;
- il indexe \M par le système.

**Objets du noyau employés par le volume II (X045–X055, ID).**

- Objets concernés : A, H, V, P, τ, N, Θ, ζ, (γ_0,γ_1), λ, d.
- Le volume II renvoie explicitement au volume I (l. 605–612, 1159) et y cite les formules de Q, M, Γ et D.
- L'identité porte sur les objets du noyau, non sur les régimes : le volume II étudie surtout γ_1 = λ = 0, N = 6 ou 9, d = 2.

**Lectures du noyau (PROJ, X056, X058, X059)** :

- la lecture découplée est x ↦ (A,H,V,P) ;
- la présentation naturelle (l. 607) donne π_s = A et ρ_int = (H,V,P) ;
- \Sstruct = \mathfrak G_N (X057, GEN).

**Constructions du volume II à partir du noyau (DER établies)** :

- fibre d'opacité \mathcal O_y comme ensemble des états qui ne diffèrent que par la trace (X060) ;
- décomposition C ≃ Y_adm × T (X061) ;
- mot structurel comme suite réduite des graphes (X062) ;
- marge de sélection (X063), avec **identité des composants** : i_r^* = i^* et m_r = min(2, d_r, N−1−d_r) = m, puisque |\mathcal N(i^*)| = d_r et |\mathcal N^c(i^*)| = N−1−d_r ;
- incrément Δτ_h et écart Δτ_j par intégration de l'équation de la trace (X065, X066) ;
- chemin de déformation (γ_1,λ) = ε(γ̄,λ̄) (X067, X068) ;
- groupe d'automorphismes du graphe (X069) ;
- u_max du volume II (X021) : il est construit à partir de l'entrée comme borne essentielle d'une entrée donnée, alors que le volume I pose u_max comme borne supposée ; **les deux statuts diffèrent**.

**Similarité et scores (X064, SPEC).** c_j^{(k)} = s(i_k^*, j) là où les traces sont non nulles. Le volume I prolonge s par 0 en cas de trace nulle ; le volume II exclut ce cas.

**Compagnons (provenance)** :

- le paramètre q = (ϑ, ε) est identique (X071) ;
- i_r = i_r^* (X072) ;
- le voisinage de transmission du volume II est un cas du voisinage \mathcal N du théorème compagnon (X074, SPEC).

## 5. Correspondances candidates : conditions à vérifier

| Id | Relation | Condition principale |
|---|---|---|
| X006 | F_A → F, GEN | Changement de représentation : graphe dans l'état, entrée portée par l'histoire |
| X008 | \mathcal K → K^*, DER | K^* défini implicitement au volume II ; cascade d'au plus N sauts |
| X009 | conventions du noyau → \Exec, GEN | Le volume I ne regroupe pas ses conventions en un objet |
| X010, X011 | Exec, Φ_H → γ_{x,H}, End, ID | Identifier la réalisation X à un état x ∈ C, alors que \mathfrak X est AMBIGUOUS ; histoire admissible ; granularité G0 ou G1 |
| X014, X015 | histoires, épisodes → \M | Correspondance élément ↔ ensemble ambiant |
| X016–X018 | \mathfrak B → \mathcal B, \Madm_x, continuations | Le volume II indexe l'admissibilité par l'état ; ID sous \mathfrak B ⊆ \Madm_x |
| X020 | entrée u → \Madm_x, GEN | Dans le noyau, les histoires sont des entrées bornées |
| X026 | \mathcal R_X^ρ → R_x^{ρ_int}, SPEC | ρ := trajectoire de ρ_int ; X = x ∈ C ; domaine \Madm_x |
| X028, X029 | ∼_{\mathfrak B,ρ} → ∼_N, SPEC | \mathfrak B = \mathfrak M (cas « de Nerode » du volume I), lecture de trajectoire de ρ_int, restriction à \mathcal O_y ; la clause d'égalité des domaines n'a pas d'équivalent au volume I |
| X030 | histoire séparatrice → famille séparante, DER | Construite sur ∼_N et les chemins structurels, non sur ∼_{\mathfrak B,ρ} |

## 6. Exemple désigné par le plan : lecture du volume I et ρ_X, ρ_int

**[CONSTAT]** Les rôles diffèrent :

- la lecture ρ du volume I est un choix de protocole appliqué aux exécutions de sonde (« Le symbole ρ ne décrit pas une variable interne du système », livre III l. 302) ;
- ρ_X = (π_s, ρ_int) est une application des états vers un espace produit \Sstruct × Y_int, déclarée avec la présentation, dont la composante π_s est constante pendant le flot.

**Relations retenues :**

- ρ → ρ_X : ANA établie (X022). Les deux objets sont analogues mais non identiques.
- τ_ρ → ρ_X : ANA candidate (X023). La condition (O2′) de l'annexe G imposerait à une lecture terminale une invariance par relaxation que ρ_X ne possède pas en général.
- ω_ρ → ρ_X : ANA (X024). La construction va de II vers I : γ ↦ ρ_X ∘ γ est une lecture de chemin si elle est compatible au suffixe. Elle n'est pas codée DER, qui est orienté I → II.

**Lien avec ρ_int.** La réponse du volume I ne coïncide avec R^{ρ_int} du volume II qu'à travers la spécialisation X026 : la lecture de chemin doit être choisie comme trajectoire de ρ_int.

## 7. Indéterminées et distinctions

**UNK (D4).**

- **\mathfrak X** (annexe G, livre III) → \X (X043, X044). Blocage : \mathfrak X désigne « les états complets ou, plus généralement, des présentations » (entrée AMBIGUOUS). La relation serait GEN si \mathfrak X désignait des états, et n'est pas définie s'il désigne des présentations.
- **ℓ_{c,\mathfrak B,ρ}** → k (X037). Même terme « profondeur » ; aucun rapport déclaré entre complexité et nombre de Kairos.

**DIST établies.** Elles portent sur des homonymies que G0.4 devra examiner, sans arbitrage ici :

- « historicité structurelle » : non-commutativité des \mathcal K_i au volume I, divergence ordinale des mots structurels au volume II (X033, X034) ;
- « présentation » : annexe K contre triplet du volume II (X042) ;
- ϑ : composante de trace diagonale (annexe C) contre paramètre caché (X075) ;
- Σ (X076) ;
- Φ (X078) ;
- \mathcal E (X079) ;
- \mathcal R (X080) ;
- Acc contre \Rep^{max} (X035) ;
- (H1)–(H5) contre H1–H4 (X073, A-G02-06).

**ANA relevées.** Elles sont utiles pour G0.4–G0.5 mais ne fondent aucune identification :

- signature κ contre mot structurel (X038) ;
- cellules hybrides contre chambres (X039) ;
- lieu de recomposition contre murs (X040) ;
- filtration par budgets contre partitions \mathcal P_k (X036) ;
- régions de réponse contre classes de mot (X081) ;
- lieux fixes de symétries invariants par le flot (X082) ;
- relativité observationnelle contre relativité du statut IWS (X041).

## 8. Relations intravolume demandées

### 8.1 Appropriation (D3, R001, candidate)

**[CONSTAT]** Les prédicats de `def:t2-appropriation` et de `def:D-appropriation` coïncident par substitution de y_T = Φ^T_{g,\mathcal P}(z_0) et renommage de l'attracteur final \mathcal A ↔ \mathcal A_1, sous quatre conditions :

- **C1 :** même système receveur, sur la même réduction (dyade A→B, diagonale interne) ;
- **C2 :** même application d'interaction (même \mathcal P, même couplage g pendant T, puis découplage) ;
- **C3 :** même dynamique autonome après découplage, donc même ω_0 sur le même domaine ;
- **C4 :** même notion d'attracteur autonome.

L'annexe D explicite (l. 1456) que la définition s'applique aux régimes hybrides invariants. Le livre II ne le précise pas, sans exclure ces régimes. L'annexe D prolonge donc explicitement la portée **sans changer le prédicat**.

Ni identité inconditionnelle ni généralisation stricte n'est affirmée. Les deux entrées sont conservées, comme le demande D3.

### 8.2 Relaxation de la pression (A-G02-08, R002, candidate)

**[CONSTAT]** Les deux écritures, P^+ = r_P P^- et P^+ = r_P Θ, définissent des opérateurs de saut :

- qui **coïncident sur {P_{i*} = Θ}** ;
- qui **diffèrent sur {P_{i*} > Θ}**.

Pour une condition initiale admissible (P_i(0) ∈ [0,Θ]), les trois faits suivants valent :

- (a) pendant le flot, P_i ≤ Θ et P_i est continue, donc tout premier saut a lieu avec P_{i*}^- = Θ (livre I l. 552) ;
- (b) dans une cascade, les pressions des nœuds non encore traités restent égales à Θ (l. 652, 666–670) ;
- (c) après un saut, P^+ = r_P Θ < Θ.

Par récurrence, **tout saut d'une exécution issue d'une condition initiale admissible vérifie P^- = Θ**, et les deux écritures produisent les mêmes exécutions. L'équivalence est **conditionnelle au domaine atteignable**, non une identité des opérateurs sur tout D.

Pour R2, l'argument vaut si la pression de l'interface franchit Θ par continuité. **[HYPOTHÈSE]** Cela suppose une pression R2 continue entre événements, ce qu'indiquent les solutions explicites de l'annexe E (l. 676) ; ce point n'a pas été démontré ici.

## 9. Coefficients de la branche résistante (D2)

**[CONTRÔLE]** Recalcul indépendant reproduit (`G0_03_crosswalk/D2_resistant_branch_check.py`) :

- r_c = 0,377964473009227 ;
- m₁ = −0,740810367098085 ;
- A = 5,303300858899108 ;
- c₁ = −2,177911111111111 ;
- c₂ = 0,321955402067028.

La formule complète et la forme simplifiée c₂ = −ζc₁²/(3m₁A) donnent la même valeur. Un contrôle par résolution directe de G(x, g_c+δ) = 0 donne un écart d'ordre δ³.

**Arrondis :** c₁ = −2,1779 ; c₂ = 0,3220.

**Corrections à faire, recensées dans `D2_occurrences.csv` :**

- 0,3216 au livre II, l. 484 ;
- −2,1774 au livre II, l. 482, à l'annexe D, l. 809, et à l'annexe F, l. 319 ;
- un résultat dépendant : annexe F, l. 330, où −0,1411 devient −0,1412.

Aucune figure ne dépend de ces coefficients. La provenance historique probable des valeurs anciennes se trouve dans `IWS_1` (lecture seule) ; leur origine n'est pas reconstruite.

**Annulation exacte des termes en m₂** (A-G02-15, correction scientifique) : (m₂/2)(Ac₁ + B)² = 0 puisque c₁ = −B/A. Les passages qualitatifs « s'annulent presque » et « l'origine générale … n'est pas encore établie » sont donc inexacts. La formalisation Lean énonce la même identité (README de `iws-lean`, l. 230 ; constat en lecture seule).

Ces corrections sont **numériques et scientifiques**, distinctes des corrections notationnelles de G0.4–G0.5. **Aucun manuscrit n'a été modifié.**

## 10. Réserves et anomalies

- **A-G02-01 à 15** sont préservées :
  - A-G02-03 et A-G02-08 sont instruites (§ 8) ;
  - A-G02-14 est instruite par D2 ;
  - A-G02-15 est nouvelle.
- **R-G0-13 :** le registre du volume II n'a pas d'entrée pour Q, M, Γ et D, pourtant cités par renvoi (l. 605–612). Les objets correspondants du volume I sont donc classés « sans correspondant identifié » faute de cible, alors qu'ils sont employés par renvoi.
- **R-G0-14 :** 33 relations candidates et 3 indéterminées attendent un arbitrage ou une instruction complémentaire.

**[HYPOTHÈSE]** Les relations GEN et ID entre le noyau et le socle supposent que les histoires du volume II se réalisent dans le noyau par les entrées u. Le volume II l'indique pour la classe maximale des entrées bornées (l. 654, 1159), mais n'en fait pas une définition générale.

## 11. Contrôles de cohérence et de non-régression

| Contrôle | Résultat |
|---|---|
| Identifiants existants ; codes, statuts et confiances valides ; orientation I/C → II | 0 erreur |
| Relations contradictoires sur un même couple (ID avec DIST, etc.) | 0 |
| Objet déclaré « sans correspondant » portant une relation d'identification | 0 |
| Objets sans bilan | 0 sur 301 |
| Propagation automatique des relations de famille aux composants | aucune (relations de famille : X036, X040, X055, X064, X070, X073, X081, chacune motivée) |
| Registre inchangé contre `reference_301` | 0 écart ; rattachements identiques octet pour octet |
| Inventaire G0.1 | 0 différence |
| Tests | 30 tests verts (dont 3 nouveaux sur la table) |
| Sources | `git diff c74fa04 -- Volume_I Volume_II` vide |
| Dépôts connexes | `iws-lean` `e9fb1a6`, `IWS_minimality_package` `b1a9738`, `IWS_1` `4240233` : aucune modification |

**[IMPOSSIBLE]** Aucune relation n'a été vérifiée par démonstration formelle. Les relations établies reposent sur la lecture des définitions et sur les renvois explicites du texte ; les candidates attendent l'auteur.

## 12. Arbitrages demandés

- **E1** — Valider G0.3 et autoriser le commit et la poussée.
- **E2** — Appartenance du noyau à \Hyb (X002) : la considérer comme établie au vu de l'annexe A et du renvoi du volume II (l. 1159), ou attendre la fixation de H1–H4.
- **E3** — Lever l'ambiguïté de \mathfrak X (X043, X044) : états complets ou présentations ? De cette décision dépendent X010, X011 et X026.
- **E4** — Statut des identifications conditionnelles par spécialisation : X026 (réponse) et X028, X029 (équivalence de Nerode). Faut-il les admettre comme établies sous leurs conditions, ou les garder candidates jusqu'à G0.5 ?
- **E5** — R-G0-13 : ajouter au registre du volume II des entrées pour Q, M, Γ et D cités par renvoi, ce qui transformerait les bilans correspondants en relations ID, ou laisser en l'état.
- **E6** — R001 et R002 : accepter les conditions documentées.
- **E7** — Ouvrir G0.4.

## 13. Addendum — intégration des arbitrages E2 à E6 (28 novembre 2026)

- **E2 :** X002 reste **candidate**. Le statut de spécimen (X001, établi) est distingué de la démonstration de l'appartenance à \Hyb. Celle-ci demande un raccord explicite entre H1–H4, l'invariance d'admissibilité et l'annexe A ; elle est inscrite en réserve de recherche (R-G0-15). Aucune démonstration n'est engagée.
- **E3 :** X043 et X044 restent **UNK**. \mathcal X reste réservé aux états complets, et \mathfrak X n'est pas identifié globalement à \mathcal X. Les conditions de X010, X011 et X026 renvoient explicitement à E3. L'examen des occurrences de \mathfrak X est fait en G0.4.
- **E4 :** X026, X028 et X029 restent **candidates**.
  - Pour X026, les compatibilités requises sont détaillées : états ou réalisations, domaines d'histoires, conventions d'exécution, espaces de sortie, lecture de chemin choisie comme trajectoire de ρ_int.
  - Pour X028 et X029, la réserve sur l'égalité des domaines d'histoires admissibles est explicite : l'égalité des réponses sur un domaine commun n'entraîne pas l'égalité des domaines.
- **E5 :** quatre entrées ajoutées au registre du volume II, reprises par renvoi après vérification des lignes : Q (l. 614), M (l. 615), Γ (l. 616), et le D du noyau (l. 626, employé l. 658–690).
  - Attribut `provenance_definition` : 266 LOCAL, 23 DERIVED (classement indicatif), 16 BY_REFERENCE.
  - Relations ID X083–X086.
  - **Distinction des rôles de D :** l'ensemble de saut abstrait du socle (l. 78–477, `II.HYB.JUMP_SET`, dont le sélecteur captait à tort les l. 600–700) ; le D du noyau (`II.KERNEL.JUMP_SET`, instance du précédent) ; la différentielle D_{(φ,μ)} (l. 1709).
  - Registre : 305 entrées ; références de 95 et 301 entrées conservées ; nouvel état figé dans `reference_305/`.
- **Rectification de renvois :** les références « l. 612 » pour D et pour K^* deviennent l. 626 et l. 628 ; la plage citée « l. 605–612 » devient l. 605–628.
- **E6 :**
  - R001 est une **identité conditionnelle établie entre les prédicats** sous C1–C4, sans identité des domaines d'application ; deux entrées conservées.
  - R002 est une **équivalence conditionnelle établie pour le noyau** (P⁻ = Θ), non étendue à R2 (R-G0-16) ; hors de P⁻ = Θ, les écritures diffèrent en général, sauf si r_P = 0.
- **Table après intégration :** 86 relations intervolumes (50 établies, 33 candidates, 3 indéterminées) et 2 intravolume établies. Elle est figée dans `G0_03_crosswalk/reference_E/`.

Arrêt avant G0.4 (levé par E7).
