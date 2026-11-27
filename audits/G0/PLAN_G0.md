# G0 — Harmonisation notationnelle et sémantique d’IWS

**Version du plan :** 2.0 — 27 novembre 2026  
**Statut :** programme de travail proposé ; primauté notationnelle du volume II validée.  
**Destination :** `audits/G0/PLAN_G0.md` dans `bhurpeau/IWS`.

## 1. Finalité et périmètre

Établir un référentiel commun des objets mathématiques, de leurs notations, de leurs types et de leurs relations entre les volumes I et II, puis préparer le raccord avec Lean avant la formalisation de G et des annexes suivantes.

G0 ne constitue ni une nouvelle théorie ni une révision générale des démonstrations. Il doit préserver l'identité des objets, les hypothèses, les conclusions et les statuts scientifiques des résultats. Les anomalies mathématiques découvertes sont consignées séparément ; seules celles qui empêchent une identification ou une utilisation non ambiguë dans le périmètre de G0 doivent être arbitrées avant clôture.

### 1.1. Règle normative

Les conventions notationnelles stabilisées du **volume II V5.17** priment. Le volume I s'adapte à ce référentiel. Cette primauté est notationnelle, non mathématique : une généralisation ne transforme pas rétroactivement un objet particulier en objet général.

| Situation | Règle |
|---|---|
| Même objet, symboles différents | Retenir la notation du volume II |
| Objets distincts, collision avec une notation réservée du volume II | Adapter le volume I dans la portée de réservation |
| Généralisation, restriction ou projection | Préserver les différences de type et expliciter la relation ; harmoniser la famille de symboles si pertinent |
| Objet propre au volume I | Conserver son symbole s'il est compatible avec le référentiel |
| Variable liée, indice ou notation strictement locale | Conserver si aucune règle de réservation applicable ni ambiguïté |
| Notation ambiguë dans le volume II lui-même | Ouvrir une décision explicite ; ne pas propager l'ambiguïté |
| Identifiant Lean existant | Conserver par défaut ; documenter le raccord |

Toute dérogation est motivée, sourcée et validée. La stabilité des annexes A, C et D constitue une contrainte de conservation mathématique, pas une priorité notationnelle concurrente.

### 1.2. Interdictions pendant G0

- Pas de remplacement global aveugle d'un symbole.
- Pas d'identification d'objets sur la seule base de leur notation ou d'un nom similaire.
- Pas de modification silencieuse des définitions, hypothèses, quantificateurs, conclusions ou statuts des résultats.
- Pas de renommage massif des identifiants Lean ni de modification de preuve sans autorisation distincte.
- Pas de nouvelle démonstration, certification numérique, formalisation de B ou G, généralisation du noyau, ni développement du volume III dans ce chantier.
- Pas de modification des audits historiques : produire des compléments versionnés.

## 2. Sources et état initial

### 2.1. Dépôts

| Dépôt | Rôle dans G0 |
|---|---|
| [IWS](https://github.com/bhurpeau/IWS) | Autorité documentaire et notationnelle ; sources à auditer et corriger |
| [iws-lean](https://github.com/bhurpeau/iws-lean) | Consultation des définitions et énoncés formalisés ; raccord documentaire |
| [IWS_minimality_package](https://github.com/bhurpeau/IWS_minimality_package) | Provenance des figures, scripts, notes et certificats numériques du volume II |
| [IWS_1](https://github.com/bhurpeau/IWS_1) | Dépôt de l'article minimal ; référence historique, hors corrections G0 par défaut |

### 2.2. Sources principales

Volume I : `Volume_I/main.tex`, ses trois livres `IWS_PART_I.tex` à `IWS_PART_III.tex`, les douze annexes `Annexes/IWS_ANNEXE_A.tex` à `IWS_ANNEXE_L.tex`, `TABLE_ENONCES.tex`, la bibliographie et les figures effectivement référencées.

Volume II : `Volume_II/IWS_volume_II_classe_objets_transformations_v5_17.tex`, seule source maîtresse retenue. L'ancienne source redondante a été supprimée du dépôt. Consulter `NOTES_V5_17.md` et `preuves_compagnons/` pour comprendre les résultats et leurs statuts ; ne pas les compter comme parties du manuscrit principal. Les notes compagnons sont des documents actifs associés, à contrôler séparément pour les collisions pertinentes ; les archives expérimentales ne sont pas réécrites.

Audits historiques : `audits/diag_rho_volI.md` et `audits/IWS_VolII_audit_notations_v5_16.md`.

### 2.3. Constats déjà établis

- L'arbre Git `8cdf171a056203268f5dde545a65e691220409d0` du dépôt principal a été inspecté. Il contient les deux volumes, le README et les répertoires `audits/` et `notations/`. Il s'agit d'un identifiant d'arbre, pas d'un commit de gel.
- Les fichiers inclus par le document maître du volume I étaient tous présents lors de la vérification précédente. Les 455 occurrences du jeton `\rho` ont été recomptées sur l'arbre antérieur `22e14626de715b3a88783f55f89b662594ee9171`, avec concordance des décomptes par fichier. Cela ne certifie pas l'identité sémantique de chaque occurrence ni l'absence de changements ultérieurs.
- L'audit V5.16 est plus récent que V5.12 ; il doit être réconcilié avec V5.17 et non appliqué aveuglément. En particulier, `\mathscr F_w` désigne la famille de polynômes, alors que les anciennes conventions mentionnaient le compteur `\mu_w`.
- Le README Lean rapportait 905 théorèmes audités et l'achèvement du périmètre analytique formalisé de A, C et D au 26 novembre 2026. Le commit, le périmètre exact et le bilan doivent être vérifiés au gel ; aucune certification des résultats numériques n'est présumée.
- Le dépôt expérimental a été inspecté sur l'arbre `b1a973842eae11d1dc9bed83f49a14b530e772d7` (identifiant d'arbre). Trois générateurs de figures d'opacité ont été identifiés par leurs sorties. La reproductibilité n'a pas été testée.
- Les compilations LaTeX n'ont pas été exécutées. Le PDF V5.17 et la source redondante ne figurent plus dans l'arbre actuel inspecté. Le README contient encore des liens et mentions à actualiser.

## 3. Organisation des livrables

```text
IWS/
├── README.md
├── Volume_I/
├── Volume_II/
├── audits/
│   ├── diag_rho_volI.md
│   ├── IWS_VolII_audit_notations_v5_16.md
│   └── G0/
│       ├── PLAN_G0.md
│       ├── STATUS.md
│       ├── G0_00_manifest.md
│       ├── G0_01_inventory/
│       ├── G0_02_objects_report.md
│       ├── G0_03_crosswalk_report.md
│       ├── G0_04_collision_report.md
│       ├── G0_05_arbitration_report.md
│       ├── G0_07_changes.md
│       ├── G0_08_lean_report.md
│       ├── G0_09_closure_report.md
│       └── RESERVES.md
└── notations/
    ├── README.md
    ├── registry.yaml
    ├── conventions.yaml
    ├── decisions.yaml
    ├── crosswalk.csv
    ├── lean_crosswalk.csv
    ├── forbidden_patterns.yaml
    ├── NOTATIONS.md
    └── scripts/
```

Arborescence cible, à créer progressivement. `audits/` décrit les constats et les contrôles ; `notations/` contient les données structurées et les décisions normatives validées. Les propositions non validées portent explicitement un statut provisoire. `NOTATIONS.md` est généré depuis le registre, jamais maintenu comme une deuxième source de vérité. Le README racine renvoie vers le plan et le statut courant sans recopier le détail du chantier.

## 4. G0.0 — Gel des sources et préparation

**But :** disposer d'une base reproductible, sans modifier le contenu mathématique.

1. Actualiser le README : liens `audits/`, suppression de la mention de la source redondante et du lien PDF absent, mise à jour de l'arborescence ; lien vers ce plan et `notations/`.
2. Résoudre et noter les SHA de commits réels des trois dépôts, leurs branches, tags éventuels et dates. Distinguer commit et arbre Git. Figer le dépôt principal sur un commit de référence et créer une branche de travail dédiée, par exemple `harmonisation/g0`.
3. Construire le manifeste récursif des inclusions LaTeX ; relever macros, bibliographies, figures, notes compagnons, fichiers générés et exclusions. Enregistrer les empreintes des sources actives. Séparer manuscrits, compagnons, illustrations et archives.
4. Compiler chaque volume depuis son répertoire avec l'outil approprié au préambule (tester `latexmk -pdf` si compatible). Noter moteur, versions, commandes, logs, erreurs et avertissements préexistants. Conserver PDF de référence et inventaire des labels/énoncés dans un emplacement reproductible, sans imposer le stockage des binaires dans Git.
5. Vérifier la provenance des figures en parallèle, sans en faire un préalable au diagnostic lexical. Relever les résultats Lean de référence, les versions de dépendances et les tags pertinents sans modifier le dépôt Lean.
6. Initialiser `STATUS.md` : phase, commit de base, tâches validées, anomalies, décisions en attente, prochaine action.

**Livrable :** `G0_00_manifest.md` et pièces de contrôle référencées.

**Porte de validation :** sources actives identifiées, source canonique unique, commits figés, état initial documenté. Une compilation impossible n'interdit pas l'inventaire en lecture seule si le blocage est explicite ; elle interdit de prétendre à une validation finale des corrections tant que non résolue.

## 5. G0.1 — Inventaire lexical

**But :** établir la couverture du corpus sans encore choisir de symboles.

Extraire les expressions mathématiques des deux volumes et les macros pertinentes, en distinguant texte, math inline, équations, environnements, commentaires, définitions de macros et usages. Préserver les indices/exposants significatifs, variantes typographiques, opérateurs et expressions composites ; ne pas confondre `\rho`, `\rho_X`, `\rho_{\mathrm{sp}}` ni compter un préfixe de commande comme un symbole. Conserver la forme source et, lorsque possible, la forme après expansion contrôlée. Signaler les constructions que le parseur ne sait pas traiter ; effectuer des contrôles manuels ciblés.

Chaque occurrence comporte : volume, fichier, ligne/plage, label stable, section, expression, symbole source, famille lexicale, contexte, statut d'extraction. Les labels et empreintes facilitent le suivi lorsque les numéros de ligne évoluent.

Réutiliser l'audit des 455 `\rho` après vérification sur le commit gelé ; comparer les écarts. Actualiser les motifs V5.16 sur V5.17, notamment les ajouts liés à la transmission C² et aux huit Kairos. Contrôler séparément les preuves compagnons et les labels de figures, sans mélanger leurs statistiques à celles des manuscrits.

**Livrables :** `G0_01_inventory/occurrences_volI.csv`, `occurrences_volII.csv`, `symbol_families.csv`, `extraction_report.md` et inventaire des exclusions. Outil reproductible dans `notations/scripts/`, testé sur des exemples réels.

**Porte :** couverture documentée de toutes les sources actives, occurrences traçables, limites du parseur recensées ; aucun renommage.

## 6. G0.2 — Inventaire sémantique

**But :** passer des symboles aux objets mathématiques.

Pour chaque objet structurant, attribuer un identifiant stable indépendant du glyphe. Exemples provisoires : `IWS.OBS.RESOLUTION`, `IWS.OPACITY.STATE_OBSERVATION`, `IWS.CORE.FLOW_SET`, `IWS.R1.REOPENING_RATE`. Ne pas créer un identifiant global pour chaque variable muette.

Le registre contient au minimum : identifiant, nom, nature, type, domaine/codomaine si applicable, définition de référence (volume, fichier, label/plage et commit), notations observées avec leurs portées, hypothèses, dépendances, statut de définition, statut de validation et notation canonique (vide si non arbitrée).

Distinguer définitions explicites, usages implicites, objets dérivés, paramètres, indices, fonctions, relations et familles. Un même symbole peut désigner plusieurs objets ; un même objet peut porter plusieurs symboles. Ne pas déduire de structure topologique, de domaine ou de codomaine non établis. Par exemple, distinguer chambre (composante connexe) et classe de mot.

Priorité de lecture : volume II canonique d'abord ; noyau du volume I ensuite ; interfaces entre volumes (livre III et G–L) ; autres annexes et variables locales. Construire des candidats de correspondance au fil de la lecture, sans les valider avant G0.3.

**Livrables :** `notations/registry.yaml` (provisoire), `G0_02_objects_report.md`, anomalies dans `RESERVES.md`.

**Porte :** objets structurants identifiés, typés et sourcés ; ambiguïtés explicitement marquées.

## 7. G0.3 — Correspondance intervolumes

**But :** construire la table qui manque actuellement.

Comparer les définitions, signatures, hypothèses, niveaux d'abstraction et rôles. Les relations sont orientées du volume I vers le volume II. Admettre plusieurs relations et des correspondances un-à-plusieurs ou plusieurs-à-un.

| Code | Sens de la relation I → II |
|---|---|
| ID | Même objet dans le cadre indiqué |
| GEN | L'objet II généralise I |
| SPEC | L'objet II spécialise I |
| PROJ | L'objet II est obtenu par projection/restriction de I ; préciser l'application |
| DER | L'objet II est dérivé de I ; préciser la construction |
| ANA | Analogie sans identification établie |
| DIST | Objets distincts |
| UNK | Relation non déterminée |
| NEW | Objet propre à un volume ; indiquer lequel |

Une identité ou correspondance conditionnelle doit expliciter ses hypothèses et, si nécessaire, l'isomorphisme ou le changement de représentation. Une notation commune ne constitue pas une preuve. Ne pas inventer une correspondance pour remplir une case.

Exemple à instruire : résolution d'observation du volume I versus `\rho_X` et `\rho_{\mathrm{int}}` du volume II. La proximité conceptuelle ne suffit pas à les identifier. Vérifier également les espaces d'états, exécutions, réponses, historiques, projections, structures, équivalences et fibres.

**Livrables :** `notations/crosswalk.csv` (ID I, ID II, relation, conditions, justification, sources, statut), `G0_03_crosswalk_report.md`.

**Porte :** chaque objet structurant est examiné, avec relation justifiée ou absence de correspondance explicitée ; les inconnues ne sont pas masquées.

## 8. G0.4 — Diagnostic des collisions

**But :** hiérarchiser les problèmes réels, non maximiser les renommages.

| Niveau | Diagnostic | Traitement |
|---|---|---|
| N0 | Réemploi local légitime | Conserver |
| N1 | Collision graphique sans ambiguïté de rôle | Documenter ou conserver |
| N2 | Collision sémantique dans une portée significative | Arbitrer |
| N3 | Collision critique entre objets proches ou notation réservée | Corriger prioritairement |
| N4 | Ambiguïté mathématique, définition absente ou types incompatibles | Clarifier ou isoler avec décision explicite |

Familles candidates : `\rho`, `\Sigma`, `\Omega`, `\Phi`, `\vartheta`, `k`, `r`, `C`, `E`, `u`, `v`, `\pi`, les espaces et applications de lecture. Liste non exhaustive, niveaux non présupposés. Examiner aussi les quasi-collisions visuelles, comme rayon et norme initiale. Les anomalies `d_\rho` et `\mathcal R^{\mathfrak B,\rho}` signalées par l'ancien audit doivent être vérifiées dans les sources courantes avant toute décision.

Pour chaque collision : identifiants d'objets, occurrences/portées, convention II applicable, niveau, impact potentiel sur les deux volumes, figures et Lean, proposition motivée, alternatives si nécessaire. Distinguer une collision intra-volume II (exception à instruire) d'une adaptation normale du volume I.

**Livrable :** `G0_04_collision_report.md`.

**Porte :** collisions significatives recensées, priorisées, traçables ; aucun changement des manuscrits.

## 9. G0.5 — Arbitrage des conventions

**But :** décider le minimum de changements nécessaires, sous primauté du volume II.

Établir les réservations globales, thématiques ou locales à partir des définitions V5.17 et de l'audit V5.16 actualisé. En cas de même objet, appliquer le symbole II ; en cas d'objets distincts, adapter le I dans la portée de réservation. Une exception impliquant II requiert une justification scientifique et une validation spécifique.

Traiter par lots cohérents :

| Lot | Famille |
|---|---|
| L1 | Noyau dynamique et paramètres |
| L2 | États, espaces et exécutions |
| L3 | Histoires et temporalités |
| L4 | Sondes, protocoles et résolutions |
| L5 | Observations, réponses et projections |
| L6 | Équivalences, accessibilité, séparabilité |
| L7 | Fibres, opacité, partitions et stratification |
| L8 | Indices locaux, paramètres expérimentaux et spectre |

Instruire d'abord les dépendances de chaque lot ; présenter les propositions par familles, pas par occurrence. Pour une décision, consigner identifiant stable, objets concernés, ancien et nouveau symbole, portée, règle II applicable, justification, sources, impacts, alternatives, statut (`proposed`, `accepted`, `rejected`, `deferred`), validation et date. Une conservation est aussi une décision. Les nouveaux symboles doivent être contrôlés contre l'ensemble du registre pour éviter des collisions induites.

**Livrables :** `notations/decisions.yaml`, `conventions.yaml`, `G0_05_arbitration_report.md`.

**Porte :** validation humaine des décisions N2–N4 et exceptions ; toute réserve différée est explicitement évaluée, notamment son impact sur G–L. Aucune application automatique avant acceptation du lot.

## 10. G0.6 — Référentiel canonique versionné

**But :** transformer les décisions en une norme exploitable.

Finaliser `registry.yaml` et `conventions.yaml` ; conserver les anciennes notations et les relations du crosswalk. Les décisions gardent l'historique et le registre décrit l'état canonique résultant. Définir un schéma minimal vérifiable, des références stables et une validation d'unicité des identifiants. Générer `NOTATIONS.md` avec objets, symboles, types, portées, définitions, relations et raccord Lean si connu.

Construire `forbidden_patterns.yaml` à partir des audits actualisés et des décisions acceptées. Les règles doivent tenir compte des portées : un motif lexical n'est pas un vérificateur sémantique. Documenter faux positifs, exemptions et contrôles manuels. Tester extraction, rendu et contrôles sur des exemples autorisés/interdits ; prévoir une exécution simple en ligne de commande et des codes de sortie documentés.

**Livrables :** registre, conventions, décisions, crosswalk, documentation générée, scripts `extract_symbols.py`, `check_notations.py`, `render_registry.py` ou équivalents, tests.

**Porte :** référentiel validé et cohérent, rendu reproductible, contrôles utilisables ; aucune décision provisoire présentée comme canonique.

## 11. G0.7 — Application contrôlée aux manuscrits

**But :** harmoniser le volume I sur le volume II sans modifier les mathématiques.

Travailler par lots acceptés et commits atomiques. Appliquer les corrections d'abord aux définitions et à leurs usages dépendants, en priorité dans le livre III et G–L lorsque les dépendances le permettent. Les livres I–II et A–F sont corrigés si les conventions le nécessitent, sans modifier les résultats certifiés. Les corrections de II sont limitées aux anomalies internes validées et à la cohérence documentaire. Vérifier tables, légendes, références, notes compagnons actives et figures. Les archives historiques sont conservées.

Introduire éventuellement des macros sémantiques pour les objets structurants récurrents (par exemple `\IWSFlowSet`), après vérification de l'absence de conflit. Ne pas multiplier les macros pour les variables locales ni imposer un préambule commun sans bénéfice démontré. Toute macro doit préserver le rendu et être documentée.

Après chaque lot : contrôler le diff et les occurrences ciblées ; comparer les expressions avant/après en tenant compte des renommages autorisés ; vérifier absence de capture de variable ou changement de type ; contrôler hypothèses, conclusions, labels et statut des résultats ; compiler les volumes concernés et comparer avec les logs initiaux. La comparaison textuelle normalisée aide mais ne prouve pas l'équivalence mathématique ; effectuer une relecture ciblée des énoncés modifiés.

**Livrable :** `G0_07_changes.md`, commits par lot, rapports de compilation et contrôles.

**Porte :** toutes les décisions acceptées appliquées ou exceptions documentées ; aucun changement mathématique non autorisé ; compilations validées.

### 11.1. Sous-chantier figures

Créer une table de provenance : figure, emplacement, script, dépôt/commit, données, commande, environnement, statut, changements notationnels requis. Dans `IWS_minimality_package/scripts/genealogie_n9/`, les générateurs `make_fig_adaptive.py`, `make_fig_recursive.py`, `make_fig_walls_control.py` ont été identifiés par leurs noms de sortie. Le second produit notamment un PDF ; la chaîne exacte vers le PNG du manuscrit reste à confirmer. Les autres figures ne disposent pas encore d'une provenance certaine. Les générateurs des figures scientifiques du volume I restent à identifier si nécessaires.

Des chemins historiques, des caches `.pkl`/`.npy` absents et une instruction de sauvegarde mal construite ont été constatés ; ne pas prétendre à une reproduction sans exécution. Corriger uniquement ce qui est nécessaire à la régénération, dans une branche expérimentale distincte si besoin. Ne pas modifier les paramètres, données ou résultats pour des raisons éditoriales. Comparer les figures régénérées et documenter toute différence.

L'ancien libellé « chambre(s) » dans `opacity_recursive_refinement.png` est un point connu de l'audit V5.16. Si une figure ne peut être régénérée, consigner le blocage et décider explicitement si une correction de légende suffit, ou si elle empêche la clôture. Une figure trompeuse non corrigée ne peut être déclarée conforme.

## 12. G0.8 — Raccord documentaire avec Lean

**But :** garantir que le futur travail Lean emploie les bons objets, sans déstabiliser A, C et D.

Consulter les définitions et signatures réelles sur le commit gelé de `iws-lean`. Pour chaque objet formalisé, enregistrer l'identifiant sémantique, le symbole canonique, le nom Lean qualifié, le fichier, le commit, les hypothèses, et le degré de correspondance (exacte, représentation, partielle, conditionnelle, non formalisée). Une construction Lean peut représenter plusieurs objets du manuscrit ou une spécialisation ; le signaler.

Conserver les identifiants et preuves existants. Proposer si nécessaire un lien vers la version du registre dans le README Lean, avec validation distincte avant tout changement de ce dépôt. Si des modifications Lean sont autorisées, comparer signatures et définitions, reconstruire avec les dépendances figées et refaire l'audit des axiomes. Sans modification, documenter le bilan de référence, sans revendiquer un nouveau build.

Préparer la liste des objets de G, leurs dépendances sur le noyau et leurs conventions de nommage ; ne pas écrire de nouvelle formalisation dans G0. Ne pas présupposer la dépendance exacte de H–L avant lecture des sources.

**Livrables :** `notations/lean_crosswalk.csv`, `G0_08_lean_report.md`.

**Porte :** raccord des objets déjà formalisés documenté ; objets de G identifiés ; aucune régression ou modification scientifique non autorisée.

## 13. G0.9 — Audit final et clôture

Relancer les contrôles sur les sources finales : couverture, réservations, anciens symboles, motifs interdits, références et macros, correspondance intervolumes, compilation et figures. Vérifier que les décisions acceptées sont effectivement appliquées, que les statuts scientifiques et les hypothèses sont préservés et que le raccord Lean est à jour. Comparer au manifeste initial et consigner les résultats réellement observés.

Classer les réserves en bloquantes, non bloquantes acceptées ou hors périmètre. Une ambiguïté touchant un objet nécessaire à G ne peut pas être reportée silencieusement. Aucun résultat de contrôle non exécuté ne doit être marqué validé.

**Livrable :** `G0_09_closure_report.md`, registre final, `STATUS.md` actualisé, README synchronisé. Proposer un tag `iws-notations-v1.0` après validation humaine et intégration des commits. Référencer cette version dans Lean au début de G.

**Conditions de clôture :**

- [ ] Sources et commits de référence identifiés ; compilations initiales et finales documentées.
- [ ] Inventaire lexical et sémantique couvrant les objets structurants.
- [ ] Correspondances intervolumes justifiées ou inconnues explicites.
- [ ] Collisions significatives arbitrées sous primauté du volume II.
- [ ] Registre, règles et documentation versionnés et cohérents.
- [ ] Corrections LaTeX vérifiées, sans changement mathématique non autorisé.
- [ ] Figures conformes ou réserves non bloquantes explicitement acceptées.
- [ ] Raccord Lean et limites de formalisation documentés.
- [ ] Aucun blocage notationnel ou sémantique identifié pour G.
- [ ] Rapport de clôture accepté et version de référence fixée.

## 14. Pilotage et consignes aux agents

L'agent réalise extraction, classification préliminaire, lecture sourcée, propositions, scripts, modifications acceptées et contrôles. L'auteur arbitre les identités mathématiques incertaines, les nouvelles notations, les exceptions et les réserves. Il valide les portes de phase ; inutile de lui soumettre chaque occurrence.

À chaque phase : lire le plan et `STATUS.md`, vérifier le commit de départ, respecter les exclusions, produire le livrable, distinguer faits/propositions/inconnues, mettre à jour le statut et s'arrêter à la porte prévue. Ne pas enchaîner un arbitrage ou un changement scientifique sans validation. Les travaux indépendants en lecture seule peuvent être parallélisés ; les écritures dans le registre et les sources doivent être coordonnées. Ne pas utiliser plusieurs sources normatives concurrentes.

`STATUS.md` doit contenir le dernier commit de travail, la phase, les livrables terminés, les résultats des contrôles, les décisions attendues, les blocages et une prochaine action concrète. Chaque réserve reçoit un identifiant, des références, une description, son impact, son statut et un responsable de décision. Les progrès ne sont jamais déduits de la simple existence d'un fichier.

| Phase | État initial au 27/11/2026 |
|---|---|
| G0.0 | Préparation documentaire largement acquise ; gel et compilation à faire |
| G0.1 | Audit rho historique disponible ; inventaire complet à faire |
| G0.2 | Audit notation–rôle II V5.16 disponible ; registre à construire |
| G0.3 | Table intervolumes à construire |
| G0.4 | Candidats connus ; diagnostic exhaustif à faire |
| G0.5 | Primauté II validée ; arbitrages individuels à faire |
| G0.6–G0.9 | À faire |

## 15. Première mission opérationnelle

Exécuter **G0.0 uniquement**. Lire le présent plan, actualiser le README documentaire si autorisé, résoudre les commits des dépôts, établir le manifeste des sources actives et tenter les compilations de référence. Documenter les obstacles et créer `STATUS.md`. Ne modifier ni les notations, ni les équations, ni les preuves. Ne pas lancer G0.1 avant validation du bilan G0.0.

---

Ce plan intègre les vérifications précédentes et la décision de primauté du volume II. Les formats YAML/CSV, noms de scripts, branche et tag sont des propositions techniques, ajustables sans changer le principe scientifique. Le plan ne constitue pas l'exécution des audits, des compilations ou des modifications Git.
