# D2 — Coefficients de la branche résistante : recalcul indépendant

**Date :** 28 novembre 2026. **Nature :** correction **numérique et scientifique**, distincte des corrections notationnelles (G0.4–G0.5). **Aucun manuscrit modifié.**

## 1. Recalcul

Script : `D2_resistant_branch_check.py` (Python standard, lecture seule) ; sortie : `D2_resistant_branch_check_output.txt`.

Paramètres : ζ = 0,8 ; λ = 2 ; α = 0,45 ; β = 0,12 (annexe F l. 132) ; w = 0,98006 (annexe D l. 50).

| Quantité | Formule (annexe D) | Valeur recalculée |
|---|---|---|
| r_c = τ_ign | √((1−ζ)/(ζ(1+λ)−1)) | 0,377964473009227 |
| m₁ = m′(r_c) | −2λr_c/[1+(1+λ)r_c²]² (l. 407) | −0,740810367098085 |
| m₂ = m″(r_c) | −2λ[1−3(1+λ)r_c²]/[1+(1+λ)r_c²]³ (l. 426) | 0,392 |
| A, B | √2α/β, √2w/β (l. 455) | 5,303300858899108 ; 11,550117866161465 |
| c₁ | −B/A = −w/α (l. 726) | −2,177911111111111 |
| c₂ (formule complète, l. 746) | −(a_xx c₁² + a_xg c₁ + a_gg)/a₂ | 0,321955402067028 |
| c₂ (forme simplifiée) | −ζc₁²/(3m₁A) | 0,321955402067028 |

Le recalcul reproduit exactement les valeurs transmises (D2). À quatre décimales : **c₁ = −2,1779 ; c₂ = 0,3220.**

**[CONTRÔLE]** Résolution directe de G(x, g_c+δ) = 0 par Newton : l'écart au développement c₁δ + c₂δ² décroît comme δ³ (rapport stable ≈ −3,53 pour δ de 10⁻² à 10⁻³), ce qui confirme c₁ et c₂.

## 2. Occurrences des valeurs anciennes et dépendances

Le recensement complet est dans `D2_occurrences.csv`.

- **Coefficient linéaire −2,1774** :
  - livre II, l. 482 ;
  - annexe D, l. 809 (incohérent avec −2,17791 à la l. 612 de la même annexe) ;
  - annexe F, l. 319.
- **Coefficient quadratique 0,3216** : livre II, l. 484 (A-G02-14). Les annexes D (l. 798, 811, 2017) et F (l. 321) donnent 0,3220, ce qui est correct.
- **Résultat numérique dépendant** : la ligne 3g_c du tableau de l'annexe F (l. 330) donne « développement : −0,1411 ».
  - Avec c₁ recalculé, on obtient −0,14116, soit **−0,1412**.
  - La ligne 2g_c (−0,0709) est inchangée.
  - Les racines numériques (−0,0710 ; −0,1421) ne dépendent pas des coefficients ; le recalcul donne −0,071047 et −0,14213.
- **Contributions au numérateur** (annexe D, l. 785) : le texte donne 27,40 ; −52,31 ; 26,15, le recalcul 27,41 ; −52,29 ; 26,15. L'écart d'arrondi est à examiner.
- **Figures** : aucune figure ni aucun script de figure du corpus ne dépend de ces coefficients. Les correspondances lexicales trouvées dans les planches TikZ sont des coordonnées, donc de faux positifs.
- **Hors périmètre, en lecture seule** :
  - copies `iws-lean/tex/IWS_ANNEXE_D.tex` et `IWS_ANNEXE_F.tex` (même −2,1774) ;
  - `IWS_1/fii1_addendum.py` et `NOTE_FII1_INTERFACE.md`, qui portent −2,1774 ; 0,3216 et « 27,40 − 52,31 + 26,14 ». C'est la provenance historique probable des valeurs anciennes.
  - **[HYPOTHÈSE non vérifiée]** Les valeurs anciennes ne s'expliquent pas par w = 0,98, qui donne c₁ = −2,17778 et c₂ = 0,32192. Leur origine (ajustement numérique, version antérieure) n'est pas reconstruite.

## 3. Annulation exacte des contributions en m₂

Les termes en m₂ du numérateur de c₂ s'écrivent :

  m₂(A²c₁²/2 + ABc₁ + B²/2) = (m₂/2)(Ac₁ + B)².

Or c₁ = −B/A, donc Ac₁ + B = 0. **La contribution de m₂ est nulle exactement**, et non numériquement : le recalcul donne 0 à l'arrondi machine près. Il reste seulement le terme ζ/3 de a_xx :

  c₂ = −(ζ/3)c₁²/a₂ = −ζc₁²/(3m₁A) > 0 (car m₁ < 0).

Les « trois contributions » de l'annexe D (27,41 − 52,29 + 26,15 ≈ 1,2649 = ζc₁²/3) ne « s'annulent » donc pas « presque » par accident numérique : leur partie en m₂ s'annule identiquement.

Les énoncés qualitatifs à reformuler ultérieurement sont :

- annexe D, l. 793 (« Elles s'annulent presque ») et l. 819 ;
- livre II, l. 488–490 (« L'origine générale de cette compensation n'est pas encore établie ») ;
- annexe F, l. 337.

La formalisation Lean de l'annexe D établit les mêmes relations : README de `iws-lean`, l. 230, `A c₁ + B = 0` et forme close de c₂. Cela a été constaté en lecture seule ; rien n'a été reconstruit.

## 4. Classement

Ces points sont des corrections numériques et scientifiques, inscrites dans `RESERVES.md` (A-G02-14 élargie, A-G02-15). Elles sont à traiter dans la phase de correction des manuscrits, non en G0.4–G0.5, qui ne portent que sur la notation.
