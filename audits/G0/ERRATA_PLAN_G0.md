# Errata du plan G0

Document de traçabilité des corrections apportées à `PLAN_G0.md` (version 2.0). Le texte du plan n'est pas réécrit : chaque passage concerné reçoit un renvoi `[Erratum E<n>]` vers ce fichier.

## E1 — Identifiants d'arbres et de commits (§ 2.3)

**Date :** 27 novembre 2026
**Origine :** constat G0.0, réserve R-G0-01 (`G0_00_manifest.md`, § 1.1)
**Validation :** auteur, décision A2 du 27 novembre 2026

**Texte d'origine.** Le § 2.3 présente comme « identifiant d'arbre » :

- `8cdf171a056203268f5dde545a65e691220409d0` (dépôt IWS) ;
- `22e14626de715b3a88783f55f89b662594ee9171` (dépôt IWS, désigné comme « arbre antérieur ») ;
- `b1a973842eae11d1dc9bed83f49a14b530e772d7` (dépôt `IWS_minimality_package`).

**Correction.** Ces trois identifiants sont des **commits** (`git cat-file -t` → `commit`) :

| Identifiant | Nature | Dépôt | Arbre Git correspondant |
|---|---|---|---|
| `8cdf171a056203268f5dde545a65e691220409d0` | commit « Reorg » | IWS | `c0253d6c357845e56d7c41265445ebe2cbfab4b0` |
| `22e14626de715b3a88783f55f89b662594ee9171` | commit « First commit » | IWS | `2800405f4cbb1d381c268d127e17929a35e8c3e5` |
| `b1a973842eae11d1dc9bed83f49a14b530e772d7` | commit, HEAD de `main` au 27/11/2026 | IWS_minimality_package | `77f2ba52f1973863ca22cd120370b4e1776001f8` |

La phrase « Il s'agit d'un identifiant d'arbre, pas d'un commit de gel » doit se lire : « Il s'agit d'un commit antérieur, non retenu comme commit de gel ». Le commit de gel est `c74fa047171ff51e308f1855d8f636add2ac33ca` (tag `g0-baseline`).

**Portée.** Purement documentaire. Aucune conséquence sur les sources ni sur les constats d'inspection : les contenus inspectés sont ceux de ces commits. Le volume I est identique entre `22e1462` et `c74fa04` (G0.0, § 1.2).
