# IWS — Volume II, V5.17 (consolidation)

**Source de départ :** `IWS_volume_II_classe_objets_transformations_v5_16.tex`.

## Modifications apportées

1. **Résumé :** mention de la preuve conditionnelle de transmission \(C^2\) à profondeur finie et de la certification de huit événements du protocole `kept1`, avec les réserves de reproduction.
2. **Section « Exploration à profondeur finie des fibres d'opacité » :** nouvelle sous-section « Transmission régulière à profondeur finie et certification des huit premiers Kairos ». Elle contient le cadre et les hypothèses, un tableau compact des huit événements, et un corollaire conditionnel sur le voisinage \(C^2\) de \(q_0=(0,0)\).
3. **Section « Portée pour la question de tameness » :** rappel explicite que la régularité locale \(C^2\) ne donne pas une propriété globale de définissabilité, de stratification ou de complexité.
4. **Section « État de travail actuel » :** actualisation des acquis, sans modifier le candidat constitutif C0, C1, \(C23^{\mathrm{pot}}\), C4 ni les questions C5 et \(G_2\).

## Statut et limites

- La transmission \(C^2\) est un **théorème conditionnel** de la note compagnon.
- La vérification de (H1)–(H5) pour huit épisodes de `kept1` en \(q_0\) est **assistée par ordinateur** ; les événements et les non-annulations aux rangs 2–8 sont reproduits par deux méthodes.
- Les **quotients de factorisation de (H2) au rang 1** ne sont certifiés que par la méthode 1 ; il serait incorrect de dire qu'ils ont été reproduits par la méthode 2.
- La validité des enclosures et du code demeure une condition de la conclusion ; **pas de relecture par un tiers**.
- Ni rayon explicite du voisinage, ni borne uniforme en profondeur, ni « tameness » globale.

## Notes de référence (fournies dans le sous-dossier `preuves_compagnons` du ZIP)

- `transmission_profondeur_finie_V2.tex`
- `certification_huit_episodes_V2.tex`
- `audit_cauchy_lemme_V2.md`

Aucun nouveau calcul n'a été exécuté lors de cette consolidation : les chiffres du tableau et le statut proviennent des notes et sorties déjà fournies.
