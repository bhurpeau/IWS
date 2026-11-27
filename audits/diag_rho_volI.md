J’ai audité l’ensemble effectivement assemblé par `main.tex` dans le ZIP fourni : avant-propos/positionnement, Tomes I–III, annexes A–L et table des énoncés. Le résultat est assez net : **455 occurrences du jeton `\rho`**, qui se répartissent exhaustivement en **quatre objets mathématiques distincts**. Aucun `\varrho`, `ρ` Unicode ou `ϱ` n’apparaît dans les sources.

Le point principal est que **trois objets différents utilisent le symbole nu \(\rho\)**. Le quatrième est l’opérateur indexé \(\rho_{\mathrm{sp}}\).

## Tableau synthétique

| notation | objet désigné | type | première définition | portée | collision potentielle |
|---|---|---|---|---|---|
| \(\rho\) dans R1 | coefficient de réouverture de la perméabilité \(q\) | **paramètre scalaire positif** | première utilisation : Tome II, `IWS_PART_II.tex:889`; contrainte explicite \(\rho>0\) seulement en Annexe E, lignes 55–70 | Tome II, chap. **R1 : perméabilité dynamique** + Annexes E et F | **forte avec le \(\rho\) d'observation** ; faible avec les autres |
| \(\rho\) dans \(J(\rho)\) | valeur propre de \(\widetilde A\), donc mode du réseau | **scalaire réel / valeur propre** | Annexe C, `1844`: « Soit \(\rho\) l'une d'elles » | strictement locale à Annexe C, § **Portée pour le réseau complet** | réemploi local ; collision faible |
| \(\rho_{\mathrm{sp}}\) | rayon spectral | **fonction/opérateur scalaire sur matrices** | première apparition `1238`, définition littérale `1241` en Annexe E | Annexes E et F, analyse de Floquet de R2 | faible ; clairement distingué par `sp` |
| \(\rho\), \(\rho_1,\rho_2,\ldots\) dans le Tome III | choix de lecture / résolution d'observation | **paramètre de protocole / index de lecture**, pas une variable interne | mention anticipée `main.tex:170`; définition explicite `IWS_PART_III.tex:300–302`; formalisation Annexe G | très large : Tome III + Annexes G–L | **forte avec le \(\rho\) de R1** et surtout avec le futur \(\rho_X\) |

En nombre de jetons :

- **395** appartiennent à la famille « résolution d'observation » ;
- **48** au coefficient R1 ;
- **8** à la valeur propre modale ;
- **4** à \(\rho_{\mathrm{sp}}\).

Total : **455/455**. Il ne reste donc pas d’occurrence non classée.

---

# 1. \(\rho\) — coefficient de réouverture de R1

### Première apparition

Tome II, partie **Quand l’interface devient dynamique**, chapitre **R1 : perméabilité dynamique**, § « Équation de perméabilité », `IWS_PART_II.tex:882–895`.

Le symbole apparaît directement dans

\[
\dot q=\rho(1-q)-\eta qgw.
\]

Le texte explique immédiatement que « le premier terme rouvre progressivement l'interface ». Le sens de \(\rho\) est donc reconstructible : **\(\rho\) règle la réouverture spontanée de l'interface** lorsque le trafic disparaît.

En revanche, le corps du Tome II ne dit pas à cet endroit explicitement :

> « \(\rho\) est un paramètre scalaire strictement positif ».

Cette propriété n'est écrite littéralement qu'en Annexe E, § « R1 : perméabilité dynamique / Modèle », `IWS_ANNEXE_E.tex:50–70` :

\[
\rho>0.
\]

### Type

Il s'agit sans ambiguïté d'un **paramètre scalaire positif** :

\[
\rho\in\mathbb R_{>0}.
\]

Il n'a donc pas à proprement parler de domaine/codomaine : c'est une constante du modèle R1, non une application.

Le fait que ce soit un paramètre et non un état est confirmé plus loin par la remarque de l'Annexe E (`475`) envisageant « une variable lente modifiant durablement \(\rho\) ou \(\eta\) ».

### Occurrences

Même objet dans :

- Tome II, `IWS_PART_II.tex:889–983` — 11 occurrences ;
- Annexe E, principalement R1, `IWS_ANNEXE_E.tex:55–475`, puis rappel à `1554` — 36 occurrences ;
- Annexe F, jeu de paramètres numériques, `IWS_ANNEXE_F.tex:158` — 1 occurrence.

Les formes telles que

\[
\rho^2,\qquad
\frac{\rho}{\rho+\eta gw},\qquad
\frac{\rho}{\eta w}
\]

ne créent évidemment aucun nouvel objet : ce sont des expressions algébriques du même paramètre.

### Vérification définition/utilisation

**Définition avant usage : imparfaite.**

Le rôle est intelligible dès la première équation, mais le type et la contrainte \(\rho>0\) ne sont explicités que dans l'annexe. C'est donc exactement un cas du genre :

> le lecteur comprend probablement ce que fait \(\rho\), mais sa déclaration mathématique complète arrive après son premier emploi.

Ce n'est pas une ambiguïté sur le modèle, mais une petite dette de notation.

---

# 2. \(\rho\) — valeur propre de la matrice relationnelle

Objet totalement différent.

Il apparaît uniquement en **Annexe C — Réduction homogène et paysage autonome**, § « Portée pour le réseau complet », `IWS_ANNEXE_C.tex:1831–1895`.

Le texte établit que, pour un graphe non orienté, \(\widetilde A\) est semblable à une matrice symétrique, puis dit explicitement à `1844` :

> « Ses valeurs propres sont donc réelles. Soit \(\rho\) l'une d'elles. »

On a donc sans reconstruction :

\[
\rho\in\sigma(\widetilde A)\subseteq\mathbb R.
\]

### Type

**Scalaire réel**, servant également de **paramètre modal** après diagonalisation selon les modes propres de \(\widetilde A\).

Il intervient dans :

- \(J(\rho)\) ;
- \(\zeta\rho S_\ast\) ;
- \(\alpha\rho S_\ast\) ;
- \(\rho=1\), identifié au mode homogène ;
- \(\rho\neq1\), pour les blocs modaux transverses.

### Portée

Extrêmement locale : **8 occurrences, toutes entre les lignes 1844 et 1888 de l'Annexe C**.

Il n'est jamais réutilisé ailleurs avec ce sens.

### Vérification définition/utilisation

Ici, c'est impeccable :

- définition littérale ;
- immédiatement avant le premier \(J(\rho)\) ;
- type réel indiqué ;
- objet dont \(\rho\) est valeur propre indiqué explicitement ;
- portée locale évidente.

C'est donc un **réemploi local sans ambiguïté intrinsèque**, même s'il participe à l'encombrement global de la lettre.

---

# 3. \(\rho_{\mathrm{sp}}\) — rayon spectral

C'est un quatrième objet, qu'il ne faut surtout pas identifier au précédent simplement parce que les deux concernent un spectre.

Première apparition en Annexe E, dans la partie R2 consacrée à la monodromie :

`IWS_ANNEXE_E.tex:1235–1248`

avec d'abord

\[
\rho_{\mathrm{sp}}(\mathcal M_g)<1,
\]

puis immédiatement :

> « où \(\rho_{\mathrm{sp}}\) désigne le rayon spectral. »

Il réapparaît en Annexe F (`479`) :

\[
\mu_{\max}(g)=\rho_{\mathrm{sp}}(\mathcal M_g).
\]

### Type

C'est une **fonction/opérateur** sur les matrices carrées :

\[
M\longmapsto\rho_{\mathrm{sp}}(M)\in\mathbb R_{\ge0}.
\]

Dans l'usage effectif ici, \(M=\mathcal M_g\) est la matrice de monodromie du bloc réduit \((x,v)\).

### Définition avant utilisation

Strictement parlant : **non**.

La première formule contenant \(\rho_{\mathrm{sp}}\) précède d'une phrase sa définition textuelle. C'est cependant une définition immédiatement postposée et parfaitement standard ; le risque réel est minime.

### Relation avec le \(\rho\) modal

Ce ne sont pas le même objet :

- \(\rho\) de l'Annexe C = **une valeur propre particulière** de \(\widetilde A\) ;
- \(\rho_{\mathrm{sp}}\) = **l'opérateur qui prend le maximum des modules des valeurs propres** d'une matrice.

Ce n'est donc pas une fausse variante du même symbole.

---

# 4. \(\rho\) — lecture / résolution d'observation

C'est de très loin l'usage dominant : **395 occurrences**.

Il constitue également le cas le plus intéressant vis-à-vis de ton futur Volume II.

## Définition dans le corps du Tome III

`IWS_PART_III.tex:275–313`, § **Ce qu'une sonde permet de lire**.

La définition littérale est à `300–302` :

> « On note \(\rho\) le choix de ce qui est ainsi retenu. Dans la suite, \(\rho\) désignera donc une *lecture*, ou de manière équivalente une résolution d'observation. »

et :

> « Le symbole \(\rho\) ne décrit pas une variable interne du système. Il appartient au protocole utilisé pour l'interroger. »

Puis :

\[
\mathcal R_X^\rho(\mathcal H)
\]

et le schéma

\[
\operatorname{Exec}_{\mathcal H}(X)
\xrightarrow{\rho}
\mathcal R_X^\rho(\mathcal H).
\]

## Son type exact est plus subtil

Le corps du texte donne presque l'impression que

\[
\rho:\operatorname{Exec}\to\text{réponse}
\]

est lui-même une application.

Mais **l'Annexe G affine cette formulation**.

Elle dit (`IWS_ANNEXE_G.tex:220` et suivants) :

> « Une résolution \(\rho\) associe à une exécution une observation dans un espace \(\mathcal Y_\rho\). »

Puis elle distingue les applications effectives.

Pour une lecture terminale :

\[
\tau_\rho:\mathfrak X\longrightarrow\mathcal Y_\rho.
\]

Pour une lecture de chemin :

\[
\omega_\rho:\operatorname{Exec}\longrightarrow\mathcal Y_\rho.
\]

Donc, formellement, **\(\rho\) n'a pas un domaine et un codomaine uniques définis dans le manuscrit**. Le meilleur typage fidèle au texte est :

> \(\rho\) est un **choix de résolution/lecture appartenant au protocole**, qui indexe un espace de réponses \(\mathcal Y_\rho\) et une application de lecture appropriée (\(\tau_\rho\), \(\omega_\rho\), etc.).

C'est important : **\(\rho\) est plutôt un paramètre de lecture qu'une application unique**.

Le schéma `Exec \xrightarrow{\rho} R` du corps est donc une notation conceptuelle légèrement plus lâche que la formalisation de l'Annexe G.

---

## Toutes les variantes appartiennent bien au même objet

Les formes suivantes ne constituent pas de nouveaux \(\rho\).

### Résolution et raffinement

\[
\rho,\qquad
\rho_1,\rho_2,\rho_3,\qquad
\rho_1\preceq\rho_2.
\]

L'Annexe G définit explicitement \(\rho_2\) comme un **raffinement** de \(\rho_1\) lorsque la lecture grossière est obtenue par projection de la lecture fine :

\[
\pi_{21}:\mathcal Y_{\rho_2}\to\mathcal Y_{\rho_1}.
\]

Les indices \(1,2,3\) désignent donc différentes résolutions du **même genre d'objet**.

### Espace et applications de lecture

Même famille :

\[
\mathcal Y_\rho,\qquad
\tau_\rho,\qquad
\omega_\rho,\qquad
\omega_\rho^{\mathrm{fin}}.
\]

### Réponse et équivalence

Même \(\rho\) encore dans :

\[
\mathcal R_X^\rho(\mathcal H),
\qquad
X\sim_{\mathfrak B,\rho}Y,
\qquad
X\not\sim_{\mathfrak B,\rho}Y,
\qquad
[X]_{\mathfrak B,\rho}.
\]

### Accessibilité et géométrie de réponse

Dans le Tome III :

\[
\operatorname{Acc}_{\mathfrak B,\rho}(X),
\]

défini par l'équation étiquetée `eq:t3-accessibilite`, et

\[
\mathcal G_{\Omega,\rho}(X).
\]

Là encore, \(\rho\) ne change pas de sens : ces objets sont **relatifs à la résolution choisie**.

### Cartes de réponse des annexes H–K

Toujours la même résolution :

\[
\Omega_{\mathcal P,\rho},
\qquad
\widehat\Omega_{\mathcal P,\rho},
\qquad
\widehat\Omega_\rho,
\]

ainsi que les ensembles et frontières dérivés :

\[
A_{\mathcal P,\rho},
\qquad
\Sigma_{\mathcal P,\rho},
\qquad
\partial A_{\mathcal P,\rho}^{\mathrm{ext}},
\qquad
\Sigma_{\mathcal P,\rho}^{\gamma},
\]

etc.

L'Annexe H est particulièrement explicite : elle déclare d'abord le couple d'observation \((\mathfrak B,\rho)\), puis construit

\[
\Omega_{\mathcal P,\rho}:\mathcal S\to\mathcal Y_\rho.
\]

C'est donc une **fausse collision interne** : la multiplication des formes contenant `rho` reflète le même paramètre d'observation, pas une prolifération d'objets \(\rho\).

### Séparabilité

Toujours la même résolution dans :

\[
\operatorname{Sep}_{\mathfrak B,\rho},
\qquad
\ell_{c,\mathfrak B,\rho},
\qquad
d_{c,\mathfrak B,\rho}.
\]

L'Annexe L le rappelle même dans sa table des notations :

> \(\rho\) — résolution de lecture.

---

# Deux petites anomalies à l'intérieur de cette famille

Elles ne constituent **pas de nouveaux \(\rho\)**, mais elles méritent l'étiquette « à vérifier ».

### `d_\rho` — Annexe I

À `IWS_ANNEXE_I.tex:497`, on trouve :

\[
d_\rho(\ldots,\ldots)\le\cdots
\]

dans le paragraphe « Extinction approchée ».

Je ne trouve **aucune définition de \(d_\rho\)** ailleurs dans les sources.

Le contexte permet fortement de penser qu'il s'agit d'une distance adaptée à l'espace d'observation \(\mathcal Y_\rho\), puisque le texte évoque immédiatement ensuite la « distance discrète » pour une lecture binaire.

Mais le manuscrit ne le dit pas.

Donc :

> **\(d_\rho\) : ambigu / à vérifier.**

Le sens de \(\rho\) reste identifiable ; c'est l'objet \(d_\rho\) qui n'est pas défini.

### \(\mathcal R^{\mathfrak B,\rho}\) — Annexe K

`IWS_ANNEXE_K.tex:101` et `348`.

Cette notation apparaît deux fois, alors que la notation canonique est normalement

\[
\mathcal R_X^\rho(\mathcal H)
\]

avec \(\mathfrak B\) comme domaine de sondes.

Le lecteur comprend très probablement « la réponse considérée relativement au protocole \((\mathfrak B,\rho)\) », mais **\(\mathcal R^{\mathfrak B,\rho}\) n'est jamais formellement définie comme objet autonome**.

Là encore :

> pas un nouveau \(\rho\), mais une notation composite implicite.

---

# 5. Chronologie réelle des changements de sens

C'est ici que le problème apparaît le plus nettement.

Dans l'ordre de lecture du volume assemblé :

1. **Positionnement bibliographique**, `main.tex:170`  
   \(\rho\) = résolution de lecture.

2. **Tome I**  
   **aucun \(\rho\)**.

3. **Tome II — R1**  
   \(\rho\) = coefficient scalaire de réouverture.

4. **Tome III**  
   \(\rho\) = résolution de lecture, explicitement redéfinie.

5. **Annexe C**  
   \(\rho\) = valeur propre de \(\widetilde A\).

6. **Annexe E**  
   \(\rho\) = de nouveau coefficient R1 ;  
   puis \(\rho_{\mathrm{sp}}\) = rayon spectral.

7. **Annexe F**  
   mêmes deux usages que l'Annexe E.

8. **Annexes G–L**  
   \(\rho\) = de nouveau résolution d'observation.

C'est donc moins une dérive progressive qu'un véritable **va-et-vient sémantique** :

\[
\text{observation}
\to
\text{R1}
\to
\text{observation}
\to
\text{valeur propre}
\to
\text{R1}
\to
\text{observation}.
\]

Aucun passage ne prévient explicitement :

> « attention, la lettre \(\rho\) est réutilisée ici avec un autre sens ».

---

# 6. Carte des collisions internes

| paire | diagnostic |
|---|---|
| R1 \(\rho\) ↔ observation \(\rho\) | **collision directe forte** |
| R1 \(\rho\) ↔ valeur propre \(\rho\) | **réemploi local / collision faible** |
| observation \(\rho\) ↔ valeur propre \(\rho\) | **collision faible**, car l'usage spectral est extrêmement local et explicitement introduit |
| R1 \(\rho\) ↔ \(\rho_{\mathrm{sp}}\) | **collision faible**, mais ils coexistent dans l'Annexe E |
| valeur propre \(\rho\) ↔ \(\rho_{\mathrm{sp}}\) | **collision faible** ; proximité sémantique « spectrale », mais objets différents |
| observation \(\rho\) ↔ \(\rho_{\mathrm{sp}}\) | **bénigne** |
| \(\rho,\rho_1,\rho_2,\rho_3,\mathcal Y_\rho,\omega_\rho,\dots\) du Tome III | **fausses collisions : même objet de résolution** |

La seule collision que je qualifierais réellement de **structurelle dans le Volume I actuel** est donc :

> **le \(\rho\) scalaire de R1 versus le \(\rho\) de résolution d'observation.**

Les deux ont une portée large, tous deux sont utilisés sans indice, et ils appartiennent à deux tomes consécutifs. Ce n'est pas seulement une variable locale recyclée dans une preuve.

---

# 7. Comparaison avec le \(\rho_X\) du futur Volume II

Le \(\rho_X\) que tu donnes,

\[
\rho_X=(\pi_s,\rho_{\mathrm{int}})
:
\mathcal X\to\mathcal S\times Y_{\mathrm{int}},
\]

est **un cinquième objet**, extérieur au Volume I audité.

Rien dans le Volume I ne permet de l'identifier à l'un des quatre précédents.

En particulier, les fibres

\[
F_y=\rho_X^{-1}(y)\cap C
\]

montrent sans ambiguïté que \(\rho_X\) est une **application définie sur l'espace d'états \(\mathcal X\)**, dont on prend des images réciproques.

Ce n'est pas ce que fait le \(\rho\) du Tome III actuel.

Le \(\rho\) du Tome III :

- choisit une résolution d'observation ;
- indexe \(\mathcal Y_\rho\) ;
- détermine des lectures \(\tau_\rho\) ou \(\omega_\rho\).

Le futur \(\rho_X\) :

- est lui-même une application ;
- part de \(\mathcal X\) ;
- possède les composantes \(\pi_s\) et \(\rho_{\mathrm{int}}\) ;
- produit des fibres par image réciproque.

### Et pourtant, c'est probablement la collision future la plus gênante

Non parce que les objets seraient proches mathématiquement, mais parce qu'ils sont **proches lexicalement et conceptuellement** : les deux parlent de « lecture » de ce qui est accessible.

Le Tome III actuel aggrave légèrement cette proximité avec :

\[
\operatorname{Exec}_{\mathcal H}(X)
\xrightarrow{\rho}
\mathcal R_X^\rho(\mathcal H),
\]

qui donne visuellement à \(\rho\) l'allure d'une application, alors que l'Annexe G réserve finalement ce rôle formel à \(\tau_\rho\) ou \(\omega_\rho\).

Un lecteur passant au futur Volume II pourrait donc raisonnablement se demander :

> « \(\rho_X\) est-il la version sur l'état du \(\rho\) d'observation du Volume I ? »

La réponse de l'audit est **non** — mais la notation l'incite à poser la question.

Je classerais donc :

- futur \(\rho_X\) ↔ résolution \(\rho\) du Volume I : **collision potentielle forte** ;
- futur \(\rho_X\) ↔ R1 \(\rho\) : **collision typographique moyenne**, mais objets très éloignés ;
- futur \(\rho_X\) ↔ valeur propre \(\rho\) : **faible** ;
- futur \(\rho_{\mathrm{int}}\) ↔ \(\rho_{\mathrm{sp}}\) : **bénigne typographiquement**, indices suffisamment explicites.

---

# Carte compacte des différents visages de \(\rho\)

En utilisant des étiquettes uniquement pour cet audit :

\[
\boxed{\text{4 objets distincts dans le Volume I}}
\]

**A — \(\rho\) de R1**  
scalaire positif ; taux/coefficient de réouverture de la perméabilité ; Tome II + E/F.

**B — \(\rho\) modal**  
valeur propre réelle de \(\widetilde A\) ; paramètre de \(J(\rho)\) ; uniquement Annexe C.

**C — \(\rho_{\mathrm{sp}}\)**  
opérateur rayon spectral ; Annexes E/F.

**D — \(\rho\) d'observation**  
résolution/lecture du protocole ; Tome III + G–L ; engendre toutes les formes
\(\mathcal Y_\rho,\tau_\rho,\omega_\rho,\mathcal R^\rho,
\sim_{\mathfrak B,\rho},\Omega_{\mathcal P,\rho},
\operatorname{Acc}_{\mathfrak B,\rho},
\ell_{c,\mathfrak B,\rho},\ldots\).

**À vérifier dans D :** \(d_\rho\) n'est jamais défini ; \(\mathcal R^{\mathfrak B,\rho}\) est employé sans définition autonome.

**Collision forte actuelle :** A ↔ D.

**Réemplois locaux acceptables :** B.

**Index suffisamment discriminant :** C.

**Collision future la plus sensible :** D ↔ futur \(\rho_X\), précisément parce que les deux objets sont différents tout en appartenant au même champ sémantique de la « lecture ».

Donc, pour répondre à la question centrale : **il y a réellement quatre \(\rho\) différents dans le Volume I, dont trois vivent sous le symbole nu \(\rho\)**. Je ne compterais ni \(\rho_1,\rho_2\), ni \(\rho^2\), ni les dizaines de \(\mathcal R^\rho,\Omega_{\bullet,\rho},\Sigma_{\bullet,\rho}\) comme des objets supplémentaires.

:chatgpt-content-reference{index="0"}[ZIP source audité](sandbox:/mnt/data/IWS_Volume_I__FR_.zip)