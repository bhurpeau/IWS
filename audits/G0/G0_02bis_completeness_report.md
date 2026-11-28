# G0.2bis — Complétude et consolidation de l'inventaire sémantique

**Date :** 27 novembre 2026
**Branche :** `harmonisation/g0` (non fusionnée dans `main`)
**Sources :** commit `c74fa04` (aucune modification des manuscrits ; `git diff c74fa04 -- Volume_I Volume_II` vide)
**Référence comparée :** registre candidat intermédiaire de G0.2, itération 1 (95 objets), figé dans `G0_02_semantic/reference_95/` (commit `2588875`)
**Statut :** soumis à validation. G0.3 n'est pas ouverte (décision C5).

Les marqueurs suivants distinguent la nature des affirmations, comme demandé :

- **[CONTRÔLE]** contrôle réalisé ;
- **[IMPOSSIBLE]** contrôle impossible ou non réalisé ;
- **[CONSTAT]** fait établi par lecture ou calcul ;
- **[HYPOTHÈSE]** supposition non vérifiée ;
- **[LIMITE]** limite de méthode.

## 1. Objet et périmètre

G0.2bis exécute la décision C3 : compléter la lecture du volume I, vérifier la complétude du volume II, consolider le registre, établir une matrice de couverture documentaire et classer les occurrences non rattachées. Elle applique aussi :

- **C1** : registre qualifié de « candidat intermédiaire » ; état de référence des 95 objets conservé ;
- **C2** : deux fibres d'opacité ;
- **C4** : registre en YAML lisible ;
- le **complément sur la granularité** des entrées collectives.

Ce qui n'a pas été fait, conformément aux consignes :

- aucune notation canonique choisie ;
- aucune identité intervolumes présumée ;
- aucune question mathématique résolue ;
- aucun manuscrit ni dépôt connexe modifié.

## 2. Méthode

1. **Lecture journalisée.** `G0_02bis/reading_log.csv` enregistre, pour chaque fichier, les plages lues, la phase et le mode (intégrale, intégrale déclarée, extraits).
   - Lus intégralement en G0.2bis : les annexes A–L, le livre III, les livres I et II, la table des énoncés, le corps de `main.tex` et les deux notes compagnons.
   - Le volume II avait été lu intégralement en G0.2 ; ses 31 énoncés formels non couverts ont été relus en G0.2bis.
2. **Inventaire des sections et des énoncés formels.** Le script `formal_environments.py` relève :
   - les sectionnements ;
   - les environnements de type théorème ;
   - les énoncés numérotés du volume I (`\resultheading`, `\resultstep`), qui n'utilisent pas d'environnements LaTeX ;
   - les encadrés et les paragraphes étiquetés, comme (E1), (A1), (P1) ou O1.
3. **Contrôle de complétude.** Pour chaque énoncé formel et chaque site de définition (« on note », « := », « désigne »…), on vérifie qu'un objet du registre couvre le passage. Chaque passage non couvert a été lu ; il a soit donné lieu à un objet, soit été classé.
   - Les 198 passages restants sont consignés dans `G0_02bis/definition_sites_review.csv` : 77 énoncés de résultat, 50 faux positifs (« soit » verbal), 34 déclarations locales, 32 sites secondaires d'objets enregistrés, 5 passages liminaires.
   - Ce contrôle a fait ajouter quatre objets du volume II : convention de fibre, u_max, \mathcal W_k, Y_adm.
4. **Critère de couverture.**
   - Est **structurant** un objet doté d'une définition, d'un type ou d'un rôle propre, et réemployé hors de son passage ou nommé par le texte.
   - Les quantités intermédiaires d'une preuve ou d'un calcul restent locales : elles sont classées, non enregistrées.
   - Aucun pourcentage lexical n'a été visé.
5. **Granularité.**
   - Chaque entrée est une `famille` ou un `element`.
   - Une famille liste ses `composants`, qui y renvoient par `familles` ; ce lien réciproque est contrôlé.
   - Une famille sans composants porte un `motif_granularite`.
   - Les sélecteurs sont portés par les éléments.
6. **Traçabilité.** Chaque modification d'une entrée est enregistrée dans son champ `revisions` (nature et motif). Le différentiel est calculé automatiquement par `registry_diff.py`.

## 3. Bilan quantitatif

| | Itération 1 (G0.2) | Itération 2 (G0.2bis) |
|---|---:|---:|
| Objets | 95 | **301** |
| Volume I / volume II / compagnons | 36 / 57 / 2 | 205 / 88 / 8 |
| EXPLICIT / IMPLICIT / AMBIGUOUS / UNDEFINED | 82 / 8 / 4 / 1 | 265 / 28 / 5 / 3 |
| Confiance haute / moyenne | 72 / 23 | 262 / 39 |
| Éléments / familles | — | 271 / 30 |
| Erreurs de schéma ; rattachements multiples ; sélecteurs vides | 0 ; 0 ; 0 | 0 ; 0 ; 0 |

Les 206 objets ajoutés se répartissent ainsi :

- 110 viennent de la lecture intégrale des annexes A–F, H–L et du livre III ;
- 61 sont des composants issus des décompositions (§ 7) ;
- 18 viennent de la relecture des livres I, II et de l'annexe G ;
- 17 viennent des énoncés formels et des sites de définition du volume II, et des compagnons.

**[CONSTAT]** Part des occurrences des clés structurantes (au moins 5 occurrences, niveau 0) rattachée à un objet :

| | Itération 1 | Itération 2 |
|---|---:|---:|
| Volume I | 35,3 % | 69,9 % (5 508 / 7 877) |
| Volume II | 60,2 % | 63,8 % (1 246 / 1 953) |
| Compagnons | 28,8 % | 50,8 % (388 / 763) |

Ce taux n'est pas un objectif. Le reste est classé au § 11.

## 4. Matrice de couverture documentaire

- **Fichiers produits :**
  - `G0_02bis/coverage_matrix.csv` : 390 unités (chapitres et sections) ;
  - `coverage_matrix_by_file.csv` : synthèse par fichier.
- **Colonnes de chaque unité :**
  - statut de lecture ;
  - nombre d'énoncés formels et de définitions ;
  - objets définis dans l'unité ;
  - occurrences et part rattachée ;
  - occurrences structurantes non rattachées, ventilées par catégorie de classement ;
  - clés principales non rattachées.

**[CONTRÔLE]** Les 390 unités sont lues intégralement : 375 en G0.2bis et 15 (volume II) en G0.2. Aucune unité non lue ; aucune occurrence non classée.

| Fichier | Unités | Énoncés | Objets définis | Occurrences niv. 0 | Rattachées |
|---|---:|---:|---:|---:|---:|
| Livre I | 40 | 6 | 41 | 818 | 73,1 % |
| Livre II | 65 | 5 | 13 | 666 | 76,4 % |
| Livre III | 45 | 1 | 24 | 822 | 59,2 % |
| Annexe A | 18 | 4 | 7 | 744 | 58,7 % |
| Annexe B | 13 | 1 | 7 | 660 | 83,2 % |
| Annexe C | 21 | 4 | 13 | 1 016 | 65,2 % |
| Annexe D | 27 | 3 | 15 | 919 | 77,7 % |
| Annexe E | 10 | 2 | 17 | 669 | 80,9 % |
| Annexe F | 32 | 0 | 5 | 328 | 79,6 % |
| Annexe G | 15 | 12 | 19 | 454 | 52,0 % |
| Annexe H | 14 | 19 | 15 | 446 | 73,1 % |
| Annexe I | 14 | 16 | 9 | 399 | 59,9 % |
| Annexe J | 16 | 8 | 5 | 216 | 69,9 % |
| Annexe K | 15 | 14 | 9 | 257 | 73,9 % |
| Annexe L | 14 | 13 | 6 | 293 | 33,4 % |
| Volume II | 15 | 45 | 77 | 2 521 | 60,8 % |
| Compagnon certification | 9 | 4 | 1 | 376 | 32,4 % |
| Compagnon transmission | 7 | 10 | 7 | 658 | 47,9 % |

« Objets définis » compte les objets dont le site de définition commence dans le fichier. Un objet défini ailleurs peut être rattaché dans plusieurs fichiers.

Les taux faibles des annexes G et L et des compagnons s'expliquent par la forte proportion de variables génériques : réalisations X et Y, histoires \mathcal H, variables locales des preuves (§ 11).

## 5. Complétude du volume II

- **[CONTRÔLE]** 45 énoncés formels relevés. Les 31 non couverts (propositions, lemmes, crash-tests, remarques, questions) ont été relus, ainsi que tous les sites de définition non couverts.
- **[CONSTAT]** Objets ajoutés :
  - `II.KERNEL.ANTISYMMETRIC_TRACE_INCREMENT` (Δτ_h) et `II.KERNEL.HIDDEN_TRACE_DIFFERENCE` (Δτ_j) : même schéma de notation pour deux objets différents ;
  - `II.SYM.GRAPH_AUTOMORPHISMS` (Aut(A), σ, Π_σ) et `II.SYM.TRACE_STABILISER` (Aut_k^τ) ;
  - `II.OPAC.SELECTION_MARGIN` (mar_q^{(r)}, i_r^*, m_r) ;
  - `II.OPAC.JOINT_REACHABLE_SET` (\mathcal R_0^{(1,2)}(\mathcal U_4)) ;
  - `II.TRANS.PROTOCOL_PARAMETER` (q, q_0) et `II.TRANS.EIGHT_KAIROS_NEIGHBOURHOOD` (V5.17) ;
  - `II.QUEST.C5` et `II.GRAN.G2`, toutes deux UNDEFINED : objets annoncés, non définis ;
  - `II.PRES.FIBRE_CONVENTION`, `II.KERNEL.INPUT_BOUND` (u_max défini comme borne essentielle d'une entrée donnée, « non un paramètre fixé du modèle », alors que le volume I pose ‖u_i‖≤u_max en hypothèse : différence de statut à examiner en G0.3), `II.OPAC.REALIZABLE_WORDS` (\mathcal W_k) et `II.KERNEL.ADMISSIBLE_READINGS` (Y_adm, espace des traces T) ;
  - la décomposition de `II.EFF.SUPPORT_REACH` et de `II.OPAC.SECTION_PARAM`, et l'élément `II.OPAC.CHAMBER` (Ξ).
- **[CONSTAT]** Les autres énoncés n'introduisent que des objets locaux à leur preuve : groupe G et score v du lemme orbital, constantes B_sa et B_conn, quantités du témoin conique. Ils figurent dans le classement des non-rattachés.
- **[CORRECTION]** La plage de définition de `II.KERNEL.EXTERNAL_VARIABLES` (l. 580–1925) était une plage d'usage. Elle faisait passer pour couverts 31 énoncés qui ne l'étaient pas. Elle a été déplacée dans `portee`.

## 6. Compagnons

- Notes lues intégralement : transmission, et certification (l. 1–154).
- Objets ajoutés :
  - `C.TRANS.HYPOTHESES` ((H1)–(H5)) ;
  - `C.TRANS.EPISODE_DYNAMICS` ;
  - `C.TRANS.STATE` ;
  - `C.TRANS.REGULARITY_NEIGHBOURHOOD`.
- **[CORRECTION]** `C.CERT.SECTION_PARAMETER` et `C.CERT.KERNEL_PARAMS` pointaient vers le mauvais fichier.
- **[CONSTAT]**
  - Les paramètres déclarés par la certification sont numériquement égaux au jeu de référence du volume I (annexe F l. 132). C'est un constat, non une identité.
  - Le ε du compagnon est un paramètre de déformation, (γ_1,λ)=ε(γ̄,λ̄) ; il est distinct du ε du terme croisé (volume I, annexe B).
  - Selon sa section « Statut », la note de transmission présente (H1)–(H5) comme « étayées, non certifiées » ; la note de certification les certifie. La différence reflète l'ordre de rédaction des deux notes ; elle n'a pas été instruite.

## 7. Granularité : familles et objets élémentaires

**Règle appliquée.** Une famille est conservée lorsqu'elle organise le registre. Un composant est individualisé lorsqu'il possède une définition, un type ou un rôle propre et peut faire l'objet d'une correspondance intervolumes individuelle. Aucune atomisation sans justification.

| Famille (itération 1) | Composants individualisés | Justification |
|---|---|---|
| `I.CORE.NODAL_VARIABLES` | H_i, V_i, τ_i, P_i | sous-sections dédiées du livre I ; rôles distincts |
| `I.CORE.DYNAMICS_PARAMETERS` | α, β, ζ ; **ajoutés** κ_1, κ_2, κ_3, r_P, r_V | rôles déclarés au tableau des paramètres de référence (annexe F l. 132) |
| `I.CORE.DISSIPATION_PRECONDITIONER` | Γ, (γ_0, γ_1), Q, M, λ, m_0 | γ_0 et γ_1 restent groupés : le volume II les emploie conjointement (régime γ_1=λ=0) |
| `I.CORE.FLOW_JUMP_SETS` | Θ, C, D | le volume II a des objets C et D propres (G0.3) |
| `I.CORE.GRAPH` | \mathcal V/N, d, A, \mathfrak G_N, \widetilde A | types distincts |
| `I.H.SLOW_SUMMARY_VARIABLES` | p, χ, θ, \mathbf s | rôles distincts (éteintes ou survivante) |
| `I.G.RESOLUTION` | \mathcal Y_ρ, τ_ρ, ω_ρ | lectures terminale et de chemin distinctes (audit ρ) |
| `I.III.EPISODES_HISTORIES` | épisodes, transitions, histoires | types distincts |
| `I.II.TWO_SYSTEM_COUPLING` | g, états (h_X, v_X, τ_X) | g gouverne tous les seuils |
| `I.L.SEPARATION_GEOMETRY` | ℓ, d | deux objets définis séparément |
| `II.KERNEL.EXTERNAL_VARIABLES` | A, H, V, P, N, Θ, ζ, τ, (γ_0,γ_1), λ | chaque usage du noyau devient un élément IMPLICIT, en vue de G0.3 |
| `II.OPAC.SECTION_PARAM` | Σ, Ω, Φ, ϑ | réservations V5.16 ; homonymes au volume I |
| `II.OPAC.WORD_PARTITION` | Ξ (chambre) | réservé par l'audit V5.16 |
| `II.EFF.SUPPORT_REACH` | \Supp, \Reach | statuts et anomalie distincts |
| `C.CERT.KERNEL_STATE_PARAMS` | q=(ϑ,ε), jeu de paramètres, état x′, P | provenance distincte |
| `I.R2.PARAMETERS` (nouvelle) | λ_χ, κ_Q, r_χ, κ_χ | rôles distincts |

Familles **non décomposées**, chacune avec un motif dans le registre :

- blocs techniques du volume II : `II.WALLS.SCORES_WALLS`, `II.SA.SEMIALGEBRAIC_BLOCK`, `II.CONIC.BLOCK`, `II.SA.DEPENDENCE_SUPPORT`, `II.GRAN.G1`, `II.TAX.MECHANISM_WITNESSES` ;
- jeux d'hypothèses énoncées ensemble : (E1)–(E3), (A1)–(A4), (P1)–(P6), (H1)–(H5), (O1)–(O3) ;
- `I.C.REFERENCE_PARAMETERS` et `C.CERT.KERNEL_PARAMS`.

`I.CORE.KAIROS_OPERATOR` est conservé comme élément : \mathcal K_i et \mathcal K=\mathcal K_{ι(x)} se définissent l'un par l'autre.

**[CONTRÔLE]** Conservation des rattachements dans les décompositions : chaque famille passe à 0 occurrence propre et ses composants reçoivent ses sélecteurs à l'identique. Les écarts entre l'ancien total de la famille et la somme de ses composants proviennent uniquement de deux sources : les corrections de sélecteurs de R-G0-11 (ancrage des fichiers, exclusion des décorations \bar, \widetilde), et les sélecteurs ajoutés (κ_i, r_P, r_V, D, portée étendue aux annexes C–F). Le détail est dans `registry_diff.csv`.

## 8. Fibres d'opacité (décision C2)

- `II.PRES.OPACITY_FIBRE_READOUT` : « fibre d'opacité complète » (provisoire), ρ_X^{-1}(s,y_int) ⊆ X_s (l. 185).
  - Son statut passe d'AMBIGUOUS à EXPLICIT : l'ambiguïté porte sur le terme, non sur l'objet.
- `II.OPAC.OPACITY_FIBRE` : « fibre d'opacité admissible au flot » (provisoire), \mathcal O_y := ρ_X^{-1}(y)∩C (l. 863).
- Relations documentées dans les deux sens : `restriction` et `restriction_de`, avec O_y = ρ_X^{-1}(y)∩C = (ρ_X|_C)^{-1}(y). L'égalité n'est pas présumée.
- L'arbitrage terminologique est renvoyé à G0.5 (A-G02-01).

## 9. Les deux définitions de l'appropriation (A-G02-03)

| | `I.II.APPROPRIATION` (livre II) | `I.D.APPROPRIATION` (annexe D) |
|---|---|---|
| Site | l. 619–665, `def:t2-appropriation`, [DEF] | l. 1406–1469, `def:D-appropriation` |
| Signature | (g,T,\mathcal P) appropriée depuis z_0 ⇔ ω_0(y_T)=\mathcal A, ω_0(z_0)=\mathcal A_0, \mathcal A≠\mathcal A_0, avec y_T=Φ^T_{g,\mathcal P}(z_0) | (g,T,\mathcal P) appropriée depuis z_0 ⇔ ω_0(Φ^T_{g,\mathcal P}(z_0))=\mathcal A_1, ω_0(z_0)=\mathcal A_0, \mathcal A_1≠\mathcal A_0 |
| Hypothèses | z_0 état de B avant l'interaction ; couplage d'intensité g pendant T selon \mathcal P, puis supprimé ; ω_0 ensemble limite de la dynamique autonome ; \mathcal A_0, \mathcal A attracteurs autonomes de B | retour à la dynamique autonome après l'interaction ; \mathcal A_0, \mathcal A_1 attracteurs autonomes du receveur ; attracteurs non nécessairement ponctuels (régimes hybrides invariants, l. 1456 ; annexe C l. 1721) |
| Portée | livre II (dyade A→B) ; exclusions : réponse temporaire, copie maintenue, transmission de la mémoire de A | annexe D ; mêmes exclusions (l. 1460–1469) |
| Objets communs | `I.D.INTERACTION_MAP`, `I.D.LIMIT_SET`, `I.II.AUTONOMOUS_ATTRACTORS`, `I.D.CONTACT_PROTOCOL` | idem |

**[CONSTAT]** La table des énoncés renvoie la définition du livre II à « Ann. D.3 ». Les deux énoncés diffèrent par la notation de l'attracteur final et par l'extension explicite aux régimes hybrides. **Leur équivalence n'est pas affirmée.**

## 10. Classe et catégories \Hyb (A-G02-07)

**[CONSTAT]** Deux niveaux d'abstraction et deux formes notationnelles :

- \Hyb (sans indice, macro → \mathfrak H) est une **classe d'objets** (l. 99–101) ;
- \Hyb_G est une **catégorie** construite sur cette classe à granularité G (l. 569), toujours indicée (\Hyb_{G_0}, \Hyb_{G_1}, \Hyb_G^{obs}).

Ce n'est donc pas une collision de notation au sens strict.

**[CONSTAT]** Il reste deux points :

- \Hyb_{G_0} ⊆ \Hyb_{G_1} (l. 506) est écrit avant la phrase qui introduit \Hyb_G (l. 569) ;
- cette inclusion porte sur les flèches, et son sens catégorique (sous-catégorie avec les mêmes objets) reste implicite.

Les champs `niveau_abstraction` et `forme_notationnelle` sont renseignés, et une relation `construite_sur` relie la catégorie à la classe.

## 11. Classement des occurrences non rattachées

**Fichiers :**

- `G0_02bis/unresolved_classification.csv` : classement ;
- `unresolved_manual.csv` : table manuelle, 233 clés justifiées ;
- `notations/scripts/classify_unresolved.py` : règles.

**Champ :** toutes les clés structurantes encore partiellement ou non rattachées.

| Catégorie | Volume I (clés / occ.) | Volume II | Compagnons |
|---|---:|---:|---:|
| Variables locales ou génériques | 54 / 993 | 42 / 490 | 26 / 290 |
| Indices et variables muettes | 2 / 32 | 2 / 28 | 0 |
| Notations mathématiques usuelles | 24 / 382 | 8 / 66 | 5 / 60 |
| Objets structurants non instruits | **0** | **0** | **0** |
| Usages ambigus (plusieurs rôles d'un même glyphe) | 37 / 962 | 11 / 123 | 2 / 25 |
| Usages non résolus | **0** | **0** | **0** |

- **[CONSTAT]** Les trois clés classées « structurant non instruit » lors d'une première passe ont été instruites :
  - R_b, variante de \widehat R (A-G02-11) ;
  - i* (nœud sélectionné) ;
  - x_A (état de la source).
- **[LIMITE]** Une clé classée USAGE_AMBIGU peut couvrir un objet structurant déjà enregistré : ses occurrences hors sélecteur restent non rattachées tant qu'une désambiguïsation occurrence par occurrence n'est pas faite (R-G0-12).

## 12. Ambiguïtés, anomalies et réemplois

**Anomalies.** Le détail est dans `RESERVES.md` :

- A-G02-01 à 07 (G0.2) : A-G02-01 est instruite par C2, A-G02-03 documentée séparément, A-G02-07 requalifiée ;
- **A-G02-08 à 14, nouvelles en G0.2bis :**
  - relaxation de la pression r_P P^- ou r_P Θ (08) ;
  - a_1, a_2 doubles dans l'annexe D (09) ;
  - trois écritures de la réduction diagonale (10) ;
  - R_b et \widehat R (11) ;
  - \mathfrak G_N et \mathcal G_N (12) ;
  - θ_∞ et θ_0(g), \mathbf s et \boldsymbol s (13) ;
  - coefficient 0,3216 et 0,3220 (14, constat de valeur numérique).

**Réemplois de glyphes à l'intérieur du volume I**, pour G0.4. Ce ne sont pas des erreurs ; ils sont documentés dans le champ `remarques` des objets concernés :

| Glyphe | Rôles relevés |
|---|---|
| q | perméabilité R1 ; facteur de saut (annexe B) ; nombre de composantes actives (annexes C–D) ; points q∈D (annexe J) ; vecteur décomposé (annexe I) |
| C | ensemble de flot ; constante b/(2a) ; épisode test (livre III) ; cellules C_k (annexe J) |
| Δ, D, \mathcal D | variété homogène ; variation ΔL ; période R2 ; délai ; ensemble de saut ; domaine (annexe J) ; diagonale interne ; délais (annexes G–H) |
| \mathcal A, \mathcal P, \mathcal L, \mathcal G, \mathcal R | attracteur ou préfixe ; protocole ou sonde ; Lyapunov ou relaxation ; regraine, graphe des voisinages ou lois ; réponse, application de retour ou ensemble atteignable (vol. II) |
| Σ, Ω, ϑ, Φ | homonymes du volume II (coupe, domaine, paramètre caché, paramétrisation) employés au volume I avec d'autres sens |
| θ, s, κ, γ, Γ, H, ι, σ | composante de trace ou horloge lente ; similarité, tanh, contenu ou variable spectrale ; coefficients de pression ou signature ; friction, variable plastique ou chemin ; état rapide ou carte de dépôt ; nœud sélectionné ou injection ; tanh ou permutation |

## 13. Différentiel avec les 95 objets de référence

**Fichier :** `G0_02bis/registry_diff.csv`, produit par `notations/scripts/registry_diff.py`.

**[CONTRÔLE]**

- Aucun identifiant de référence n'a disparu.
- 206 identifiants ont été ajoutés.
- Les 95 identifiants de référence sont modifiés, au moins par l'ajout du champ `granularite`.
- Natures de révision :
  - 206 ajouts ;
  - 16 décompositions ;
  - 5 requalifications ;
  - 5 corrections ;
  - 27 corrections de sélecteurs ;
  - 20 enrichissements ;
  - 79 évaluations de granularité.

**Changement de statut** (un seul) : `II.PRES.OPACITY_FIBRE_READOUT`, AMBIGUOUS → EXPLICIT (C2).

**Corrections de l'itération 1** (R-G0-11) :

- motifs de fichier non ancrés ;
- motif de `I.CORE.DYNAMICS_PARAMETERS`, qui citait la variante linéaire contrefactuelle (l. 280) ;
- plage de `II.KERNEL.EXTERNAL_VARIABLES` ;
- fichiers des objets compagnons ;
- site premier de la complexité c (annexe G l. 564).

## 14. Contrôles de schéma, de rattachement et de non-régression

| Contrôle | Résultat |
|---|---|
| Schéma : unicité, statuts, dépendances, relations, granularité, réciprocité famille ↔ composants, notation canonique vide | 0 erreur |
| Rattachements multiples ; sélecteurs vides | 0 ; 0 |
| Conversion JSON → YAML (C4), égalité profonde des valeurs, types et ordre | 0 écart ; rattachements de l'itération 1 identiques octet pour octet après conversion |
| Non-régression de l'inventaire G0.1 contre `05afddd` (`check_regression.py`) | 0 différence |
| Référence `reference_95/` | inchangée depuis `2588875` |
| Tests unitaires | 27 tests verts sous `.venv-g0` (16 d'extraction, 11 nouveaux sur les outils du registre) ; 23 sous Python système, 1 ignoré faute de PyYAML |
| Intégrité des sources | `git diff c74fa04 -- Volume_I Volume_II` vide |
| Dépôts connexes | non modifiés |

**[IMPOSSIBLE]** Le rôle de chaque occurrence n'a pas été vérifié individuellement : les rattachements restent lexicaux et bornés par des sélecteurs.

## 15. Échantillon de contrôle qualité

- **[CONTRÔLE]** 40 rattachements tirés au hasard (graine 20261127) parmi les 6 885 rattachements des objets G0.2bis au moment du tirage (6 896 après l'ajout des quatre derniers objets du volume II) ; fichier `G0_02bis/quality_sample.csv`.
- **Résultat :** 38 corrects, 2 recevables avec réserve :
  - \hat H_k, quotient de factorisation, rattaché à l'état de la note de transmission ;
  - \vec χ du livre III, rattaché à la mémoire lente.
- Aucun rattachement erroné.

## 16. Limites

- **[LIMITE]** Les sélecteurs restent lexicaux. Les clés ambiguës (R-G0-12) ne sont rattachées que sur des plages sûres.
- **[LIMITE]** La lecture intégrale a été faite sur un rendu compact du source : commentaires retirés, paragraphes joints. Pour les livres I et II, le début du livre III et l'annexe G, les paragraphes de plus de 380 à 420 caractères étaient tronqués ; pour les énoncés du volume II, au-delà de 1 100 caractères.
  - **[CONTRÔLE]** Le contrôle des sites de définition et des énoncés formels, qui travaille sur le source complet, a été relancé. Ses 198 passages restants sont tous classés (`definition_sites_review.csv`).
  - **[HYPOTHÈSE]** Aucune définition ne se trouve dans une fin de paragraphe tronqué sans être signalée par ce contrôle, par exemple une définition en prose sans marqueur lexical. Ce n'est pas démontré, en particulier pour les tableaux longs.
- **[LIMITE]** Les figures, planches TikZ et scripts ne sont pas inventoriés. Ils relèvent de G0.7.
- **[LIMITE]** Les relations intravolume (`relations_intra`) décrivent des liens explicités par le texte. Aucune n'établit une identité. Les homonymies notées `homonyme_a_instruire` (χ R2 et χ des annexes H–K ; s de l'annexe F et \mathbf s des annexes H–K ; mémoire \vec s du livre III) restent à instruire.

## 17. Livrables

- **Registre :** `notations/registry.yaml`, registre candidat intermédiaire, itération 2, 301 objets, YAML style bloc.
- **Outillage :**
  - `notations/requirements-g0.txt` (PyYAML 6.0.2) et `.gitignore` (environnement `.venv-g0`, non versionné) ;
  - scripts nouveaux : `registry_io.py`, `formal_environments.py`, `coverage_matrix.py`, `classify_unresolved.py`, `registry_diff.py` ;
  - `link_registry.py` étendu : sélecteurs `decoration` et `police`, contrôles de granularité ;
  - tests : `tests/test_registry_tools.py`.
- **`audits/G0/G0_02bis/` :**
  - `reading_log.csv`, `sections_*.csv`, `formal_statements_*.csv` ;
  - `coverage_matrix.csv`, `coverage_matrix_by_file.csv`, `coverage_matrix_summary.txt` ;
  - `unresolved_classification.csv`, `unresolved_manual.csv`, `definition_sites_review.csv` ;
  - `registry_diff.csv`, `quality_sample.csv`.
- **Sorties actualisées :** `audits/G0/G0_02_semantic/` (`registry_occurrences.csv`, `coverage_structuring_keys.csv`, `registry_summary.json`) ; l'état de référence est conservé dans `reference_95/`.
- **Documents :** `RESERVES.md`, `STATUS.md`, ce rapport.
- **Préservation :** les rapports antérieurs, dont `G0_02_objects_report.md` et l'inventaire G0.1, sont inchangés.

## 18. Arbitrages résiduels

- **D1 — Validation de G0.2bis et clôture de G0.2** ; autorisation de committer et de pousser.
- **D2 — A-G02-14.** Valeur du coefficient quadratique de x_res : 0,3216 ou 0,3220. Constat seulement ; à vérifier par l'auteur.
- **D3 — A-G02-03.** Faut-il instruire l'équivalence des deux définitions de l'appropriation avant G0.3, ou les garder comme deux objets jusqu'à G0.5 ?
- **D4 — Homonymies intravolume** (χ, s/\mathbf s/\vec s, θ). Les instruire en G0.3 ou les reporter à G0.4.
- **D5 — R-G0-12.** Accepter que les usages ambigus restent partiellement non rattachés (désambiguïsation occurrence par occurrence reportée à G0.4), ou exiger cette désambiguïsation avant G0.3.
- **D6 — Ouverture de G0.3.**

Arrêt avant G0.3.
