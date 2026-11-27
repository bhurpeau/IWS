# G0.2 — Inventaire sémantique : rapport des objets

**Phase :** G0.2, soumise à validation ; G0.3 non entamée
**Date :** 27 novembre 2026
**Sources :** `Volume_I/`, `Volume_II/` identiques au commit de base `c74fa04` (tag `g0-baseline`) ; inventaire lexical de référence `05afddd`
**Registre :** `notations/registry.yaml` — **registre candidat, non normatif**

Conventions : **[CTRL]** contrôle exécuté ; **[CONSTAT]** fait établi par lecture ; **[HYP]** interprétation non vérifiée ; **[LIMITE]** limite de méthode.

> **Portée.** Ce rapport identifie et type des objets **à l'intérieur de chaque volume**. Il ne produit aucune identification intervolumes (G0.3), aucune décision de collision (G0.4) et aucune notation canonique : le champ `notation_canonique` est vide pour tous les objets. Les identifiants portent un préfixe de volume (`I.`, `II.`, `C.` pour les compagnons) précisément pour ne pas présumer d'identité : `I.CORE.STATE_SPACE` et `II.HYB.STATE_SPACE` sont deux entrées distinctes, même si G0.3 pourra les relier.

---

## 1. Méthode

1. **Repérage des sites de définition.** `notations/scripts/definition_sites.py` relève les lignes portant un indice de définition. Il produit `G0_02_semantic/definition_sites_*.csv` et `notation_keys_*.csv`. Indices retenus :
   - environnements `definition` et `candidate` ;
   - « on note », « désigne », « on appelle », « on définit », « on pose », « soit » ;
   - `:=` et `\resultheading{Définition}`.

   Ce relevé n'est qu'une aide à la lecture.
2. **Lecture des sources, dans l'ordre imposé :**
   - G0.2a, volume II : lecture intégrale des l. 73–580 (socle, présentation, historicité, efficacité, candidat, taxonomie, granularités, morphismes) ; lecture ciblée des l. 856–900, 1114–1195, 1297–1346 et 1659–1676 ; lecture des 94 sites de définition ;
   - G0.2b, noyau du volume I et annexes A–F : livre I l. 55–190, 286–300, 452–466, 525–600, 918–932 ; livre II l. 108–150, 296–312, 880–895 ; extraits des annexes B, C, D, E ;
   - G0.2c, livre III : l. 124–345 ;
   - G0.2d, annexes G–L : G l. 40–80, 165–335 et 596–606 ; H l. 14–36 et 52–57 ; I l. 485–505 ; K l. 50–125 et 340–355 ; L l. 168–182 ;
   - G0.2e, compagnons : paragraphes « État », « Impact » et « Données », plus `NOTES_V5_17.md`.
3. **Rédaction du registre.** Chaque objet reçoit une entrée sourcée (fichier, plage de lignes, label s'il existe). Les champs type, domaine et codomaine ne sont remplis que s'ils figurent dans la source ; sinon ils valent `null`.
4. **Rattachement aux occurrences.** `notations/scripts/link_registry.py` valide le schéma (unicité, statuts, dépendances, notation canonique vide) et applique les **sélecteurs** lexicaux de chaque objet à l'inventaire G0.1. Il produit `G0_02_semantic/registry_occurrences.csv`, `coverage_structuring_keys.csv` et `registry_summary.json`.
5. **Classement manuel** des principales clés non résolues (`G0_02_semantic/unresolved_classification.csv`).
6. **Contrôle qualité** par échantillon aléatoire (§ 8).

**Statuts.**
- `EXPLICIT` : définition identifiable (environnement, « on note », `:=`, liste déclarative).
- `IMPLICIT` : objet déterminable par le contexte, sans définition autonome.
- `AMBIGUOUS` : au moins deux lectures possibles, documentées.
- `UNDEFINED` : aucune définition suffisante dans le corpus.

Le motif de chaque attribution figure dans `motif_statut`. Une absence de définition explicite n'est pas présentée comme une erreur mathématique.

**Confiance.**
- `haute` : passage définitionnel lu intégralement.
- `moyenne` : lecture partielle ou définition dispersée.
- `faible` : non utilisé.

## 2. Bilan quantitatif

[CTRL] Résultats de `link_registry.py` : **95 objets**, 0 erreur de schéma, 0 sélecteur vide, 0 occurrence rattachée à plusieurs objets.

| Volume | Objets | EXPLICIT | IMPLICIT | AMBIGUOUS | UNDEFINED |
|---|---:|---:|---:|---:|---:|
| II (G0.2a) | 57 | 49 | 6 | 2 | 0 |
| I (G0.2b–d) | 36 | 31 | 2 | 2 | 1 |
| Compagnons (G0.2e) | 2 | 2 | 0 | 0 | 0 |
| **Total** | **95** | **82** | **8** | **4** | **1** |

Par phase, la répartition est la suivante :

| Phase | Objets |
|---|---:|
| G0.2a (volume II) | 57 |
| G0.2b (noyau et annexes A–F) | 20 |
| G0.2c (livre III) | 5 |
| G0.2d (annexes G–L) | 11 |
| G0.2e (compagnons) | 2 |

La confiance est haute pour 72 objets et moyenne pour 23.

Par nature (regroupement indicatif) :

| Nature | Objets |
|---|---:|
| Applications et fonctions (dont exécutions, cartes, distances) | 34 |
| Ensembles, sous-ensembles, familles, partitions | 23 |
| Paramètres, variables, indices | 13 |
| Structures, classes, catégories | 9 |
| Propriétés et hypothèses | 9 |
| Relations | 4 |
| Autre ou indéterminée | 3 |

Par portée :

| Portée | Objets |
|---|---:|
| Globale au volume | 36 |
| Sectionnelle (section, bloc, livre, groupe d'annexes) | 55 |
| Locale | 4 |

10 objets n'ont aucune occurrence rattachée, et c'est attendu. Ce sont :
- des propriétés ou hypothèses énoncées en prose, sans symbole propre : H1–H4, invariance d'admissibilité, compatibilité préfixe–état, C23^act ;
- des relations, que l'inventaire lexical n'extrait pas : `\preceq_{pref}`, `\equiv_k^{\mathcal H}`, `\sim_N`, `\sim_{\mathfrak B,\rho}` ;
- deux structures notées par un n-uplet sans glyphe propre : I.CORE.HYBRID_SYSTEM, II.KERNEL.DECOUPLED_READOUT.

## 3. Couverture des occurrences structurantes

Une **clé de notation** réunit un glyphe, son indice et son exposant, au niveau 0. Elle est dite **structurante** si elle compte au moins 5 occurrences dans le corpus. Ce critère lexical englobe aussi des variables génériques et muettes. Résultats (`coverage_structuring_keys.csv`) :

| Corpus | Clés structurantes | Occurrences | Rattachées | Taux |
|---|---:|---:|---:|---:|
| Volume II | 138 | 1 953 | 1 176 | **60,2 %** |
| Volume I | 307 | 7 877 | 2 781 | **35,3 %** |
| Compagnons | 58 | 763 | 220 | 28,8 % |

Lecture de ces taux :

- **Volume II.** Les clés non rattachées sont d'abord des variables génériques typées par des objets du registre (`x` 72, `t` 37, `y` 28, `\mathcal H` 27, `x_1`, `x_2` 26), des indices muets (`i`, `j`), des opérateurs usuels et des objets locaux de preuve (`\operatorname{Aut}`, `\sigma`, `h`). Le classement manuel est dans `unresolved_classification.csv`.
- **Volume I.** Le taux plus bas reflète d'abord la **lecture partielle des annexes A–F** : de nombreux seuils, constantes et variables de preuve n'y sont pas instruits (`g_{\mathrm{ign}}`, `\lambda` hors livre I, `\mathcal L` du livre III, `x^\ast`, `\Delta`, `z`). Il reflète ensuite des **réemplois lexicaux multiples** classés `AMBIGU_LEXICAL` (`C`, `D`, `B`, `\gamma`, `\Delta`, `\varepsilon`, `s`, `\theta`, `Y`). C'est la principale limite de G0.2 (§ 9).
- **Hors corpus mathématique.** Les relations, les propriétés et le texte ne relèvent pas de cette mesure.

**Occurrences non résolues.**

- La liste complète des clés `partielle` et `non_resolue` est dans `coverage_structuring_keys.csv` : 69 pour le volume II, 253 pour le volume I.
- Le classement manuel des principales (`unresolved_classification.csv`) utilise les catégories suivantes : `VARIABLE_GENERIQUE`, `INDICE_MUET`, `OPERATEUR_STANDARD`, `REGULARITE`, `OBJET_LOCAL`, `OBJET_LOCAL_NON_INSTRUIT`, `AMBIGU_LEXICAL`, `NON_INSTRUIT`.
- Les variables locales et muettes restent couvertes par l'inventaire G0.1 sans devenir des entrées du registre.

## 4. Principaux objets structurants

### 4.1. Volume II (référentiel cible)

| Domaine | Objets (identifiants) |
|---|---|
| Socle hybride | `II.HYB.BASE_SYSTEM` S=(\X,C,F,D,K;\Exec) ; `STATE_SPACE` \X ; `FLOW_SET` C ; `FLOW_GENERATOR` F ; `JUMP_SET` D ; `JUMP_OPERATOR` K ; `CASCADE_MAP` K^* (IMPLICIT) ; `EXEC_SEMANTICS` \Exec ; `EXECUTION` γ_{x,H} ; `WELL_POSEDNESS` H1–H4 (IMPLICIT) ; `ADMISSIBILITY_INVARIANCE` ; `AMBIENT_CLASS` \Hyb |
| Histoires | `II.HIST.MONOID` (\M,·,ε), avec renvoi explicite à l'annexe G du volume I ; `ADMISSIBLE_FAMILY` (\Madm_x) ; `ADMISSIBLE_UNION` \Madm ; `END_STATE` \End ; `CONTINUATIONS` H_0^{-1}\Madm_{x_0} ; `PREFIX_STATE_COMPATIBILITY` |
| Présentation et lectures | `II.PRES.PRESENTATION` \mathbf S ; `READOUT` ρ_X=(π_s,ρ_int) ; `STRUCT_READOUT` π_s ; `INTERNAL_READOUT` ρ_int ; `STRUCT_VALUES` \Sstruct (IMPLICIT) ; `INTERNAL_OBS_SPACE` Y_int (IMPLICIT) ; `OBS_SPACE` Y ; `STRUCT_PROJECTION` r_s ; `ADMISSIBLE_PAIRS` \mathcal E_I^{adm} ; `ORGANISATION_FIBRE` X_s ; `OPACITY_FIBRE_READOUT` (AMBIGUOUS) |
| Régime, historicité, efficacité | `II.EXP.REGIME` (I,\mathcal B) ; `HIST.EFFECTIVE_HISTORICITY` H_{ρ,I,B} ; `CHRONOLOGICAL_HISTORICITY` H_t^s (IMPLICIT) ; `STRUCTURAL_WORD` \Word_s ; `PREFIX_ORDER` ; `ORDINAL_HISTORICITY` H_ρ^{s,ord} ; `EFF.INTERNAL_RESPONSE` R_x^{ρ_int} ; `MAX_REPERTOIRE` \Rep^{max} ; `SUPPORT_REACH` (AMBIGUOUS) |
| Classe candidate | `II.CLASS.IWS_CANDIDATE` (C0, C1, C23^pot, C4) ; `C23_ACT` |
| Taxonomie, granularités, morphismes | `II.TAX.MECHANISM_WITNESSES` I1_ρ, I2 ; `GRAN.G1` ; `MOR.DYNAMIC_MORPHISM` (f,η), ψ_X ; `MOR.AMBIENT_CATEGORY` \Hyb_G |
| Profondeur finie et opacité | `II.DEPTH.DEPTH_RANK` k, r ; `OPAC.OPACITY_FIBRE` \mathcal O_y ; `OPAC.SECTION_PARAM` Σ, Ω, Φ, ϑ ; `OPAC.WORD_PARTITION` \mathcal P_k, Ξ, Ω_w ; `DEPTH_EQUIVALENCE` ≡_k^H ; `NERODE_EQUIVALENCE` ∼_N ; `SEPARATING_FAMILY` \mathcal U |
| Bloc du noyau | `II.WALLS.SCORES_WALLS` c_j^{(k)}, J_k^±, W_{ij}^{(k)}, \mathcal D_k ; `SA.DEPENDENCE_SUPPORT` Dep(Σ) ; `SA.SEMIALGEBRAIC_BLOCK` τ_⋆, a_i, s_i, χ_ij, \mathscr F_w ; `CONIC.BLOCK` μ, b_{j,w}^{(r)}, R_j, ρ_j, Δ_{j,w}^{(r)} ; `KERNEL.DECOUPLED_READOUT` ; `KERNEL.EXTERNAL_VARIABLES` (IMPLICIT) |

### 4.2. Volume I

| Partie | Objets |
|---|---|
| Noyau, livres I–II, annexes A–F (G0.2b) | `I.CORE.HYBRID_SYSTEM` ; `STATE_SPACE` \mathcal X ; `NODAL_VARIABLES` H_i, V_i, τ_i, P_i ; `GRAPH` \mathcal V, A, \mathfrak G_N, \widetilde A ; `FLOW_JUMP_SETS` Θ, C, D ; `KAIROS_OPERATOR` \mathcal K_i, ι, \mathcal K ; `REWIRING` \mathcal N(i^*), s(i,j), m ; `DISSIPATION_PRECONDITIONER` Γ, M, Q, λ, m_0 ; `DYNAMICS_PARAMETERS` α, β, ζ (IMPLICIT) ; `INPUT` u ; `LYAPUNOV` \mathcal L ; `B.ENERGY` E ; `II.TWO_SYSTEM_COUPLING` g, h_X, v_X ; `II.CRITICAL_COUPLING` g_c ; `R1.PERMEABILITY` q ; `R1.REOPENING_RATE` ρ (IMPLICIT) ; `C.MODAL_EIGENVALUE` ρ ; `E.SPECTRAL_RADIUS` ρ_sp ; `E.MONODROMY` Φ_g, \mathcal M_g ; `D.APPROPRIATION` |
| Livre III (G0.2c) | `I.III.EPISODES_HISTORIES` \mathcal E, Φ_e, Φ_H, ε ; `REALIZATION_SPACE` \mathfrak X ; `READING` ρ ; `EXECUTION` Exec_H(X) ; `RESPONSE` \mathcal R_X^ρ(H) |
| Annexes G–L (G0.2d) | `I.G.HISTORY_MONOID` \mathfrak M=\mathcal E^* ; `REALIZATION_SPACE` \mathfrak X (AMBIGUOUS) ; `ADMISSIBLE_CLASS` \mathfrak B ; `RESOLUTION` \mathcal Y_ρ, τ_ρ, ω_ρ ; `OBS_EQUIVALENCE` ∼_{B,ρ} ; `H.SLOW_SUMMARY_VARIABLES` p, χ, θ, \mathbf s ; `H.RESPONSE_MAP` Ω_{P,ρ} ; `L.SEPARATION_GEOMETRY` ℓ_{c,B,ρ}, d_{c,B,ρ} ; `I.OBSERVATION_DISTANCE` d_ρ (UNDEFINED) ; `K.CLASS_RESPONSE` \mathcal R^{B,ρ} (AMBIGUOUS) ; `K.AUGMENTED_STATE` |
| Compagnons (G0.2e) | `C.CERT.KERNEL_STATE_PARAMS` ; `C.CERT.IMPACT_SEQUENCE` |

## 5. Capitalisation sur les audits historiques

### 5.1. Audit ρ (`diag_rho_volI.md`)

[CTRL] Les quatre objets de l'audit sont repris comme entrées distinctes. Leurs sélecteurs reproduisent exactement les décomptes de l'audit sur les sources gelées :

| Entrée du registre | Objet de l'audit | Occurrences rattachées |
|---|---|---:|
| `I.R1.REOPENING_RATE` | coefficient R1 | 48 |
| `I.C.MODAL_EIGENVALUE` | valeur propre | 8 |
| `I.E.SPECTRAL_RADIUS` | ρ_sp | 4 |
| `I.III.READING` | lecture / résolution | 395 |

Le statut `IMPLICIT` du coefficient R1 reprend le constat de l'audit : son type et ρ>0 ne sont écrits qu'en annexe E.

[CONSTAT] L'audit regroupe « ρ, ρ_1, ρ_2… du Tome III » en un seul objet. Le registre conserve ce regroupement pour `I.III.READING`. Le registre n'examine pas si ρ_1, ρ_2 désignent des lectures distinctes d'une même famille : c'est à instruire en G0.3/G0.4.

### 5.2. Audit V5.16

[CTRL] Conventions reconfirmées par la lecture de V5.17 :

- `C` : ensemble de flot (l. 80) ;
- `\Xi` : chambre, c'est-à-dire composante connexe d'une classe de mot ; « classe de mot » reste distinct (l. 873) ;
- `\Sigma` : coupe ;
- `\Omega` : domaine paramétrique ;
- `\Phi` : homéomorphisme Ω→Σ ;
- `\vartheta` : paramètre caché (l. 875) ;
- `\operatorname{Dep}(\Sigma)` (l. 1443) ;
- `k` : profondeur, et `r` : rang local avec 1≤r≤k (l. 1299) ;
- `\mathscr F_w` : famille de polynômes (l. 1615) ;
- `v` : fonction-score du lemme orbital (l. 771) ;
- `s_i` : norme carrée (l. 1549) ;
- `\tau_\star` (l. 1545) ;
- `R_j` maintenu à côté de la norme initiale `\rho_j` (l. 1663).

[CONSTAT] **Symboles nouveaux dans V5.17 et symboles simplement absents du tableau V5.16.**

- D'après `NOTES_V5_17.md` (corpus auxiliaire), V5.17 ajoute surtout la sous-section « Transmission régulière à profondeur finie et certification des huit premiers Kairos » (l. 1787–1833).
- **Aucun glyphe** n'y apparaît pour la première fois.
- Seules six clés de notation y sont nouvelles : `q_0`, `T_r`, `V_j`, `H_j`, `t^{2m+1}`, `t^{2m+2}` (`v517_new_symbols.json`). Elles reprennent des objets des compagnons (q=(ϑ,ε), T_r) et du noyau.
- Les 131 glyphes de niveau 0 hors tableau V5.16 (151, tous niveaux confondus) apparaissent tous **avant** cette sous-section. Ce sont donc des symboles absents du tableau ciblé de V5.16, non des objets introduits par V5.17. Une bonne part sont des variables génériques ou muettes (§ 3).

[LIMITE] La source V5.16 n'est disponible dans aucun dépôt : on ne peut pas confronter ligne à ligne les autres sections. Les écarts de décompte (`\vartheta` +1, `u` −1, `b_{i,w}`/`λ_{r,w}` +7) restent à expliquer.

## 6. Cas d'étude demandés

### 6.1. `d_\rho` (annexe I, l. 497) → `I.I.OBSERVATION_DISTANCE`, **UNDEFINED**

[CONSTAT]

- **Occurrence unique** : la borne d_ρ(\widehat Ω(p,χ,θ,s), Ω(s)) ≤ L_p|p|+L_χ|χ|+L_θ|θ| (§ « Extinction approchée »).
- **Indices de sens** : le contexte compare deux valeurs de réponse et évoque « une lecture binaire munie de la distance discrète ». On peut donc présumer une distance sur l'espace d'observation [HYP].
- **Aucune définition trouvée** : recherche de `d_\rho`, `d_{\rho`, « distance », « métrique » dans le livre III et les annexes G–L. Aucun passage ne munit \mathcal Y_ρ d'une distance.
- **Dépendances** : lecture ρ (I.III.READING), cartes Ω, \widehat Ω (annexes H–I).
- **Objet voisin à ne pas confondre** : d_{c,\mathfrak B,ρ}(X,Y)=exp[−ℓ_{c,\mathfrak B,ρ}(X,Y)] (annexe L, eq:annexe-L-distance), défini, qui porte sur des paires de systèmes. Le premier sélecteur de `d_\rho` captait ces 6 occurrences ; il a été corrigé.
- **Statut** : UNDEFINED ; aucune correction ni définition proposée (anomalie A-G02-04).

### 6.2. `\mathcal R^{\mathfrak B,\rho}` (annexe K, l. 101 et 348) → `I.K.CLASS_RESPONSE`, **AMBIGUOUS**

[CONSTAT]

- **Deux occurrences**, dans l'hypothèse (P5) (« la lecture ω_ρ et la réponse \mathcal R^{\mathfrak B,ρ} dépendent de l'exécution produite ») et dans la décision D-08 (« ne constitue pas un invariant de \mathcal R^{\mathfrak B,ρ} »).
- **Aucune définition** de cette forme.
- **Formes voisines**, ailleurs et dans la même annexe :
  - la réponse définie est \mathcal R_X^ρ(\mathcal H) (livre III l. 304, annexe G) ;
  - l'annexe K emploie aussi \mathcal R_{pl}^ρ(\mathcal H), \mathcal R_{fig}^ρ(\mathcal H) (l. 186–188) et \mathcal R^ρ_{z_5}(\mathcal P) (l. 264).
- **Au moins deux lectures** [HYP] :
  - la famille des réponses X ↦ (\mathcal H ↦ \mathcal R_X^ρ(\mathcal H)) restreinte à \mathfrak B ;
  - la réponse générique d'une présentation sur la classe.
- **Dépendances** : I.III.RESPONSE, I.G.ADMISSIBLE_CLASS.
- **Statut** : AMBIGUOUS ; ni correction ni définition proposée (anomalie A-G02-05).

## 7. Ambiguïtés et anomalies constatées

Les anomalies sont détaillées dans `RESERVES.md`. Aucune n'est corrigée.

| Id | Objet(s) | Constat |
|---|---|---|
| A-G02-01 | `II.PRES.OPACITY_FIBRE_READOUT`, `II.OPAC.OPACITY_FIBRE` | « fibre d'opacité » désigne ρ_X^{-1}(s,y_int) (l. 185) puis ρ_X^{-1}(y)∩C (l. 863). **Notation ambiguë interne au volume II** : décision explicite requise (règle du plan § 1.1) |
| A-G02-02 | `II.EFF.SUPPORT_REACH` | \Supp employé l. 300 avant toute définition ; \Reach^{flow} employé l. 484 sans définition |
| A-G02-03 | `I.D.APPROPRIATION` | Deux énoncés de définition : `def:t2-appropriation` (livre II l. 640) et `def:D-appropriation` (annexe D l. 1429) ; équivalence non vérifiée |
| A-G02-04 | `I.I.OBSERVATION_DISTANCE` | d_ρ non défini (§ 6.1) |
| A-G02-05 | `I.K.CLASS_RESPONSE` | \mathcal R^{B,ρ} non défini et ambigu (§ 6.2) |
| A-G02-06 | `II.HYB.WELL_POSEDNESS` et compagnons | H1–H4 du socle du volume II (« regroupées provisoirement », sans répartition) ; la note de consolidation et les compagnons emploient (H1)–(H5) pour d'autres hypothèses (transmission C²) : même étiquette, familles distinctes |
| A-G02-07 | `II.HYB.AMBIENT_CLASS`, `II.MOR.AMBIENT_CATEGORY` | \Hyb désigne une classe (l. 99), \Hyb_G une catégorie (l. 569) |

**Réemplois lexicaux relevés pour G0.4** (non arbitrés) :

- au volume I, `A` désigne la matrice d'adjacence (livre I) et le système source (livre II) ;
- `C` désigne l'ensemble de flot et la constante C=b/(2a) (livre I l. 1057) ;
- `D` désigne l'ensemble de saut et des domaines (annexes J l. 65, K l. 79) ;
- `\tau_\rho`, lecture terminale (annexe G), partage le glyphe de la trace τ ;
- `q` désigne la perméabilité R1 (volume I) et le paramètre (ϑ,ε) (compagnons, volume II l. 1796) ;
- `\Omega` désigne le domaine paramétrique (volume II) et la carte de réponse Ω_{P,ρ} (volume I, annexes H–K) ;
- `\rho_j` (norme initiale, volume II) appartient à la famille ρ ;
- `\mathfrak X` est défini par une alternative « états complets ou présentations » (annexe G, AMBIGUOUS).

## 8. Échantillon argumenté de contrôle qualité

[CTRL] **Échantillon aléatoire stratifié.** Graine 2026, un rattachement tiré dans chacun de 30 objets distincts.

**28 corrects**, dont :

- Φ_g dans \mathcal M_g=R_VΦ_g(Δ(g)) (annexe E l. 1231) ;
- \Reach^{flow} (II l. 484) ;
- η dans les conditions de morphisme (II l. 559) ;
- \mathcal O_y dans la définition de famille séparante (II l. 1181) ;
- \mathcal X dans la définition de D (livre I l. 549) ;
- ρ dans \widehat\Omega^{(5)}_{P,ρ} (annexe K l. 290) ;
- ρ_X (II l. 153) et ρ_int en exposant de R (II l. 1145) ;
- ρ_X^{-1}(s,y_int) (II l. 185) ;
- κ_1 dans \dot P_j (compagnon l. 30) ;
- \mathcal N^c(i^*) (annexe A l. 940) ;
- \mathcal Y_ρ (annexe G l. 228) ;
- ρ_sp(\mathcal M_g) (annexe F l. 479) ;
- et 15 autres de même nature.

**2 recevables avec réserve :**

- `S` dans (f,η):S→T (II l. 549) est une variable du type « système hybride de base », non l'objet générique lui-même ;
- `g` dans Δ(g) (annexe E l. 1348) n'est rattaché à l'intensité de couplage que par la portée du sélecteur (annexes C–F).

[CTRL] **Sélecteurs larges contrôlés**, 8 tirages chacun : I.CORE.NODAL_VARIABLES (846 occurrences), II.KERNEL.EXTERNAL_VARIABLES (369), II.DEPTH.DEPTH_RANK (89). Les 24 tirages sont cohérents avec l'objet.

Une réserve : τ, argument générique de M(τ) ou Q(τ), est rattaché aux variables nodales comme variable du même type.

[CTRL] **Défauts corrigés pendant la phase.**

- Le sélecteur de d_ρ captait d_{c,B,ρ} (§ 6.1).
- Des recouvrements entre objets (I des témoins I1/I2 et I du régime ; H_ρ et H_ρ^{s,ord} ; \M et \Madm ; b_{j,w} des blocs semi-algébrique et conique) ont été éliminés : 0 rattachement multiple à l'issue.

## 9. Limites de la méthode

- **[LIMITE] Lecture partielle du volume I.** Les annexes A–F et la seconde moitié du livre III n'ont été lues que par extraits. Le registre du volume I couvre le noyau, R1, les quatre objets ρ, les objets formels de G et quelques objets de H–L. De nombreux seuils et constantes des annexes A–F restent non instruits. C'est la principale réserve avant G0.3 (R-G0-10).
- **[LIMITE] Sélecteurs lexicaux.** Un sélecteur délimite une portée (glyphe, indice, fichier, lignes) ; il ne prouve pas l'identité de chaque occurrence. Les sélecteurs larges sont signalés dans `remarques` et contrôlés par échantillon.
- **[LIMITE] Relations et propriétés.** Elles ne sont pas inventoriées lexicalement, donc leurs occurrences ne sont pas comptées.
- **[LIMITE] Nature et portée.** Ce sont des descriptions textuelles ; le regroupement du § 2 est indicatif.
- **[LIMITE] Format du registre.** `registry.yaml` est écrit en syntaxe JSON (sous-ensemble de YAML 1.2), faute de PyYAML installé. Aucune dépendance n'a été installée.
- **[LIMITE] Compagnons.** Seuls deux objets sont enregistrés ; ce corpus auxiliaire sert surtout de provenance (B4).

## 10. Livrables

| Fichier | Contenu |
|---|---|
| `notations/registry.yaml` | registre candidat (95 objets) |
| `audits/G0/G0_02_objects_report.md` | le présent rapport |
| `audits/G0/RESERVES.md` | anomalies et réserves G0.2 |
| `audits/G0/G0_02_semantic/registry_occurrences.csv` | occurrences ↔ objets |
| `audits/G0/G0_02_semantic/coverage_structuring_keys.csv` | couverture par clé et liste des clés non résolues |
| `audits/G0/G0_02_semantic/unresolved_classification.csv` | classement manuel des principales clés non résolues |
| `audits/G0/G0_02_semantic/registry_summary.json` | bilan, distributions, contrôles |
| `audits/G0/G0_02_semantic/definition_sites_*.csv`, `notation_keys_*.csv` | aides à la lecture |
| `audits/G0/G0_02_semantic/v517_new_symbols.json` | symboles et clés propres à la sous-section ajoutée par V5.17 |
| `notations/scripts/definition_sites.py`, `link_registry.py`, `check_regression.py` | outils (lecture seule) |

Reproduction :

```bash
python3 -I notations/scripts/definition_sites.py
```

```bash
python3 -I notations/scripts/link_registry.py
```

## 11. Porte de validation G0.2

| Critère du plan | État |
|---|---|
| Objets structurants identifiés, typés et sourcés | **Atteint pour le volume II** (socle, présentation, historicité, classe candidate, profondeur finie). **Partiel pour le volume I** (noyau, R1, livre III et formalisme G atteints ; annexes A–F et H–L partiellement) |
| Ambiguïtés explicitement marquées | Atteint (4 AMBIGUOUS, 1 UNDEFINED, 7 anomalies, réemplois listés) |
| Aucune identité intervolumes, aucune notation canonique, aucun manuscrit modifié | Atteint |

Arbitrages demandés : voir `STATUS.md`, décisions C1 à C5.
