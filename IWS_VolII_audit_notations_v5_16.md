# Audit notation–rôle — Volume II V5.16

Cet audit vérifie des couples **(symbole, rôle)** et des motifs interdits. Il complète l’inventaire lexical en cherchant les recyclages contextuels.

| Symbole | Rôle attendu | Occurrences indicatives | Motifs interdits trouvés | Statut |
|---|---|---:|---:|---|
| `C` | ensemble de flot (réservé) | 181 | 0 | **OK** |
| `E` | énergie (réservé hors indices historiques déjà définis) | — | 0 | **OK** |
| `\Xi` | chambre = composante connexe d’une classe de mot | 7 | 0 | **OK** |
| `\Sigma` | coupe de fibre d’opacité | 28 | 0 | **OK** |
| `\Omega` | domaine paramétrique semi-algébrique et sous-ensembles dérivés | 25 | 0 | **OK** |
| `\Phi` | homéomorphisme de paramétrisation Ω→Σ | 11 | 0 | **OK** |
| `\vartheta` | valeur du paramètre caché dans Ω | 26 | 0 | **OK** |
| `Dep(Σ)` | support nodal de dépendance de la coupe/famille | 19 | 0 | **OK** |
| `k` | profondeur / indice des partitions | 18 | 0 | **OK** |
| `r` | rang local d’un Kairos à profondeur k fixée | 9 | 0 | **OK** |
| `u` | entrée du noyau | 22 | 0 | **OK** |
| `v` | fonction-score du lemme orbital | 1 | 0 | **OK** |
| `s_i` | norme carrée locale du bloc semi-algébrique | 1 | 0 | **OK** |
| `\mathscr F_w` | famille de polynômes déterminant les signes | 3 | 0 | **OK** |
| `Ω_w` | ensemble des paramètres réalisant le mot w | 5 | 0 | **OK** |
| `b_{i,w}, λ_{r,w}` | coefficients dépendant du mot | 8 | 0 | **OK** |
| `τ_*` | trace du déclencheur dans le bloc semi-algébrique | 9 | 0 | **OK** |

## Compléments du contrôle V5.16

- **Régularité des frontières** : `\tau_\star(\mu)` est explicitement de classe C¹ près de `\mu_*`.
- **Résolution des frontières coniques** : théorème des fonctions implicites nommé pour `(\rho,\epsilon)` et dérivée `-\ell_\pm\ne0`.
- **Rayon `R_j`** : maintien délibéré, pour éviter la quasi-collision visuelle avec la norme initiale `\rho_j`.

## Contrôles ciblés

- **Références obsolètes internes `V5.10`** : OK — aucun.
- **Réemploi de κ pour des bornes** : OK — aucun.
- **Ancienne borne de chambres régulières** : OK — aucun.
- **Ancien découpage en domaine singulier pour le comptage** : OK — aucun.
- **Ancienne constante K pour pente du cône** : OK — aucun.
- **Ancien paramètre eta du bloc conique** : OK — aucun.
- **Ancien nom T pour application conique** : OK — aucun.
- **Ancienne notation a(eta)** : OK — aucun.
- **Ancienne valeur interpolée eta critique** : OK — aucun.
- **Ancien exemple H_0(0) ambigu** : OK — aucun.
- **Ancienne formulation des contrôles secondaires** : OK — aucun.
- **Y admissible sans définition** : OK — aucun.
- **Union de partition recyclant `E`** : OK — aucun.
- **Ancien `π_0(E)`** : OK — aucun.
- **Partition indexée par `r` (`\mathcal P_r`)** : OK — aucun.
- **Partition indexée par `r` (`\mathcal P_{r...}`)** : OK — aucun.
- **Ancien `Dep(\vartheta)`** : OK — aucun.
- **Ancien indexage `b_{i,\Xi}`** : OK — aucun.
- **Ancien indexage `\lambda_{r,\Xi}`** : OK — aucun.
- **Ancien compteur `s_w`** : OK — aucun.
- **Ancien compteur `\ell_w`** : OK — aucun.
- **Réemploi `u:=\tau`** : OK — aucun.
- **Réemploi `v_i:=\tau`** : OK — aucun.
- **Ancienne convention tardive k/r** : OK — aucun.
- **Ancien conditionnement expérimental par chambre** : OK — aucun.
- **Ancien contrôle obtenu dans la chambre** : OK — aucun.
- **Ancienne récursion avec `\ell`** : OK — aucun.
- **Ancien compteur récursif `3^\ell`** : OK — aucun.
- **Phrase circulaire sur la dépendance initiale** : OK — aucun.
- **Pronom final erroné** : OK — aucun.
- **Ancienne formulation forte du support** : OK — aucun.

## Conventions stabilisées

- `k` indexe la profondeur des partitions et la longueur d’un mot ; `r` indexe un Kairos local avec `1≤r≤k`, et `r=k` au dernier Kairos du mot. Cette convention est annoncée dès l’ouverture du bloc « Murs actifs ».
- `classe de mot` est employé dans les sections expérimentales lorsque la connexité n’a pas été établie ; `chambre` / `Ξ` est réservé aux composantes connexes.
- `μ_w` était le compteur des conditions dans V5.13 ; pour V5.16, `\mathscr F_w` porte la famille de polynômes. `ℓ` reste réservé à l’indice de coordonnées ; `n` désigne la réinjection (`k=2n`).
- Le corollaire de conservation n’affirme plus la réciproque sur une réalisation arbitrairement mince. Dans les familles affines, la non-constance sur toute partie relativement ouverte non vide est obtenue par analyticité sous l’hypothèse de connexité indiquée dans le texte.

## Note sur les figures historiques

La figure de raffinement récursif `opacity_recursive_refinement.png` contient encore dans son raster les intitulés historiques « chambre(s) ». Le texte et la légende emploient désormais « classes de mot ». Cette inscription graphique devra être régénérée depuis le script source si l’on veut une homogénéité terminologique parfaite.