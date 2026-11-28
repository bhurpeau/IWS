# G0.4 — Diagnostic des collisions notationnelles et sémantiques

**Date :** 28 novembre 2026
**Branche :** `harmonisation/g0` (non fusionnée dans `main`) ; base G0.3 : `fcf132a`
**Décision d'ouverture :** E7 (exécuter exclusivement G0.4 ; arrêt avant G0.5)
**Statut :** **clôturée (F2)** après intégration de F1 (§ 13) ; les §§ 1–12 conservent le diagnostic initial remis ; **aucune notation canonique choisie, aucun manuscrit, figure ni dépôt connexe modifié**.

Conventions de lecture : **[CTRL]** contrôle réalisé et reproductible ; **[CONSTAT]** fait relevé dans les sources ; **[HYP]** hypothèse ou proposition, non vérifiée ; **[IMPOSSIBLE]** contrôle non réalisable dans le cadre de G0.

---

## 1. Objet, sources et livrables

G0.4 recense les collisions entre notations et entre objets, les qualifie (nature) et les classe (niveau N0–N4) **sans les résoudre**. La primauté du volume II V5.17 est notationnelle et non mathématique : un usage du volume II sert de **côté de référence**, l'usage concurrent du volume I ou des compagnons est le **côté à examiner** ; les ambiguïtés internes au volume II sont distinguées et soumises à arbitrage, non tranchées par défaut.

Sources mobilisées : inventaire G0.1 (`G0_01_inventory/`, 11 697 occurrences au volume I, 3 591 au volume II, 1 415 aux compagnons) ; registre de 305 entrées (`notations/registry.yaml`, identique à `reference_305/`) ; table de correspondance figée (`G0_03_crosswalk/reference_E/`) ; classement des non-rattachés de G0.2bis (`G0_02bis/unresolved_classification.csv`, 50 clés USAGE_AMBIGU) ; `RESERVES.md` (A-G02-01 à 15, R-G0-12 à 16) ; audit V5.16 (réservations de symboles) ; audit ρ ; README de `iws-lean` (lecture seule) pour l'impact Lean.

| Livrable | Contenu |
|---|---|
| `notations/collisions.yaml` | **catalogue structuré** (source) : 65 collisions, réservations V5.16, relations sans collision, synonymies ID examinées, corrections scientifiques |
| `notations/scripts/build_collisions.py` | validation du catalogue, décomptes, couverture, propagation |
| `notations/scripts/tests/test_collisions.py` | 5 tests |
| `G0_04_collisions/collisions.csv` | une ligne par collision (généré) |
| `G0_04_collisions/collision_occurrences.csv` | propagation : décompte par collision, sélecteur, rôle et fichier (généré) |
| `G0_04_collisions/ambiguous_keys_coverage.csv` | **bilan des 50 clés ambiguës** (généré) |
| `G0_04_collisions/collisions_summary.json` | répartitions et erreurs (généré) |
| `G0_04_collisions/mathfrak_X_occurrences.csv` | classement manuel des 32 occurrences de 𝔛 (E3) |

### 1.1 Schéma d'une collision

Chaque entrée porte : identifiant stable `COL-…`, famille thématique, symboles, objets du registre, nature (une ou plusieurs parmi HOMONYMIE, SYNONYMIE, QUASI_COLLISION, AMBIGUITE), niveau, portée (`intra_I`, `intra_II`, `intra_C`, `inter`, `inter_C`), portées respectives, relations intervolumes (X…, R…), anomalies (A-G02-…), clés ambiguës couvertes, justification, impacts scientifique, éditorial et Lean, dépendances, propagation, **action proposée (sans arbitrage)**, type d'arbitrage attendu, catégorie de correction (NOTATIONNELLE, TERMINOLOGIQUE, DOCUMENTAIRE, SCIENTIFIQUE) et sélecteurs de comptage avec leur rôle.

### 1.2 Règles de classement

La nature et le niveau sont indépendants : une homonymie peut être N0 (réemploi local) ou N3.

| Niveau | Critère appliqué |
|---|---|
| N0 | réemploi local légitime (preuve, calcul, annexe), sans rôle partagé |
| N1 | collision graphique sans ambiguïté de rôle (indices discriminants, portées disjointes, types sans rapport) |
| N2 | collision sémantique dans une portée significative (même livre ou même annexe, ou objets lus ensemble) |
| N3 | notation **réservée par le volume II** (audit V5.16, macro, terme défini) **et** proximité conceptuelle ou portée partagée par les deux volumes |
| N4 | définition absente, ambiguïté mathématique non levée ou types incompatibles dans un même énoncé |

[HYP] La règle de N3 est une interprétation du plan (§ 8, « collision critique entre objets proches ou avec une notation réservée ») : une notation réservée réemployée loin de sa portée, sans proximité (par exemple v, k, r), est classée N1 ou N2. Le script refuse un N3 dont la justification ne motive ni réservation ni proximité.

---

## 2. Résultats d'ensemble

[CTRL] `build_collisions.py` : **0 erreur** (identifiants, valeurs, objets du registre, relations de la table, anomalies, sélecteurs non vides, couverture).

| Niveau | N0 | N1 | N2 | N3 | N4 | Total |
|---|---|---|---|---|---|---|
| Collisions | 4 | 18 | 30 | 9 | 4 | **65** |

| Portée | N0 | N1 | N2 | N3 | N4 |
|---|---|---|---|---|---|
| inter (I↔II) | 2 | 9 | 19 | 9 | 1 |
| inter_C (compagnons↔II) | — | — | 1 | — | — |
| intra_I | 2 | 6 | 8 | — | 2 |
| intra_II | — | 3 | 2 | — | 1 |

Natures (une collision peut en porter plusieurs) : HOMONYMIE 47, SYNONYMIE 14, QUASI_COLLISION 13, AMBIGUITE 11.
Catégories de correction : NOTATIONNELLE 37, DOCUMENTAIRE 19, TERMINOLOGIQUE 5, SCIENTIFIQUE 4 (plus 3 corrections scientifiques hors collisions, § 8).

[CONSTAT] Les **9 collisions N3** sont toutes intervolumes : la portée partagée par les deux volumes est le facteur commun. Les **4 N4** sont trois défauts de définition du volume I et un du volume II (§ 5).

---

## 3. Familles thématiques

| Famille | Collisions | N0 | N1 | N2 | N3 | N4 |
|---|---|---|---|---|---|---|
| F1 ρ et ses lectures | 8 | 1 | 3 | 1 | 1 | 2 |
| F2 espaces 𝔛, \mathcal X, X ; présentations | 3 | | | 1 | 1 | 1 |
| F3 fibres d'opacité | 2 | 1 | | 1 | | |
| F4 symboles réservés Σ, Ω, Φ, ϑ, \mathcal S | 5 | | | 1 | 4 | |
| F5 applications de réponse | 3 | | 1 | 2 | | |
| F6 équivalences | 2 | | | 2 | | |
| F7 historicité | 1 | | | | 1 | |
| F8 profondeur, k, r, ℓ | 3 | | | 3 | | |
| F9 lettres du noyau et des annexes | 17 | | 2 | 13 | 2 | |
| F10 synonymies | 10 | | 5 | 5 | | |
| F11 hypothèses et étiquettes | 2 | | 1 | 1 | | |
| F12 ambiguïtés internes au volume II | 6 | 1 | 4 | | | 1 |
| F13 réemplois locaux regroupés | 3 | 1 | 2 | | | |

### 3.1 F1 — ρ

- **COL-RHO-01 (N3, inter)** [CONSTAT] : la résolution d'observation ρ du volume I (paramètre de protocole ; 394 occurrences côté volume I, livre III et annexes G–L, dont 313 en indice) et la lecture ρ_X, ρ_int du volume II (application des états ; 67 occurrences) partagent glyphe et champ sémantique ; relations ANA seulement (X022–X024). Le décompte reproduit à une unité près les 395 occurrences de l'audit ρ. C'est la collision la plus sensible du corpus : elle porte toute la famille indexée (\mathcal Y_ρ, τ_ρ, ω_ρ, \mathcal R^ρ, ∼_{𝔅,ρ}, Ω_{\mathcal P,ρ}, Acc, ℓ, d) et conditionne X026, X028, X029.
- COL-RHO-02 (N2, intra_I) : coefficient de réouverture de R1 (48 occurrences) contre lecture.
- COL-RHO-03 (N0) : valeur propre modale et ρ_sp ; COL-RHO-04 (N1) : ρ_sp contre ρ_int.
- **Ambiguïtés internes au volume II** : COL-RHO-05 (N1, ρ nu en indice abrégeant ρ_X, 19 occurrences, sans convention écrite) ; COL-RHO-06 (N1, ρ polaire et ρ_j du bloc conique).
- COL-RHO-07 (N4, d_ρ, A-G02-04) et COL-RHO-08 (N4, \mathcal R^{𝔅,ρ}, A-G02-05) : § 5.

### 3.2 F2 — 𝔛, \mathcal X, présentations (E3)

[CONSTAT] Classement manuel des 32 occurrences de 𝔛 (`mathfrak_X_occurrences.csv`) :

| Niveau d'abstraction | Occurrences | Exemples |
|---|---|---|
| Réalisations | 18 | livre III, annexes G, L (familles de réalisations, « réalisations X∈𝔛 ») |
| Indéterminé | 12 | déclarations doubles : annexe G l. 46 et 868 (« états complets ou présentations ») ; annexe L l. 22 et 500 (« systèmes ou conditions initiales ») ; quotients, résumés, pseudo-ultramétrique qui en héritent |
| États d'un système fixé | 2 | annexe G l. 228 (τ_ρ : 𝔛 → \mathcal Y_ρ, lecture de l'état terminal) ; livre III l. 1001 (réalisations au repos) |
| Présentations (explicite) | 0 | aucune occurrence n'emploie 𝔛 pour des présentations hors des déclarations doubles |

**COL-X-01 (N4, inter)** : le niveau d'abstraction de 𝔛 n'est pas fixé par le volume I lui-même, et 𝔛 voisine graphiquement \mathcal X (réservé aux états complets, E3), que le volume I emploie aussi pour le noyau.

Conséquences pour la table (sans modification de celle-ci) :

- **X010 (exécution) et X011 (état terminal)** : l'identification à Exec(x,\mathcal H) et End(x,\mathcal H) n'a de sens que dans les occurrences de type « état » ; elle est exclue pour les 18 occurrences de type « réalisation » tant qu'aucune projection n'est posée (E3 interdit de la postuler) ; les 12 indéterminées restent bloquantes.
- **X026 (réponse)** : la lecture terminale τ_ρ de l'annexe G l. 228 impose le type « état » là où elle est employée ; c'est le seul point d'appui textuel pour la compatibilité (a) de X026.
- X043, X044 restent UNK.

COL-X-02 (N2) : X nu ou indexé (réalisation, indice de système X∈{A,B}, ensemble d'états de l'annexe K) contre les fibres X_s, X_A du volume II ; **X_A** existe dans les deux volumes avec des sens différents.
**COL-PRES-01 (N3)** : « présentation » (annexes G, K, L ; théorème d'équivalence de présentation) contre la présentation \mathbf S=(S,ρ_X,(\Madm_x)) du volume II, terme défini ; proximité forte.

### 3.3 F3 à F8

- **F3** COL-FIB-01 (N2, interne au volume II, A-G02-01, décision C2) : deux « fibres d'opacité » ; arbitrage terminologique interne.
- **F4** : Σ (COL-SIG-01), Ω (COL-OME-01), Φ (COL-PHI-01) et ϑ (COL-VTH-01), réservés par V5.16, sont tous **N3**. Les plus lourds en propagation sont Ω (90 occurrences au volume I, dont l'espace des sondes du livre III, proche du domaine paramétrique) et Φ (76, transitions d'histoires, objet central du volume I). Pour ϑ, l'annexe C emploie le symbole pour une composante de trace alors que le volume II l'emploie pour un paramètre caché de traces : la proximité est conceptuelle ; Lean emploie ϑ dans 11 fichiers. COL-SSTRUCT-01 (N2) : \mathcal S (macro \Sstruct) contre l'espace des contenus de l'annexe H.
- **F5** : COL-RESP-01 (N2) \mathcal R_X^ρ contre R_x^{ρ_int}, synonymie **conditionnelle à X026** ; COL-RESP-03 (N2) : la réponse triplet du livre II et l'écriture « précisée » du livre III ; COL-RESP-02 (N1).
- **F6** : COL-EQ-01 (N2) « Nerode » : classe complète au volume I, fibre et égalité des domaines au volume II (réserve E4) ; COL-EQ-02 (N2) ≡_b contre ≡_k^{\mathcal H}.
- **F7** : **COL-HIST-01 (N3)** « historicité structurelle » (non-commutativité des \mathcal K_i, livre I) contre H^{s,ord}_ρ, constitutive de la classe IWS (X033, X034 DIST) : risque de lire la proposition du livre I comme établissant la propriété du volume II.
- **F8** : COL-DEPTH-01 (N2) « profondeur » (ℓ_{c,𝔅,ρ}, complexité de séparateurs, contre k, nombre de Kairos ; X037 UNK ; ℓ réservé à un indice de coordonnées) ; COL-K-01 (N2) k=α/β ; COL-R-01 (N2) r=‖τ‖.

### 3.4 F9 — lettres du noyau et des annexes

| Id | Symbole | Niveau | Point saillant |
|---|---|---|---|
| **COL-C-01** | C | **N3** | C réservé à l'ensemble de flot, employé ainsi dans le livre I, qui emploie aussi C=b/(2a) quelques centaines de lignes plus loin (et l'annexe B, l'épisode test C du livre III, les cellules C_k) |
| **COL-U-01** | u | **N3** | u réservé à l'entrée du noyau ; le livre III l'emploie pour le paramètre de sonde, alors que les sondes sont réalisées par des entrées (X020) |
| COL-D-01 | D | N2 | trois rôles au volume II (socle, noyau, différentielle), délai et domaines au volume I, matrice des degrés au compagnon |
| COL-DCAL-01 | \mathcal D | N2 | opérateur de Kairos, diagonale (Lean ιD), délais, lieux dégénérés |
| COL-Q-01 | q | N2 | cinq rôles au volume I |
| COL-Q-02 | q | N2 | **interne au volume II** : nœud contre paramètre de protocole |
| COL-A-01 | A, B | N2 | adjacence (ID) et ≈ 100 réemplois au volume I ; « paire miroir » au volume II |
| COL-CHI-01 | χ | N2 | **homonymie à instruire** (D4) : χ de R2 et χ des annexes H–K, tous deux « variable d'interface » ; décision scientifique |
| COL-S-01, S-02 | s | N2 | au moins cinq rôles ; \mathbf s et \boldsymbol s pour la même mémoire ; lien des mémoires lentes non instruit |
| COL-THETA-01 | θ | N2 | composante de trace, horloge lente, angles ; θ_0 double |
| COL-EPS-01 | ε | N2 | **interne au volume II** : unité du monoïde contre paramètre de déformation |
| COL-DELTA-01 | Δ | N2 | variété homogène contre période et délai |
| COL-CAL-01 | \mathcal A, \mathcal P, \mathcal L, \mathcal G, \mathcal V, \mathcal M | N2 | \mathcal P protocole de contact contre sonde |
| COL-E-ALPH-01 | \mathcal E | N2 | alphabet des épisodes contre paires admissibles |
| COL-V-01, E-01 | v, E | N1 | réservations très locales (lemme orbital) ou usage conforme |

### 3.5 F10 à F13

- **F10 synonymies** : écritures (x,y,ϑ)/(x,v,θ)/(x,ẋ,θ) (A-G02-10, N2) ; θ_∞ et θ_0(g) (A-G02-13, N2) ; R_b et \widehat R (A-G02-11, N1) ; 𝔊_N et \mathcal G_N (A-G02-12, N1) ; \mathcal K contre K, K^* (N1) ; Φ_{\mathcal H}/End et Exec_{\mathcal H}(X)/Exec(x,\mathcal H) (N2, conditionnelle à X010–X011) ; i^*, i_r^*, i_r (N1) ; reset r_P P^- / r_P Θ (A-G02-08, R002, N2) ; deux définitions de l'appropriation (A-G02-03, R001, N1) ; a₁, a₂ double (A-G02-09, N2, homonymie).
- **F11** : H1–H4 (socle) contre (H1)–(H5) (compagnon de transmission, A-G02-06, N2, portée inter_C ; le volume II signale lui-même la distinction l. 1792) ; étiquettes (A1)–(A4), (O1), (P1)–(P6) (N1).
- **F12 internes au volume II** : \Hyb (N1, requalifiée, A-G02-07) ; \Supp et \Reach^{flow} (**N4**) ; G, T, m, φ (N0–N1).
- **F13** : réemplois locaux regroupés (x, z, h, t, conditions initiales ; constantes c, a, b, d, δ, η, J, σ, p, P, I ; R_V).

---

## 4. Bilan des 50 clés ambiguës (R-G0-12, D5)

[CTRL] Les 50 clés USAGE_AMBIGU de G0.2bis sont **toutes** rattachées à au moins une collision (`ambiguous_keys_coverage.csv`) ; aucune clé hors liste n'est déclarée.

| Niveau le plus élevé | Clés | Exemples |
|---|---|---|
| N0 | 10 | x, z, h, x_0, z_0, t_0 (I) ; φ, φ_4, φ_5 (II) ; φ (I) |
| N1 | 22 | c, a, b, d, δ, η, J, σ, p, P, I, m, T, v, v_0, R_V (I) ; I, m, T, G (II) ; d, I (compagnons) |
| N2 | 17 | s, θ, θ_0, A, B, q, Δ, D, ε, r, k, \mathcal D, \mathcal V (I) ; θ, Δ, ε, \epsilon (II) |
| N3 | 1 | C (I) |
| N4 | 0 | — |

[CONSTAT] 32 clés sur 50 (N0, N1) relèvent de réemplois sans ambiguïté de rôle : leur statut « ambigu » en G0.2bis tenait à la pluralité des rôles, non à un risque de confusion. 18 clés portent une collision significative ; toutes sont au volume I sauf θ, Δ, ε et \epsilon au volume II.

---

## 5. Blocages (N4)

| Id | Objet | Nature du défaut | Arbitrage |
|---|---|---|---|
| COL-RHO-07 | d_ρ (annexe I l. 497, A-G02-04) | définition absente | scientifique |
| COL-RHO-08 | \mathcal R^{𝔅,ρ} (annexe K, hypothèse (P5), A-G02-05) | employé sans définition, au moins deux lectures | scientifique |
| COL-X-01 | 𝔛 | niveau d'abstraction non fixé (§ 3.2) | scientifique et notationnel |
| COL-SUPP-01 | \Reach^{flow}, \Supp (volume II, A-G02-02) | définition absente ; usage avant définition | scientifique, interne au volume II |

[CTRL] Les quatre défauts ont été vérifiés dans les sources courantes (plan § 8) : aucune définition n'apparaît dans les fichiers gelés.

---

## 6. Primauté du volume II et ambiguïtés internes

Dans les collisions intervolumes, le volume II fournit le côté de référence : aucune adaptation n'est proposée pour ρ_X, ρ_int, Σ, Ω, Φ, ϑ, C, u, \mathcal X, « présentation » ni « historicité structurelle ordinale ». Les huit collisions **internes au volume II** ne sont pas tranchées par la primauté et sont soumises à arbitrage :

| Id | Objet | Niveau |
|---|---|---|
| COL-RHO-05 | ρ nu en indice (abrégé de ρ_X) | N1 |
| COL-RHO-06 | ρ polaire, ρ_j | N1 |
| COL-FIB-01 | deux « fibres d'opacité » | N2 |
| COL-Q-02 | q nœud contre paramètre de protocole | N2 |
| COL-EPS-01 | ε unité du monoïde contre paramètre de déformation | N2 |
| COL-H-01 | H1–H4 contre (H1)–(H5) (avec le compagnon) | N2 |
| COL-HYB-01, T-01 | \Hyb ; T à trois rôles | N1 |
| COL-SUPP-01 | \Reach^{flow}, \Supp | N4 |

---

## 7. Propagation estimée

[CTRL] Décomptes de l'inventaire G0.1 par sélecteur (`collision_occurrences.csv`). Les motifs texte (« présentation », « Nerode », « historicité structurelle », étiquettes) comptent environ 100 occurrences supplémentaires, ligne par ligne (un terme coupé par un saut de ligne n'est pas compté).

| Ensemble | Occurrences distinctes côté à examiner |
|---|---|
| Toutes collisions | 3 618 (31 % des 11 697 occurrences du volume I, avec chevauchements entre collisions résolus) |
| Collisions N3 et N4 | 760 |

Répartition par fichier (somme par collision, chevauchements non retirés) : livre III 614, annexe C 385, annexe D 382, annexe I 336, annexe H 331, annexe G 274, livre II 270, annexe E 259, annexe L 201, annexe K 178, annexe B 126, annexe F 116, annexe J 104, livre I 98, annexe A 82.

[HYP] Ces chiffres sont des **bornes supérieures** : ils incluent les N0 et N1 (à conserver par défaut) et les collisions dont l'action proposée est documentaire. Le volume de correction effectif dépend des arbitrages de G0.5 ; la propagation la plus concentrée est celle de ρ (394 occurrences) et des réservés Σ, Ω, Φ, ϑ (≈ 250 occurrences), principalement dans le livre III et les annexes C, G–L.

### 7.1 Impact Lean (lecture seule de `iws-lean`)

[CONSTAT] Les identifiants Lean sont conservés par défaut (plan § 1.1) ; aucune collision n'impose de modification Lean. Raccords documentaires à prévoir en G0.8 : ϑ (AnnexC/AnnexD, composante de trace, COL-VTH-01), k (LambdaQ, COL-K-01), r et rP (COL-R-01, COL-SYN-08), ιD (COL-DCAL-01), liftΔ (COL-DELTA-01), charCoeffs (a₁, a₂, COL-SYN-10), θ (COL-THETA-01), IsAppropriated (COL-SYN-09, COL-CAL-01). Le README Lean documente la sémantique garde P=Θ et reset r_P Θ avec coïncidence sur C, cohérente avec R002. [IMPOSSIBLE] Aucune compilation Lean n'a été relancée.

---

## 8. Corrections scientifiques (catégorie distincte)

| Id | Anomalie | Description | Statut |
|---|---|---|---|
| SCI-01 | A-G02-14 | c₁ = −2,1779 et c₂ = 0,3220 (valeurs anciennes −2,1774 et 0,3216) ; résultat dépendant à l'annexe F l. 330 | instruite (D2), correction en attente |
| SCI-02 | A-G02-15 | annulation exacte des termes en m₂ ; énoncés « s'annulent presque » et « origine non établie » inexacts | instruite, correction en attente |
| SCI-03 | — | [CONSTAT] la formalisation Lean de l'annexe D signale que ζ_min(k) n'est pas toujours atteint (infimum, ζ_inf) | relevé seulement ; non instruit en G0 |

Ces points ne sont pas des collisions et ne relèvent pas de l'harmonisation notationnelle ; ils sont rappelés pour qu'aucune correction notationnelle ne les absorbe.

---

## 9. Couverture du mandat (E7)

| Exigence | Traitement | Contrôle |
|---|---|---|
| 50 clés ambiguës | § 4 | [CTRL] 50/50 |
| Homonymies internes (D4) | χ, s, θ, a₁/a₂, q, ρ, D, \mathcal D… | dans le catalogue |
| Relations DIST, ANA, UNK | 30 relations (17 ANA, 10 DIST, 3 UNK) : rattachées à une collision ou motivées sans collision (`relations_examinees_sans_collision`) | [CTRL] 0 non examinée |
| Synonymies des relations ID et R001, R002 | `synonymies_ID_examinees` | [CTRL] 0 non examinée |
| Réservations du volume II (V5.16, macros) | `reservations_V5_16` : 18 symboles ; Ξ, Dep et le bloc semi-algébrique sans usage au volume I ; \mathfrak M sans collision | [CTRL] collisions existantes |
| Réemplois locaux légitimes | F13, N0 | — |
| Blocages | § 5 | — |
| Cas prioritaires (ρ, 𝔛, réalisations, présentations, fibres, Σ, Ω, Φ, ϑ, réponses, équivalences, historicité, profondeur, C, D, q, k, r, A, χ, s, θ, H1–H4/H1–H5) | tous présents | — |

---

## 10. Arbitrages à rendre en G0.5

Propositions sans arbitrage ; l'ordre suit la dépendance et le niveau.

### 10.1 Scientifiques (préalables)

| # | Question | Collisions |
|---|---|---|
| S1 | Niveau d'abstraction de 𝔛 (états, réalisations, présentations) : précision textuelle ou deux symboles ; conséquences pour X010, X011, X026 | COL-X-01, COL-SYN-06, COL-RESP-01 |
| S2 | Identité ou distinction de χ (R2) et χ (annexes H–K), et des mémoires s, \mathbf s, \vec s ; lien de θ (trace) avec la phase lente θ | COL-CHI-01, COL-S-01, COL-THETA-01 |
| S3 | Définition de d_ρ ou reformulation de la borne de l'annexe I | COL-RHO-07 |
| S4 | Lecture retenue pour \mathcal R^{𝔅,ρ} dans (P5) | COL-RHO-08 |
| S5 | \Reach^{flow} et \Supp (volume II) | COL-SUPP-01 |
| S6 | Relation entre profondeur de séparabilité et profondeur de Kairos (X037), si un lien est envisagé | COL-DEPTH-01 |
| S7 | Portée R2 du reset de pression (R-G0-16) | COL-SYN-08 |

### 10.2 Notationnels et terminologiques (intervolumes, N3)

| # | Question | Collision |
|---|---|---|
| N1 | Résolution d'observation ρ du volume I et sa famille indexée : qualification, renommage ou avertissement | COL-RHO-01 (et COL-RHO-02) |
| N2 | Σ, Ω, Φ, ϑ au volume I : adaptation dans la portée de réservation, ou dérogation motivée (stabilité de l'annexe C pour ϑ) | COL-SIG-01, COL-OME-01, COL-PHI-01, COL-VTH-01 |
| N3 | C=b/(2a) et l'épisode C ; paramètre de sonde u | COL-C-01, COL-U-01 |
| N4 | Termes « présentation » et « historicité structurelle » au volume I | COL-PRES-01, COL-HIST-01 |

### 10.3 Notationnels N2 (volume I) et synonymies

Q, D, \mathcal D, A, B, Δ, k, r, \mathcal P, \mathcal A, \mathcal E, X, \mathcal S ; unification des écritures de la réduction scalaire, de θ_0(g), de R_b, de \mathcal K/K ; choix d'un énoncé de référence de l'appropriation ; écriture de référence du reset (avec la condition P⁻ = Θ) ; renommage de l'un des jeux a₁, a₂ ; « Nerode » et ≡.

### 10.4 Internes au volume II

Fibres d'opacité (C2), q nœud, ε déformation, convention ρ en indice, H1–H4 contre (H1)–(H5), \Hyb, T.

### 10.5 Sans arbitrage

13 collisions (N0 et N1 documentaires) : conservation proposée, mention éventuelle dans la table des notations.

---

## 11. Contrôles de non-régression

| Contrôle | Résultat |
|---|---|
| Catalogue | [CTRL] `build_collisions.py` : 0 erreur |
| Tests | [CTRL] 35 tests verts (30 antérieurs + 5 nouveaux) |
| Registre | [CTRL] identique à `reference_305` (`registry_io.py verify` : 0 écart) ; références 95 et 301 non touchées |
| Table de correspondance | [CTRL] régénérée sans erreur ; `crosswalk.csv` et `crosswalk_relations.yaml` identiques octet pour octet à `reference_E/` |
| Inventaire G0.1 | [CTRL] `check_regression.py` : 0 différence sur 8 fichiers |
| Sources | [CTRL] `git diff fcf132a -- Volume_I Volume_II` vide |
| Dépôts connexes | [CTRL] `iws-lean`, `IWS_minimality_package`, `IWS_1` : arbres propres |
| Compilation LaTeX, Lean | [IMPOSSIBLE/non requis] non relancées (aucune source modifiée) |

Limites : [HYP] les décomptes par motif texte sont ligne à ligne ; les sélecteurs larges (par exemple s, θ, A) comptent toutes les occurrences du glyphe, y compris les rôles locaux, et surestiment la propagation. Le classement N0–N4 est un jugement documenté, non un calcul.

---

## 12. Décisions demandées

1. Valider G0.4 (catalogue, classement N0–N4, bilan des 50 clés) et autoriser le commit et la poussée sur `harmonisation/g0`, sans fusion dans `main`.
2. Valider la règle de N3 (réservation **et** proximité ou portée partagée), ou la modifier.
3. Confirmer que le catalogue `notations/collisions.yaml` doit être figé comme référence à la clôture (`G0_04_collisions/reference/`).
4. Fixer l'ordre de traitement des arbitrages de G0.5 (proposition : scientifiques S1–S2 d'abord, puis N3 intervolumes, puis internes au volume II).
5. Autoriser l'ouverture de G0.5 ; G0.4 s'arrête ici.

---

## 13. Addendum — intégration de F1 (clôture de G0.4)

Le diagnostic initial des §§ 1–12 est conservé tel qu'il a été remis ; le présent addendum consigne les modifications apportées par F1. Le catalogue figé (§ 13.5) reflète l'état après F1 et conserve, pour chaque collision reclassée, son niveau initial (`niveau_G04_initial`) et le motif du reclassement (`reclassement_F1`).

### 13.1 Règle N3 précisée (F1)

> Une collision N3 est une collision intervolumes entre objets distincts, dont les portées, les rôles ou les contextes d'utilisation présentent une proximité suffisante pour compromettre l'interprétation du corpus commun. La réservation explicite d'une notation par le volume II est un facteur aggravant qui détermine la priorité notationnelle lors de l'arbitrage ; elle n'est ni nécessaire ni suffisante.

Mise en œuvre : champ `facteur_aggravant: reservation_volume_II` (17 collisions) ; contrôle du script : un N3 est intervolumes et motive une proximité (dans `justification` ou `revue_F1`) ; tout niveau modifié porte un motif documenté.

### 13.2 Revue des neuf N3 initiaux

| Id | Décision | Motif |
|---|---|---|
| COL-RHO-01 | maintenu N3 | paramètre de protocole contre application des états, dans le même champ (lectures, réponses, équivalences) |
| COL-PRES-01 | maintenu N3 | même terme, objets distincts, contextes proches |
| COL-SIG-01 | maintenu N3 (**cas limite**) | dans les deux volumes, Σ est le lieu où l'on localise les changements d'issue : frontière ∂_D A et frontière relative de l'ensemble d'appropriation (annexes I, J) contre coupe portant la partition expérimentale \mathcal P_k(Σ) (volume II l. 873) ; proximité de rôle, indépendante de la réservation |
| COL-OME-01 | maintenu N3 | espace des paramètres de sonde contre domaine du paramètre caché (X077) |
| COL-VTH-01 | maintenu N3 | deux coordonnées de traces |
| COL-HIST-01 | maintenu N3 | même terme, propriétés distinctes, la seconde constitutive de la classe IWS |
| COL-U-01 | maintenu N3 | paramètre de sonde contre entrée, alors que les sondes sont réalisées par des entrées (X020) |
| **COL-PHI-01** | **N3 → N2** | transitions d'histoires contre homéomorphisme de paramétrisation d'une coupe : ni rôle ni contexte proches ; seule la réservation V5.16 motivait N3. La réservation reste un facteur aggravant, et la propagation (76 occurrences) est inchangée |
| **COL-C-01** | **N3 → N2** | l'ensemble de flot C est le même objet dans les deux volumes (X004) ; la collision oppose, au sein du volume I, C=b/(2a), l'épisode C et les cellules C_k à C, avec des types incompatibles et des contextes explicites ; il n'y a pas d'objets intervolumes distincts qui soient proches |

Revue des N2 intervolumes, sans facteur de réservation nécessaire : aucun reclassement vers N3 n'est justifié en l'état. Deux réexamens conditionnels sont consignés :

- COL-DEPTH-01 : les deux profondeurs mesurent la profondeur de séparation par des histoires, mais X037 est UNK et la distinction des objets n'est pas établie ; à réexaminer après S6 (G0.5a) ;
- COL-EQ-01 (avec COL-EQ-02) : à réexaminer si X028 est rejetée, auquel cas les objets seraient distincts sous le même terme « Nerode ».

| Niveau | N0 | N1 | N2 | N3 | N4 |
|---|---|---|---|---|---|
| Initial (§ 2) | 4 | 18 | 30 | 9 | 4 |
| Après F1 | 4 | 18 | **32** | **7** | 4 |

Effet sur les 50 clés : C passe de N3 à N2 (niveau maximal : N0 10, N1 22, N2 18, N3 0).

### 13.3 Rapprochement des occurrences de ρ (394 contre 395)

[CTRL] Les 394 occurrences du catalogue initial forment un **sous-ensemble exact** des 395 occurrences attribuées à la lecture par l'audit historique (`G0_01_inventory/coverage_rho_volI.csv`, attribution par plages). L'unique occurrence manquante est `I-009663` (annexe H, l. 286, `\mathbf 1_{A_{\mathcal P,\rho}}(\mathbf s)`), où ρ figure en indice d'indice (niveau 2). Les sélecteurs initiaux couvraient les niveaux 0 et 1 seulement. La différence tient donc au **périmètre de niveau**, et non à une différence d'attribution. Un sélecteur de niveau 2 a été ajouté : le catalogue compte désormais **395** occurrences, rapprochées une à une de l'audit (0 occurrence en plus, 0 en moins ; test `test_rho_395`).

Récapitulatif des 455 ρ du volume I : 141 au niveau 0, 313 au niveau 1, 1 au niveau 2 ; lecture 395 (COL-RHO-01), R1 48 (COL-RHO-02), valeur propre modale 8 et rayon spectral 4 (COL-RHO-03, 04).

### 13.4 Réemplois à préserver et corrections éventuelles

Un classement N0 ou N1 n'implique pas d'intervention dans les manuscrits. Le champ `intervention` distingue :

| Intervention | Sens | Collisions | Occurrences distinctes côté volume I |
|---|---|---|---|
| PRESERVER | réemploi légitime, aucune intervention | 10 (N0 : RHO-03, O-01, PHIV-01, LOC-01 ; N1 : RHO-04, V-01, G-01, M-01, LOC-02, LOC-03) | 791 |
| DOCUMENTER | mention documentaire (table des notations), texte inchangé | 5 (N1 : RESP-02, E-01, SYN-07, LAB-01, T-01) | 25 |
| CORRECTION_CANDIDATE | correction évidente, soumise à validation | 1 (N1 : SYN-04, typographie 𝔊_N / \mathcal G_N, 1 occurrence) | 1 |
| A_ARBITRER | décision de G0.5 | 49 : tous les N2–N4, plus 6 N1 (RHO-05, RHO-06, HYB-01, internes au volume II ; SYN-03, SYN-05, SYN-09, synonymies) | 2 803 |

[HYP] Dans les collisions A_ARBITRER, les sélecteurs larges (s, θ, A, q) incluent des rôles locaux qui seront eux-mêmes préservés : 2 803 est une borne supérieure du volume de correction. Occurrences distinctes des collisions N3 et N4 après F1 : 643 (au lieu de 760, du fait des deux reclassements).

### 13.5 Gel du catalogue (F2)

Référence figée : `audits/G0/G0_04_collisions/reference_F/`, qui contient `collisions.yaml` (copie du catalogue après F1), les sorties générées (`collisions.csv`, `collision_occurrences.csv`, `ambiguous_keys_coverage.csv`, `collisions_summary.json`), `mathfrak_X_occurrences.csv` et `REGLES.md` (règles de classification, contrôles et bilan quantitatif). Les décisions ultérieures porteront sur `notations/collisions.yaml` ; la référence conserve le diagnostic.

### 13.6 Contrôles après F1

[CTRL] `build_collisions.py` : 0 erreur ; 37 tests verts ; registre identique à `reference_305` ; table identique à `reference_E` ; inventaire G0.1 : 0 différence ; sources et dépôts connexes inchangés.
